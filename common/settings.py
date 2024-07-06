import pathlib
import environ

from pydantic_settings import BaseSettings

BASE_DIR = pathlib.Path(__file__).parent.parent
env = environ.Env()
environ.Env.read_env(str(BASE_DIR.joinpath(".env")))


class Settings(BaseSettings):
    debug: bool = env("DEBUG", default=False)
    title: str = env("TITLE")
    vk_token: str = env("VK_TOKEN")

    db_username: str = env("DB_USER")
    db_password: str = env("DB_PASSWORD")
    db_host: str = env("DB_HOST")
    db_port: str = env("DB_PORT")
    db_name: str = env("DB_NAME")


settings = Settings()
