from pydantic import BaseModel, EmailStr


class UserAuth(BaseModel):
    username: str
    email: EmailStr
    password: str
