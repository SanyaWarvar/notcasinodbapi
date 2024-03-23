import uuid
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED
from src.database import get_async_session
from src.tokens.tokens import check_token_valid
from src.users.models import User, Token
from src.users.schemes import UserCreate
from sqlalchemy import select, delete
from secure import pwd_contex

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


@router.get("/check_token_valid", status_code=200)
async def check_token(access_token: str, session=Depends(get_async_session)):
    if not await check_token_valid(access_token, session):
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Token isn't valid!")
    return {"access_token": access_token}


@router.post("/register", status_code=201)
async def register_user(user_create: UserCreate, session=Depends(get_async_session)):
    query = select(User).where(User.username == user_create.username)
    res = await session.scalar(query)
    if res is not None:
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




    await session.execute(delete(Token).where(Token.user_id == target_user.id))
    await session.commit()

    token: Token = Token(user_id=target_user.id, access_token=str(uuid.uuid4()))
    session.add(token)
    await session.commit()

    return {"access_token": token.access_token}
