from typing import Optional
from fastapi_users import schemas


class UserRead(schemas.BaseUser[int]):
    id: int
    name: str
    balance: int
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False

    class Config:
        orm_mode = True


class UserCreate(schemas.BaseUserCreate):
    name: str
    balance: int
    password: str
    salt: str
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False
