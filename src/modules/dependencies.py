from fastapi import Depends, Header, HTTPException
from sqlalchemy.orm import Session

from . import models
from .database import crud, schemas
from .database.database import get_db


async def generate_token(credentials: models.Credentials) -> models.Token:
    return models.Token(token=credentials.login + "__" + credentials.password)


async def read_token(token: str = Header(), db: Session = Depends(get_db)) -> schemas.UserPassword:
    try:
        user = crud.authorize_user(
            db, credentials=models.Credentials(login=token.split("__")[0], password=token.split("__")[1])
        )
    except Exception:
        raise HTTPException(status_code=500, detail="failed to decode token")
    if not user:
        raise HTTPException(status_code=403, detail="unauthorized")
    return user
