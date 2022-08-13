from pydantic import BaseModel


class User(BaseModel):
    id: int

    class Config:
        orm_mode = True


class UserEditable(User):
    username: str
    full_name: str
    details: str


class UserPassword(UserEditable):
    password: str
