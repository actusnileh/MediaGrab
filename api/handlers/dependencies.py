from datetime import datetime
from typing import Optional

from fastapi import Depends, Request, Response
from jose import JWTError, jwt

from common.exceptions import (
    IncorrectTokenFormatExpressionException,
    TokenExpiredException,
)
from common.settings import settings
from database.users.auth import refresh_access_token
from database.users.repository import UserRepository


def get_tokens(request: Request):
    user_token = request.cookies.get("user_token")
    refresh_token = request.cookies.get("refresh_token")
    if not user_token:
        return None
    return user_token, refresh_token


async def get_current_user(
    response: Response = None,
    tokens: tuple = Depends(get_tokens),
):
    user_token, refresh_token = tokens
    try:
        payload = jwt.decode(user_token, settings.secret_key, settings.algorithm)
    except JWTError:
        try:
            new_access_token = await refresh_access_token(refresh_token)
            if response:
                response.set_cookie("user_token", new_access_token, httponly=True)
            return await get_current_user(response, (new_access_token, refresh_token))
        except JWTError:
            raise TokenExpiredException
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


async def get_current_user_optional(
    response: Response,
    tokens: Optional[tuple] = Depends(get_tokens),
):
    if tokens is None:
        return None
    user_token, refresh_token = tokens
    try:
        payload = jwt.decode(user_token, settings.secret_key, settings.algorithm)
    except JWTError:
        try:
            new_access_token = await refresh_access_token(refresh_token)
            response.set_cookie("user_token", new_access_token, httponly=True)
            return await get_current_user(response, (new_access_token, refresh_token))
        except JWTError:
            raise TokenExpiredException
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
