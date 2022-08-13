from pydantic import BaseModel


class Token(BaseModel):
    token: str


class Credentials(BaseModel):
    login: str
    password: str
