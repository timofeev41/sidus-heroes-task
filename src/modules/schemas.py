from pydantic import BaseModel


class User(BaseModel):
    id: int
    username: str
    full_name: str
    details: str

    class Config:
        orm_mode = True


class UserPassword(User):
    password: str
