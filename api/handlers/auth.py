from typing import Dict
import re

from fastapi import Response
from fastapi.routing import APIRouter

from api.schemas.auth import UserAuth, UserRegister
from common.exceptions import (
    IncorrectEmailOrPasswordsException,
    RegexEmailException,
    RegexPasswordException,
    RegexUserNameException,
    UnknownException,
    UserAlreadyExistsException,
)
from common.regex import EMAIL_PATTERN, PASSWORD_PATTERN, USERNAME_PATTERN
from database.users.auth import (
    authenticate_user,
    create_access_token,
    get_password_hash,
)
from database.users.repository import UserRepository

router = APIRouter(tags=["Authentication"], prefix="/auth")


@router.post(
    "/register",
    summary="Регистрация нового пользователя",
    description="Создает новую учетную запись пользователя.\
Требуется указать имя пользователя (никнейм), электронную почту и пароль.",
)
async def register_user(user_data: UserRegister) -> Dict:
    existing_user = await UserRepository.find_one_or_none(email=user_data.email)
    if existing_user:
        raise UserAlreadyExistsException

    if not EMAIL_PATTERN.match(user_data.email):
        raise RegexEmailException
    if not USERNAME_PATTERN.match(user_data.username):
        raise RegexUserNameException
    if not PASSWORD_PATTERN.match(user_data.password):
        raise RegexPasswordException

    hashed_password = get_password_hash(user_data.password)

    try:
        await UserRepository.add(
            username=user_data.username,
            email=user_data.email,
            hashed_password=hashed_password,
        )
    except Exception:
        raise UnknownException

    return {"detail": "Успешно"}


@router.post(
    "/login",
    summary="Авторизация пользователя",
    description="Авторизует пользователя, проверяя его почту и пароль.\
Возвращает идентификатор пользователя и токен доступа.",
)
async def login_user(response: Response, user_data: UserAuth):
    if not EMAIL_PATTERN.match(user_data.email):
        raise RegexEmailException
    if not PASSWORD_PATTERN.match(user_data.password):
        raise RegexPasswordException

    user = await authenticate_user(user_data.email, user_data.password)

    if not user:
        raise IncorrectEmailOrPasswordsException

    access_token, refresh_token = create_access_token({"sub": str(user.id)})

    response.set_cookie("user_token", access_token, httponly=True)
    response.set_cookie("refresh_token", refresh_token, httponly=True)

    return {
        "user_id": user.id,
        "access_token": access_token,
        "refresh_token": refresh_token,
    }


@router.post(
    "/logout",
    summary="Выход из системы",
    description="Выходит из текущей учетной записи пользователя, удаляя токен авторизации.",
)
async def logout_user(response: Response) -> Dict:
    response.delete_cookie("user_token")
    response.delete_cookie("refresh_token")
    return {"detail": "Успешно"}
