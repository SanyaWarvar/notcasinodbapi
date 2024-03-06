from typing import List
from urllib.request import Request

from fastapi import APIRouter, Depends
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_async_session
from src.auth.models import user


router = APIRouter(
    prefix="/users",
    tags=["User"]
)


@router.get("/")
async def get_users(session: AsyncSession = Depends(get_async_session)):
    query = select(user.c.id, user.c.name, user.c.balance)
    result = await session.execute(query)
    return result.mappings().all()
