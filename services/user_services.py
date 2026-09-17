from sqlalchemy.orm import Session

from repositories.user_repository import UserRepository


class UserService:

    def __init__(self):
        self.repository = UserRepository()

    def create_user(self, db: Session, user_data):
        return self.repository.create_user(db, user_data)

    def create_google_user(
        self,
        db: Session,
        first_name: str,
        last_name: str,
        email: str
    ):
        return self.repository.create_google_user(
            db,
            first_name,
            last_name,
            email
        )

    def get_users(self, db: Session):
        return self.repository.get_all_users(db)

    def get_user(self,db:Session,user_id):
        user = self.repository.get_user_by_id(db,user_id)

        return user

    def update_user(
        self,
        db: Session,
        user_id,
        user_data
    ):
        return self.repository.update_user(
            db,
            user_id,
            user_data
        )

    def patch_user(
        self,
        db: Session,
        user_id,
        user_data
    ):
        return self.repository.patch_user(
            db,
            user_id,
            user_data
        )

    def delete_user(
        self,
        db: Session,
        user_id
    ):
        self.repository.delete_user(
            db,
            user_id
        )

        return True