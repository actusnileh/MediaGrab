from datetime import datetime, timedelta

from jose import jwt
from passlib.context import CryptContext

from app.core.config import configs
from app.core.exceptions import AuthError
from app.repository.user_repository import UserRepository


pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)


def create_refresh_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now() + timedelta(days=configs.refresh_token_expire)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, configs.secret_key, configs.algorithm)
    return encoded_jwt


def create_access_token(data: dict) -> dict:
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=configs.user_token_expire)
    to_encode.update({"exp": expire})
    access_token = jwt.encode(to_encode, configs.secret_key, configs.algorithm)
    refresh_token = create_refresh_token(data)
    return access_token, refresh_token


async def refresh_access_token(refresh_token: str) -> str:
    decoded_token = jwt.decode(
        refresh_token, configs.secret_key, algorithms=[configs.algorithm]
    )
    user_id = decoded_token.get("sub")
    if not user_id:
        raise AuthError("Token format not found")

    user = await UserRepository.find_by_id(int(user_id))
    if not user:
        raise AuthError("User not found")

    access_token_data = {"sub": str(user.id)}
    expire = datetime.now() + timedelta(minutes=configs.user_token_expire)
    access_token_data.update({"exp": expire})
    new_access_token = jwt.encode(
        access_token_data, configs.secret_key, configs.algorithm
    )

    return new_access_token
