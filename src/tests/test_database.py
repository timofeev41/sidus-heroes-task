import random
import string

import pytest

from ..modules import models
from ..modules.database import crud, schemas
from . import db_session


def test_create_user(db_session):
    new_user = schemas.UserPassword(username="TESTUSER", full_name="TEST USER", details="TEST", password="pass")
    crud.create_user(db_session, user=new_user)

    created_user = crud.get_user_by_username(db_session, username="TESTUSER")
    assert created_user
    assert isinstance(created_user.id, int)
    assert created_user.username == new_user.username


def test_get_nonexistent_user(db_session):
    user = crud.get_user_by_username(
        db_session, username="".join(random.choice(string.ascii_letters) for _ in range(random.randint(3, 15)))
    )
    assert not user


def test_authorize_user(db_session):
    credentials = models.Credentials(login="TESTUSER", password="pass")
    token = crud.authorize_user(db_session, credentials=credentials)
    assert token


def test_get_users(db_session):
    users = crud.get_users(db_session)
    assert len(users) > 0


def test_edit_user(db_session):
    new_user_data = schemas.UserPassword(
        username="TESTUSER", full_name="NEW NAME", details="NEW DETAILS", password="NEW PASS"
    )
    crud.edit_user(db_session, username="TESTUSER", new_data=new_user_data)

    new_user = crud.get_user_by_username(db_session, username="TESTUSER")
    assert new_user
    assert new_user.full_name == "NEW NAME"
    assert new_user.details == "NEW DETAILS"


def test_remove_created_user(db_session):
    crud.purge_user(db_session, username="TESTUSER")
    new_user = crud.get_user_by_username(db_session, username="TESTUSER")
    assert not new_user
