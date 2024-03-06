from sqlalchemy import Column, Integer, String, MetaData, Table, ForeignKey, TIMESTAMP
from datetime import timedelta, datetime
from src.database import Base

metadata = MetaData()

user = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("username", String, unique=True, nullable=False),
    Column("hashed_password", String, nullable=False),
    Column("balance", Integer, default=1000, nullable=False)
)

Token = Table(
    "tokens",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("access_token", String, unique=True, nullable=False),
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("exp", TIMESTAMP, default=datetime.now() + timedelta(minutes=60)),
    Column("use_num", Integer, default=1)
)


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    balance = Column(Integer, default=1000, nullable=False)

    # this_token = relationship("Token", back_populates="users")


class Token(Base):
    __tablename__ = "tokens"
    id = Column(Integer, primary_key=True, index=True)
    access_token = Column(String, unique=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    exp = Column(TIMESTAMP, default=datetime.now() + timedelta(minutes=60))
    use_num = Column(Integer, default=1)

    # this_user = relationship("User", back_populates="tokens")
