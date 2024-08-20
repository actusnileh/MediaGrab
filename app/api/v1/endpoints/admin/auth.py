from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request

from app.core.dependencies import get_current_user
from app.core.security import create_access_token
from app.repository.user_repository import UserRepository
from app.services.auth_service import AuthService


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        email, password = form["username"], form["password"]

        user = await AuthService(UserRepository).sign_in_admin(email, password)

        if user:
            access_token = create_access_token({"sub": str(user.id)})
            request.session.update({"token": access_token})

        return True

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get("token")
        if not token:
            return False
        user = await get_current_user(None, token)
        if not user:
            return False
        return True


authentication_backend = AdminAuth(secret_key="...")
