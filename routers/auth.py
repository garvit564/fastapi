from fastapi import APIRouter, HTTPException
from auth.security import verify_password, create_access_token
from database import SessionLocal
from repositories import user_repository
from models.user import User

router = APIRouter()


# @router.post("/login")
# def login(email:str,password:str):
#     db = SessionLocal()

#     try:
#         user = user_repository.get_user_by_email(db,email)

#         if user is None:
#             raise HTTPException(
#                 status_code=401,
#                 detail="invalid username or password"
#             )
#         if not verify_password(password,user.password_hash):
#             raise HTTPException(
#                 status_code=401,
#                 detail="innvalid username or password"
#             )

#         token = create_access_token(user.id)
#         return {
#             "access_token": token,
#             "token_type":"bearer"
#         }
#     finally:
#         db.close()