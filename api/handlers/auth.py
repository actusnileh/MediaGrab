from fastapi import HTTPException, Response, status
from fastapi.routing import APIRouter
from database.users.auth import (
    authenticate_user,
    create_access_token,
    get_password_hash,
)
from api.schemas.auth import UserAuth
from database.users.repository import UserRepository

router = APIRouter(tags=["Аутентификация"], prefix="/auth")


@router.post(
    "/register",
)
async def register_user(user_data: UserAuth):
    existing_user = await UserRepository.find_one_or_none(email=user_data.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
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
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    access_token = create_access_token({"sub": user.id})
    response.set_cookie("user_token", access_token, httponly=True)
    return {"user_id": user.id, "access_token": access_token}
