from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from database import get_db
from database import SessionLocal
from auth.google import oauth
from schemas.users import (
    UserCreate,
    UserUpdate,
    UserPatch,
    LoginRequest
)
from auth.security import (
    verify_password,
    create_access_token,
    create_refresh_token,
    verify_refresh_token,
    get_current_user,
)
from services.user_services import UserService


router = APIRouter()

user_service = UserService()


@router.get("/auth/google")
async def google_login(request: Request):
    redirect_uri = request.url_for("google_callback")

    return await oauth.google.authorize_redirect(
        request,
        redirect_uri
    )

@router.get("/auth/google/callback")
async def google_callback(request: Request):

    db = SessionLocal()

    try:
        # 1. Google authorization code ko token mein exchange karo
        token = await oauth.google.authorize_access_token(request)

        # 2. Google se user information nikalo
        user_info = token.get("userinfo")

        if not user_info:
            raise HTTPException(
                status_code=400,
                detail="Google user information not found"
            )

        # 3. Required Google information nikalo
        email = user_info.get("email")
        first_name = user_info.get("given_name")
        last_name = user_info.get("family_name")

        # 4. Basic validation
        if not email:
            raise HTTPException(
                status_code=400,
                detail="Google account email not found"
            )

        if not user_info.get("email_verified"):
            raise HTTPException(
                status_code=400,
                detail="Google email is not verified"
            )

        # 5. Local database mein email se user search karo
        user = user_service.repository.get_user_by_email(
            db,
            email
        )

        # 6. Agar user nahi mila → new user create karo
        if user is None:
            user = user_service.create_google_user(
                db,
                first_name or "",
                last_name or "",
                email
            )

        # 7. Hamare application ka JWT create karo
        access_token = create_access_token(user.id)
        refresh_token = create_refresh_token(user.id)

        request.session["user_id"] = user.id
        request.session["access_token"] = access_token
        request.session["refresh_token"] = refresh_token


        # 8. Client ko JWT return karo
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }

    except HTTPException:
        raise

    except Exception as e:
        print("Google login error", repr(e))
        raise

    # except Exception:
    #     raise HTTPException(
    #         status_code=500,
    #         detail="Google login failed"
    #     )

    finally:
        db.close()


@router.post("/refresh")
def refresh_access_token(request: Request):

    refresh_token = request.session.get("refresh_token")

    if not refresh_token:
        raise HTTPException(
            status_code=401,
            detail="Refresh token not found"
        )

    user_id = verify_refresh_token(refresh_token)

    new_access_token = create_access_token(user_id)

    request.session["access_token"] = new_access_token

    return {
        "access_token": new_access_token,
        "token_type": "bearer"
    }


@router.get("/test-session")
async def test_session(request: Request):
    return {
        "user_id": request.session.get("user_id"),
        "access_token": request.session.get("access_token"),
        "refresh_token": request.session.get("refresh_token")
    }



@router.post("/login")
def login(login_data: LoginRequest,request:Request):
    db = SessionLocal()

    try:
        user = user_service.repository.get_user_by_email(
            db,
            login_data.email
        )

        if user is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid email or password"
            )

        password_valid = verify_password(
            login_data.password,
            user.password_hash
        )

        if not password_valid:
            raise HTTPException(
                status_code=401,
                detail="Invalid email or password"
            )

        access_token = create_access_token(user.id)
        refresh_token = create_refresh_token(user.id)

        request.session["user_id"] = user.id
        request.session["access_token"] = access_token
        request.session["refresh_token"] = refresh_token

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }

    except HTTPException:
        raise

    except Exception as e:
        print("LOGIN ERROR:", repr(e))
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

    finally:
        db.close()


@router.post("/logout")
def logout(request: Request):
    request.session.clear()

    return {
        "message": "Logged out successfully"
    }



@router.post("/users")
def create_user(user_data: UserCreate):

    db = SessionLocal()

    try:
        return user_service.create_user(db, user_data)

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Failed to create user"
        )

    finally:
        db.close()


@router.get("/users")
def get_users(current_user = Depends(get_current_user),db: Session = Depends(get_db)):
    print(current_user.id)
    print(current_user.email)

    
    
    try:
        return user_service.get_users(db)

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Failed to fetch users"
        )

    


@router.get("/users/me")
def get_my_profile(
    current_user=Depends(get_current_user)
):
    return current_user


@router.put("/users/me")
def update_my_profile(
    user_data: UserUpdate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
   

    try:
        user = user_service.update_user(
            db,
            current_user,
            user_data
        )

        return user

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Failed to update user"
        )



@router.patch("/users/me")
def patch_my_profile(
    user_data: UserPatch,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    

    try:
        user = user_service.patch_user(
            db,
            current_user,
            user_data
        )

        return user

    except HTTPException:
        raise

    except Exception as e:
        print("PATCH ERROR:", repr(e))
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )




@router.delete("/users/me")
def delete_my_account(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    

    try:
        user_service.delete_user(
            db,
            current_user
        )

        return {
            "message": "User deleted successfully"
        }

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Failed to delete user"
        )

    