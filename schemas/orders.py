from pydantic import BaseModel


class OrderCreate(BaseModel):
    user_id: int
    product: str
    amount: int
    description: str
    status: str


class OrderUpdate(BaseModel):
    user_id: int
    product: str
    amount: int
    description: str
    status: str


class OrderPatch(BaseModel):
    user_id: int | None = None
    product: str | None = None
    amount: int | None = None
    description: str | None = None
    status: str | None = None   