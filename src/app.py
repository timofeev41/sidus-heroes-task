from fastapi import FastAPI, Depends, HTTPException
from .modules import models, database, crud, schemas

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()


@app.get("/users", response_model=list[schemas.User])
async def get_users(
    skip: int = 0, limit: int = 100, db: database.Session = Depends(database.get_db)
) -> list[schemas.User]:
    users = crud.get_users(db)
    return users


@app.get("/users/{username}", response_model=schemas.User)
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


@app.patch("/users/{username}")
async def edit_user(username: str) -> None:
    pass
