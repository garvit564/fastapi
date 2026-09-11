from pydantic import BaseModel


class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: str
    age: int
    phone: str
    pincode:str


class UserUpdate(BaseModel):
    first_name: str
    last_name: str
    email: str
    age: int
    phone:str
    pincode:str


class UserPatch(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None
    age: int | None = None
    phone: str | None = None
    pincode: str | None = None