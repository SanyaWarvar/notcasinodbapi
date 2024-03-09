from fastapi import FastAPI
from src.auth.routers import router as auth_router
from src.users.routers import router as main_router
from src.roulette.routers import router as roulette_router


app = FastAPI(
    title="Lucky_000_DB_API"
)


@app.get("/", status_code=200)
def hello_world():
    return {"detail": "Hello world"}


app.include_router(auth_router)
app.include_router(main_router)
app.include_router(roulette_router)
