from pydantic import BaseModel


class UserBase(BaseModel):
    username: str


class User(UserBase):
    id: int

    class Config:
        orm_mode = True


class UserCreate(UserBase):
    password: str
    email: str
    first_name: str
    last_name: str

    class Config:
        orm_mode = True
