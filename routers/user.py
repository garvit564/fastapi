from fastapi import APIRouter, Depends, HTTPException

from database import SessionLocal

from schemas.users import (
    UserCreate,
    UserUpdate,
    UserPatch,
    LoginRequest
)
from auth.security import (
    verify_password,
    create_access_token,
    get_current_user,
)
from services.user_services import UserService


router = APIRouter()

user_service = UserService()


@router.post("/login")
def login(login_data: LoginRequest):
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

        return {
            "access_token": access_token,
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
def get_users(current_user = Depends(get_current_user)):
    print(current_user.id)
    print(current_user.email)

    db = SessionLocal()
    
    try:
        return user_service.get_users(db)

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Failed to fetch users"
        )

    finally:
        db.close()


@router.get("/users/{user_id}")
def get_user(
    user_id: int,
    current_user=Depends(get_current_user)):

    if user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You cannot access another user's profile"
        )

    db = SessionLocal()

    try:
        user = user_service.get_user(db, user_id)

        if user is None:
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )

        return user

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Failed to fetch user"
        )

    finally:
        db.close()


@router.put("/users/{user_id}")
def update_user(
    user_id: int,
    user_data: UserUpdate,
    current_user=Depends(get_current_user)
):

    if user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You cannot update another user's profile"
        )

    db = SessionLocal()

    try:
        user = user_service.update_user(
            db,
            user_id,
            user_data
        )

        if user is None:
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )

        return user

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Failed to update user"
        )

    finally:
        db.close()


@router.patch("/users/{user_id}")
def patch_user(
    user_id: int,
    user_data: UserPatch,
    current_user=Depends(get_current_user)
):

    if user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You cannot update another user's profile"
        )

    db = SessionLocal()

    try:
        user = user_service.patch_user(
            db,
            user_id,
            user_data
        )

        if user is None:
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )

        return user

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Failed to update user"
        )

    finally:
        db.close()


@router.delete("/users/{user_id}")
def delete_user(
    user_id: int,
    current_user=Depends(get_current_user)):

    if user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You cannot delete another user's profile"
        )

    db = SessionLocal()

    try:
        result = user_service.delete_user(
            db,
            user_id
        )

        if result is None:
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )

        return {
            "message": "User deleted successfully"
        }

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Failed to delete user"
        )

    finally:
        db.close()