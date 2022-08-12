from sqlalchemy import Column, String, Integer
from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    password = Column(String)
    full_name = Column(String)
    details = Column(String)
