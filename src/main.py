import psycopg2
from fastapi import FastAPI
from fastapi_users import FastAPIUsers
from src.auth.base_config import auth_backend
from src.auth.manager import get_user_manager
from src.auth.models import User
from src.auth.schemas import UserRead, UserCreate
from src.config import *

app = FastAPI(
    title="Lucky_000_DB_API"
)

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

connection = psycopg2.connect(
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASS,
    database=DB_NAME
)
connection.autocommit = True

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

current_user = fastapi_users.current_user()
