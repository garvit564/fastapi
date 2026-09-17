from fastapi import Request, HTTPException
from passlib.context import CryptContext
import os
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from database import SessionLocal
from jose import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from database import SessionLocal
from database import get_db
from sqlalchemy.orm import Session
from models.user import User
import logging
from functools import wraps
from inspect import signature
load_dotenv()

logger = logging.getLogger(__name__)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(password: str, password_hash: str):
    return pwd_context.verify(password, password_hash)



SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = "HS256"

def create_access_token(user_id:int):
    expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    payload = {
        "sub":str(user_id),
        "exp":expire
    }
    token = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )
    return token


def create_refresh_token(user_id: int):
    expire = datetime.now(timezone.utc) + timedelta(days=7)
    payload = {
        "sub":str(user_id),
        "type":"refresh",
        "exp":expire
    }
    token = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )
    return token

def verify_refresh_token(token: str):
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        if payload.get("type") != "refresh":
            raise HTTPException(
                status_code=401,
                detail="Invalid refresh token"
            )

        user_id = payload.get("sub")

        if user_id is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid refresh token"
            )

        return int(user_id)

    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired refresh token"
        )


def get_current_user(request: Request,db:Session = Depends(get_db)):
    user_id = request.session.get("user_id")

    if user_id is None:
        raise HTTPException(
            status_code=401,
            detail="Not authenticated"
        )
    
    user = db.query(User).filter(User.id == user_id).first()

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="User not found"
        )
    return user




def get_current_user_id(func):

    original_signature = signature(func)

    parameters = [
        parameter
        for name, parameter in original_signature.parameters.items()
        if name != "user_id"
    ]

    @wraps(func)
    def wrapper(*args, **kwargs):

        # request nikalo
        request = kwargs.get("request")

        if request is None:
            raise HTTPException(
                status_code=401,
                detail="Request not found"
            )

        # db nikalo
        db = kwargs.get("db")

        if db is None:
            raise HTTPException(
                status_code=500,
                detail="Database session not found"
            )

        # existing get_current_user use karo
        current_user = get_current_user(request, db)

        # User object se sirf ID nikalo
        user_id = current_user.id

        # API ke kwargs mein user_id add karo
        kwargs["user_id"] = user_id

        # original API call karo
        return func(*args, **kwargs)

    wrapper.__signature__ = original_signature.replace(
        parameters=parameters
    )

    return wrapper