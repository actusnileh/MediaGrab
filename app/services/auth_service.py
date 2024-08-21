from app.core.exceptions import AuthError
from app.core.security.user_security import (
    create_access_token,
    get_password_hash,
    verify_password,
)
from app.repository.user_repository import UserRepository
from app.schema.auth_schema import (
    SignIn,
    SignInResponse,
    SignUp,
)


class AuthService:
    def __init__(self, user_repository: type[UserRepository]):
        self.user_repository = user_repository

    async def sign_up(self, sign_up_info: SignUp):
        existing_user = await self.user_repository.find_one_or_none(
            email=sign_up_info.email,
        )

        if existing_user:
            raise AuthError(detail="User already signed up")

        hashed_password = get_password_hash(sign_up_info.password)

        await self.user_repository.add(
            username=sign_up_info.username,
            email=sign_up_info.email,
            hashed_password=hashed_password,
        )
        return SignIn(email=sign_up_info.email, password=sign_up_info.password)

    async def sign_in(self, response, sign_in_info: SignIn):
        user = await self.user_repository.find_one_or_none(email=sign_in_info.email)

        if not user or not verify_password(sign_in_info.password, user.hashed_password):
            raise AuthError(detail="Incorrect email or password")

        if not user:
            raise AuthError(detail="Account does not exist")

        access_token, refresh_token = create_access_token({"sub": str(user.id)})

        response.set_cookie("user_token", access_token, httponly=True)
        response.set_cookie("refresh_token", refresh_token, httponly=True)
        return SignInResponse(
            user_info=user,
            access_token=access_token,
            refresh_token=refresh_token,
        )

    async def sign_in_admin(self, email: str, password: str):
        user = await UserRepository.find_one_or_none(email=email)
        if (
            not user
            or not verify_password(password, user.hashed_password)
            or user.is_admin is not True
        ):
            return None
        return user
