from sqlalchemy import Column, Integer, String, ForeignKey

from database import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    product = Column(String(150), nullable=False)
    amount = Column(Integer, nullable=False)
    description = Column(String(100), nullable=True)
    status = Column(String(50), nullable=False)