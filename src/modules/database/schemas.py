from __future__ import annotations

from pydantic import BaseModel


class User(BaseModel):
    id: int

    class Config:
        orm_mode = True


class UserEditableInformation(BaseModel):
    username: str
    full_name: str
    details: str


class UserPassword(UserEditableInformation):
    password: str


class UserPublicInformation(User, UserEditableInformation):
    pass


class UserPrivateInformation(User, UserPassword):
    pass
