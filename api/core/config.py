from functools import lru_cache
from pydantic_settings import BaseSettings

import settings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Book Service"
    VERSION: str = "1.0.0"

    DATABASE_URL: str = settings.ASYNC_REAL_DATABASE_URL
    TEST_DATABASE_URL: str = settings.TEST_DATABASE_URL

    APP_PORT: int = settings.APP_PORT

    SECRET_KEY_FOR_ACCESS: str = settings.SECRET_KEY_FOR_ACCESS
    ALGORITHM: str = settings.ALGORITHM

    ENABLE_ROLE_CHECK: bool = settings.ENABLE_ROLE_CHECK

@lru_cache()
def get_settings():
    return Settings()