from pydantic import BaseModel


class OrderCreate(BaseModel):
    user_id: int
    product: str
    amount: int
    status: str


class OrderUpdate(BaseModel):
    user_id: int
    product: str
    amount: int
    status: str


class OrderPatch(BaseModel):
    user_id: int | None = None
    product: str | None = None
    amount: int | None = None
    status: str | None = None   