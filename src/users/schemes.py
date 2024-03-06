from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    id: int
    access_token: str
    user_id: int
