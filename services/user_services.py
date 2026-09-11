from sqlalchemy.orm import Session

from repositories.user_repository import UserRepository


class UserService:

    def __init__(self):
        self.repository = UserRepository()

    def create_user(self, db: Session, user_data):
        return self.repository.create_user(db, user_data)

    def get_users(self, db: Session):
        return self.repository.get_all_users(db)

    def get_user(self, db: Session, user_id: int):
        return self.repository.get_user_by_id(db, user_id)

    def update_user(self, db: Session, user_id: int, user_data):
        user = self.repository.get_user_by_id(db, user_id)

        if user is None:
            return None

        return self.repository.update_user(
            db,
            user,
            user_data
        )

    def patch_user(self, db: Session, user_id: int, user_data):
        user = self.repository.get_user_by_id(db, user_id)

        if user is None:
            return None

        return self.repository.patch_user(
            db,
            user,
            user_data
        )

    def delete_user(self, db: Session, user_id: int):
        user = self.repository.get_user_by_id(db, user_id)

        if user is None:
            return None

        self.repository.delete_user(db, user)

        return True