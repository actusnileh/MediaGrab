from pydantic import BaseModel, EmailStr
from app.schema.user_schema import User


class SignUp(BaseModel):
    username: str
    email: EmailStr
    password: str


class SignIn(BaseModel):
    email: EmailStr
    password: str


class SignInResponse(BaseModel):
    user_info: User
    access_token: str
    refresh_token: str
