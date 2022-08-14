import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

# from .. import app

# client = TestClient(app.app)


@pytest.fixture
def db_session():
    """returns a SQLAlchemy scoped session"""
    engine = create_engine("sqlite:///./sql_app.db", echo=True)
    session_ = scoped_session(sessionmaker(bind=engine))
    yield session_
    engine.dispose()
    session_.rollback()
    session_.close()
