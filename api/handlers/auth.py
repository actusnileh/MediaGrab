from fastapi import Depends, Response
from fastapi.routing import APIRouter
from api.handlers.dependencies import get_current_user
from common.exceptions import IncorrectEmailOrPasswordsException, UserAlreadyExistsException
from database.users.auth import (
    authenticate_user,
    create_access_token,
    get_password_hash,
)
from api.schemas.auth import UserAuth
from database.users.models import Users
from database.users.repository import UserRepository

router = APIRouter(tags=["Аутентификация"], prefix="/auth")


@router.post(
    "/register",
)
async def register_user(user_data: UserAuth):
    existing_user = await UserRepository.find_one_or_none(email=user_data.email)
    if existing_user:
        raise UserAlreadyExistsException
    hashed_password = get_password_hash(user_data.password)
    await UserRepository.add(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed_password,
    )


@router.post(
    "/login",
)
async def login_user(response: Response, user_data: UserAuth):
    user = await authenticate_user(user_data.email, user_data.password)
    if not user:
        raise IncorrectEmailOrPasswordsException
    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie("multigrab_user_token", access_token, httponly=True)
    return {"user_id": user.id, "access_token": access_token}


@router.post(
    "/logout",
)
async def logout_user(response: Response):
    response.delete_cookie("multigrab_user_token")


@router.get(
    "/about_user",
)
async def about_user(current_user: Users = Depends(get_current_user)):
    return current_user
