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



load_dotenv()
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

    