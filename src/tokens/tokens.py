import uuid
from datetime import datetime
from fastapi import Depends
from src.database import get_async_session
from src.users.models import User, Token
from secure import pwd_contex
from src.users.schemes import UserCreate
from sqlalchemy import select
from fastapi import HTTPException


async def check_pass(user_data: UserCreate, session=Depends(get_async_session)):
    query = select(User).where(User.username == user_data.username)
    result = await session.execute(query)

    if not pwd_contex.verify(user_data.password, result["hashed_password"]):
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    token: Token = Token(user_data=result["id"], access_token=uuid.uuid4())
    session.add(token)
    await session.commit()

    return {"access_token": token}


async def check_token_valid(token: str, session):
    query = select(Token).where(Token.access_token == token)
    result: Token = await session.scalar(query)

    if not result or datetime.now() > result.exp or result.use_num <= 0:
        if result:
            await session.delete(result)
            await session.commit()
        return False
    return True
