from datetime import datetime, timedelta

from jose import jwt
from passlib.context import CryptContext
from pydantic import EmailStr

from common.exceptions import (
    IncorrectTokenFormatExpressionException,
    TokenAbsentException,
)
from common.settings import settings
from database.users.repository import UserRepository

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
    expire = datetime.now() + timedelta(days=settings.refresh_token_expire)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, settings.algorithm)
    return encoded_jwt


def create_access_token(data: dict) -> dict:
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=settings.user_token_expire)
    to_encode.update({"exp": expire})
    access_token = jwt.encode(to_encode, settings.secret_key, settings.algorithm)
    refresh_token = create_refresh_token(data)
    return access_token, refresh_token


async def authenticate_user(email: EmailStr, password: str):
    user = await UserRepository.find_one_or_none(email=email)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user


async def authenticate_admin(email: EmailStr, password: str):
    user = await UserRepository.find_one_or_none(email=email)
    if (
        not user
        or not verify_password(password, user.hashed_password)
        or user.is_admin is not True
    ):
        return None
    return user


async def refresh_access_token(refresh_token: str) -> str:
    decoded_token = jwt.decode(
        refresh_token, settings.secret_key, algorithms=[settings.algorithm]
    )
    user_id = decoded_token.get("sub")
    if not user_id:
        raise IncorrectTokenFormatExpressionException

    user = await UserRepository.find_by_id(int(user_id))
    if not user:
        raise TokenAbsentException

    access_token_data = {"sub": str(user.id)}
    expire = datetime.now() + timedelta(minutes=settings.user_token_expire)
    access_token_data.update({"exp": expire})
    new_access_token = jwt.encode(
        access_token_data, settings.secret_key, settings.algorithm
    )

    return new_access_token
