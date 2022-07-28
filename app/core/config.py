import os
from logging import config as logging_config
from dotenv import load_dotenv
from pydantic import BaseSettings

from core.logger import LOGGING

load_dotenv()

# Применяем настройки логирования
logging_config.dictConfig(LOGGING)


class Settings(BaseSettings):
    PROJECT_NAME = os.getenv('PROJECT_NAME')
    REDIS_HOST = os.getenv('REDIS_HOST')
    REDIS_PORT = int(os.getenv('REDIS_PORT'))

    INSTAGRAM_LOGIN = os.getenv("INSTAGRAM_LOGIN")
    INSTAGRAM_PASSWORD = os.getenv("INSTAGRAM_PASSWORD")

    class Config:
        env_file = ".env"


# Корень проекта
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

settings = Settings()
