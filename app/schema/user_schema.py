from pydantic import BaseModel


class User(BaseModel):
    username: str
    email: str

    class Config:
        from_attributes = True
