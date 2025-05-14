import os
import json
from typing import Optional
from pydantic import EmailStr, field_validator

from src.core.config.base_config import Settings
from src.models.users import Gender
from src.core.logger.logger import logger
from src.core.config.base_config import BASE_DIR

logger.debug(f"BASE_DIR: {BASE_DIR}")

# Определяем среду выполнения (используем более надежный способ)
is_docker = os.path.exists("/.dockerenv")
print(f"Определена среда: {'Docker' if is_docker else 'Локальная'}")

class DBConfig(Settings):
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: int = 567234
    POSTGRES_DB: str = "alphadb"
    POSTGRES_HOST: str = "db"  # Будет переопределено позже
    POSTGRES_PORT: int = 5432

    @property
    def DATABASE_URL(self) -> str:
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:"
            f"{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:"
            f"{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

class JWTConfig(Settings):
    SECRET_KEY: str = "1234567890"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    EMAIL_TOKEN_EXPIRE_DAYS: int = 7


class AdminConfig(Settings):
    ADMIN_PASSWORD: str = "admin"
    ADMIN_FULLNAME: str = "Admin User Ampss"
    ADMIN_AGE: int = 30
    ADMIN_GENDER: Gender = Gender.M
    ADMIN_EMAIL: str ="admin@example.com"

class RedisConfig(Settings):
    REDIS_HOST: str = "redis"  # Будет переопределено позже
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: Optional[str] = None
    REDIS_DB: int = 0

class CloudinaryConfig(Settings):
    CLOUDINARY_NAME: str = "your_cloud_name"
    CLOUDINARY_API_KEY: int = 1234567890
    CLOUDINARY_API_SECRET: str = "your_api_secret"


# Инициализация объектов конфигурации
admin_config = AdminConfig()
db_config = DBConfig()
jwt_config = JWTConfig()
redis_config = RedisConfig()
cloudinary_config = CloudinaryConfig()

# Настройка в зависимости от среды ПОСЛЕ инициализации объектов
if not is_docker:
    # Для локальной разработки
    db_config.POSTGRES_HOST = "localhost"
    redis_config.REDIS_HOST = "172.23.6.211"  # IP-адрес WSL2
    print(f"Локальная конфигурация: POSTGRES_HOST={db_config.POSTGRES_HOST}, REDIS_HOST={redis_config.REDIS_HOST}")

print(f"DBConfig: {db_config.DATABASE_URL}")