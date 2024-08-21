from pydantic import BaseModel

from app.schema.user_schema import User


class SignUp(BaseModel):
    username: str
    email: str
    password: str


class SignIn(BaseModel):
    email: str
    password: str


class SignInResponse(BaseModel):
    user_info: User
    access_token: str
    refresh_token: str
