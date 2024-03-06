# from fastapi.security import APIKeyHeader
from passlib.context import CryptContext

pwd_contex = CryptContext(schemes=["bcrypt"], deprecated="auto")

# apikey_scheme = APIKeyHeader(name="Authorized")
