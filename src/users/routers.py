from fastapi import APIRouter, Depends, HTTPException
from starlette.status import HTTP_400_BAD_REQUEST
from src.database import get_async_session
from src.users.models import User, Token
from sqlalchemy import select
from src.tokens.tokens import check_token_valid


router = APIRouter(
    prefix="/main",
    tags=["main"]
)


@router.post("/change_balance", status_code=200)
async def change_balance(delta: int, access_token: str, session=Depends(get_async_session)):
    if not await check_token_valid(access_token, session):
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Token isn't valid!")
    token: Token = await session.scalar(select(Token).where(Token.access_token == access_token))
    token.use_num -= 1
    if token.use_num <= 0:
        await session.delete(token)

    user: User = await session.scalar(select(User).where(token.user_id == User.id))

    user.balance += delta
    await session.commit()
    return {"detail": "Success"}


@router.get("/ladder", status_code=200)
async def ladder(num: int, session=Depends(get_async_session)):
    query = select(User.username, User.balance).order_by(User.balance.desc()).limit(num)
    res = await session.execute(query)

    return res.mappings().all()

@router.get("/watch_all", status_code=200)
async def watch_all(session=Depends(get_async_session)):
    query = select(User.username, User.balance).order_by(User.balance.desc())
    res = await session.execute(query)

    return res.mappings().all()
