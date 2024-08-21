import pathlib
from typing import Literal

import environ
from pydantic import Field
from pydantic_settings import BaseSettings


BASE_DIR = pathlib.Path(__file__).parent.parent.parent
env = environ.Env()
environ.Env.read_env(str(BASE_DIR.joinpath(".env")))


class Configs(BaseSettings):
    mode: Literal["DEV", "TEST", "PROD"] = Field(env("MODE"))
    debug: bool = Field(default=False)

    title: str = env("TITLE")

    # tokens
    youtube_token: str = env("YOUTUBE_TOKEN")
    vk_token: str = env("VK_TOKEN")
    sentry_token: str = env("SENTRY_TOKEN")

    # db
    db_username: str = env("DB_USER")
    db_password: str = env("DB_PASSWORD")
    db_host: str = env("DB_HOST")
    db_port: str = env("DB_PORT")
    db_name: str = env("DB_NAME")

    # test db
    test_db_username: str = env("TEST_DB_USER")
    test_db_password: str = env("TEST_DB_PASSWORD")
    test_db_host: str = env("TEST_DB_HOST")
    test_db_port: str = env("TEST_DB_PORT")
    test_db_name: str = env("TEST_DB_NAME")

    # redis
    redis_host: str = env("REDIS_HOST")
    redis_port: str = env("REDIS_PORT")

    # auth
    secret_key: str = env("SECRET_KEY")
    algorithm: str = env("ALGORITHM")
    user_token_expire: int = env("USER_TOKEN_EXPIRE")
    refresh_token_expire: int = env("REFRESH_TOKEN_EXPIRE")

    def __init__(self, **values):
        super().__init__(**values)
        if self.mode == "PROD":
            self.debug = False
        else:
            self.debug = True


configs = Configs()
