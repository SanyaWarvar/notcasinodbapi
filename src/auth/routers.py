import uuid
from fastapi import APIRouter, Depends, HTTPException
from starlette.status import HTTP_400_BAD_REQUEST
from src.database import get_async_session
from src.users.models import User, Token
from src.users.schemes import UserCreate
from sqlalchemy import select

from secure import pwd_contex

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


@router.post("/register", status_code=200)
async def register_user(user_create: UserCreate, session=Depends(get_async_session)):
    query = select(User).where(User.username == user_create.username)
    res = await session.scalar(query)
    if not res:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=f"User {user_create.username} already exist!"
        )

    session.add(User(
        username=user_create.username,
        hashed_password=pwd_contex.hash(user_create.password),
    ))
    await session.commit()

    return {"detail": "Success"}


@router.post("/generate_token", status_code=201)
async def create_token(user_create: UserCreate, session=Depends(get_async_session)):
    query = select(User).where(User.username == user_create.username)
    # result = await session.execute(query)

    target_user: User = await session.scalar(query)

    if not target_user or not pwd_contex.verify(user_create.password, target_user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    token: Token = Token(user_id=target_user.id, access_token=str(uuid.uuid4()))
    session.add(token)
    await session.commit()

    return {"access_token": token.access_token}
