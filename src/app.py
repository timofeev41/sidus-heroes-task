from typing import no_type_check

import aioredis
from fastapi import Depends, FastAPI, HTTPException
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache

from .modules.database import crud, database, models, schemas
from .modules.dependencies import generate_token, read_token
from .modules.models import Credentials, Token

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()


@app.get("/users", response_model=list[schemas.UserPublicInformation])
async def get_users(
    skip: int = 0, limit: int = 100, db: database.Session = Depends(database.get_db)
) -> list[schemas.UserPublicInformation]:
    users: list[schemas.UserPublicInformation] = crud.get_users(db)
    return users


@app.get("/users/{username}", response_model=schemas.UserPublicInformation)
@cache(namespace="user", expire=60)
async def get_concrete_user(
    username: str, db: database.Session = Depends(database.get_db)
) -> schemas.UserPublicInformation | None:
    user = crud.get_user_by_username(db, username=username)
    return user


@app.post("/users", response_model=schemas.UserPublicInformation)
async def create_user(
    user: schemas.UserPassword, db: database.Session = Depends(database.get_db)
) -> schemas.UserPassword:
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail=f"User {user.username} already registered")
    return crud.create_user(db, user=user)


@app.post("/auth")
async def get_token(credentials: Credentials, db: database.Session = Depends(database.get_db)) -> Token:
    user = crud.authorize_user(db, credentials=credentials)
    if not user:
        raise HTTPException(status_code=403, detail="wrong login/password")
    return await generate_token(credentials=credentials)


@app.patch("/me")
async def edit_user(
    new_data: schemas.UserEditableInformation,
    user: schemas.UserPassword = Depends(read_token),
    db: database.Session = Depends(database.get_db),
) -> dict[str, str]:
    await FastAPICache.clear(namespace="user")
    crud.edit_user(db, username=user.username, new_data=new_data)
    return {"status": f"data for user {user.username} updated"}


@app.get("/me")
async def get_my_profile(user: schemas.UserPassword = Depends(read_token)) -> schemas.UserPassword:
    return user


@app.on_event("startup")
@no_type_check
async def startup() -> None:
    redis = aioredis.from_url("redis://redis_cache", encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
