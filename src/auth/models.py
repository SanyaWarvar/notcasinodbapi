from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import MetaData, Integer, String, Table, Column, Boolean
from src.database import Base

metadata = MetaData()

users = Table(
    "user",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
    Column("balance", Integer, default=1000),
    Column("email", String),
    Column("hashed_password", String, nullable=False),
    Column("salt", String, nullable=False),
    Column("is_active", Boolean, default=True, nullable=False),
    Column("is_superuser", Boolean, default=False, nullable=False),
    Column("is_verified", Boolean, default=False, nullable=False)
)


class User(SQLAlchemyBaseUserTable[int], Base):
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    balance = Column(Integer, default=1000)
    salt = Column(String, nullable=False)
