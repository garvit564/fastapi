from fastapi import APIRouter, HTTPException

from database import SessionLocal

from schemas.users import (
    UserCreate,
    UserUpdate,
    UserPatch
)

from services.user_services import UserService


router = APIRouter()

user_service = UserService()


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
def get_users():

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
def get_user(user_id: int):

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
    user_data: UserUpdate
):

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
    user_data: UserPatch
):

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
def delete_user(user_id: int):

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