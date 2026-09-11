from sqlalchemy.orm import Session
from models.user import User


class UserRepository:

    def create_user(self, db: Session, user_data):
        user = User(
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            email=user_data.email,
            age=user_data.age,
            phone=user_data.phone,
            pincode=user_data.pincode
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        return user

    def get_all_users(self, db: Session):
        return db.query(User).all()

    def get_user_by_id(self, db: Session, user_id: int):
        return db.query(User).filter(User.id == user_id).first()

    def update_user(self, db: Session, user, user_data):
        user.first_name = user_data.first_name
        user.last_name = user_data.last_name
        user.email = user_data.email
        user.age = user_data.age
        user.phone = user_data.phone
        user.pincode = user_data.pincode

        db.commit()
        db.refresh(user)

        return user

    def patch_user(self, db: Session, user, user_data):
        if user_data.first_name is not None:
            user.first_name = user_data.first_name

        if user_data.last_name is not None:
            user.last_name = user_data.last_name    

        if user_data.email is not None:
            user.email = user_data.email

        if user_data.age is not None:
            user.age = user_data.age

        if user_data.phone is not None:
            user.phone = user_data.phone

        if user_data.pincode is not None:
            user.pincode = user_data.pincode    

        db.commit()
        db.refresh(user)

        return user

    def delete_user(self, db: Session, user):
        db.delete(user)
        db.commit()