from sqlalchemy import update
from sqlalchemy.orm import Session

from ..models import Credentials

from . import models

from . import schemas


def get_user(db: Session, user_id: int) -> schemas.UserEditable | None:
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_username(db: Session, username: str) -> schemas.UserEditable | None:
    return db.query(models.User).filter(models.User.username == username).first()


def authorize_user(db: Session, credentials: Credentials) -> schemas.UserPassword | None:
    return (
        db.query(models.User)
        .filter(models.User.username == credentials.login, models.User.password == credentials.password + "1234")
        .first()
    )


def get_users(db: Session, skip: int = 0, limit: int = 100) -> list[schemas.UserPassword]:
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserPassword):
    fake_hashed_password = user.password + "1234"
    db_user = models.User(
        username=user.username, password=fake_hashed_password, full_name=user.full_name, details=user.details
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def edit_user(db: Session, username: str, new_data: schemas.UserEditable):
    db_user = get_user_by_username(db, username=username)
    if not db_user:
        raise ValueError("User not found, nothing to update")

    # if nothing to update
    if db_user == new_data:
        return db_user

    db.query(models.User).filter(models.User.username == username).update(new_data.dict())
    db.commit()
    return db_user
