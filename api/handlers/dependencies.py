from datetime import datetime
from typing import Optional

from fastapi import Depends, Request
from jose import JWTError, jwt

from common.exceptions import (
    IncorrectTokenFormatExpressionException,
    TokenAbsentException,
    TokenExpiredException,
)
from common.settings import settings
from database.users.repository import UserRepository


def get_token(request: Request):
    token = request.cookies.get("multigrab_user_token")
    if not token:
        return None
    return token


async def get_current_user(token: str = Depends(get_token)):
    if not token:
        raise TokenAbsentException
    try:
        payload = jwt.decode(token, settings.secret_key, settings.algorithm)
    except JWTError:
        raise IncorrectTokenFormatExpressionException
    expire: str = payload.get("exp")
    if (not expire) or (int(expire) < datetime.now().timestamp()):
        raise TokenExpiredException
    user_id: str = payload.get("sub")
    if not user_id:
        raise IncorrectTokenFormatExpressionException
    user = await UserRepository.find_by_id(int(user_id))
    if not user:
        raise IncorrectTokenFormatExpressionException
    return user


async def get_current_user_optional(token: Optional[str] = Depends(get_token)):
    if not token:
        return None
    try:
        payload = jwt.decode(token, settings.secret_key, settings.algorithm)
    except JWTError:
        raise IncorrectTokenFormatExpressionException
    expire = payload.get("exp")
    if (not expire) or (int(expire) < datetime.now().timestamp()):
        raise TokenExpiredException
    user_id = payload.get("sub")
    if not user_id:
        raise IncorrectTokenFormatExpressionException
    user = await UserRepository.find_by_id(int(user_id))
    if not user:
        raise IncorrectTokenFormatExpressionException
    return user
