from fastapi import (
    Depends,
    Response,
)
from fastapi.routing import APIRouter

from app.core.dependencies import get_current_user
from app.repository.user_repository import UserRepository
from app.schema.auth_schema import (
    SignIn,
    SignInResponse,
    SignUp,
)
from app.schema.user_schema import User
from app.services.auth_service import AuthService


router = APIRouter(tags=["Auth"], prefix="/auth")


@router.post("/sign-up", response_model=SignIn)
async def sign_up(user_info: SignUp):
    return await AuthService(UserRepository).sign_up(user_info)


@router.post("/sign-in", response_model=SignInResponse)
async def sign_in(response: Response, user_info: SignIn):
    return await AuthService(UserRepository).sign_in(response, user_info)


@router.get("/me", response_model=User)
async def me(current_user: User = Depends(get_current_user)):
    return current_user


@router.post("/logout")
async def logout(response: Response) -> dict:
    response.delete_cookie("user_token")
    response.delete_cookie("refresh_token")
    return {"detail": "OK"}
