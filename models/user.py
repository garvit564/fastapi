from sqlalchemy import Column, Integer, String

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    # name = Column(String(100), nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    age = Column(Integer, nullable=False)
    phone = Column(String(20),nullable=True)
    pincode = Column(String(20),nullable=True)
    password_hash = Column(String(255), nullable=True)