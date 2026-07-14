from fastapi import FastAPI

from routers import users, seasons

app = FastAPI()

app.include_router(users.router)
app.include_router(seasons.router)


@app.get("/")
def read_root():
    return {"message": "SportsHub backend is running"}