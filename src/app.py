import aioredis
from fastapi import FastAPI, Depends, HTTPException
from .modules.dependencies import generate_token, read_token
from .modules.models import Token, Credentials

from .modules.database import crud, database, models, schemas
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()


@app.get("/users", response_model=list[schemas.UserEditable])
async def get_users(
    skip: int = 0, limit: int = 100, db: database.Session = Depends(database.get_db)
) -> list[schemas.UserPassword]:
    users = crud.get_users(db)
    return users


@app.get("/users/{username}", response_model=schemas.UserEditable)
@cache(namespace="user", expire=60)
async def get_concrete_user(username: str, db: database.Session = Depends(database.get_db)) -> schemas.User | None:
    user = crud.get_user_by_username(db, username=username)
    return user


@app.post("/users", response_model=schemas.UserPassword)
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
    new_data: schemas.UserPassword,
    user: schemas.UserPassword = Depends(read_token),
    db: database.Session = Depends(database.get_db),
):
    await FastAPICache.clear(namespace="user")
    db_user = crud.edit_user(db, username=user.username, new_data=new_data)
    return db_user


@app.get("/me")
async def get_my_profile(user: schemas.UserPassword = Depends(read_token)) -> schemas.UserPassword:
    return user


@app.on_event("startup")
async def startup():
    redis = aioredis.from_url("redis://redis_cache", encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")  # type: ignore
