from fastapi import FastAPI


app = FastAPI()


@app.get("/users")
async def get_users() -> None:
    pass


@app.post("/users")
async def create_user() -> None:
    pass


@app.patch("/users/{username}")
async def edit_user(username: str) -> None:
    pass
