from sqlalchemy import Column, Integer, String

from .database import Base


class User(Base):  # type: ignore
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    password = Column(String)
    full_name = Column(String)
    details = Column(String)
