from pydantic import BaseModel, Field
from sqlalchemy import MetaData, Integer, String, TIMESTAMP, Table, Column, JSON, Boolean


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
