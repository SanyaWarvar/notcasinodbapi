from fastapi import FastAPI
from src.auth.base_config import auth_backend
from src.auth.schemas import UserRead, UserCreate
from src.auth.base_config import fastapi_users
from src.users.router import router as router_operation


app = FastAPI(
    title="Lucky_000_DB_API"
)


app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(router_operation)
