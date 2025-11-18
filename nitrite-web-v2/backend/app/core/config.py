from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    # Application
    APP_NAME: str = "NiTriTe API"
    APP_VERSION: str = "2.0.0"
    DEBUG: bool = True
    SECRET_KEY: str = "your-super-secret-key-change-in-production"

    # Database
    DATABASE_URL: str = "postgresql+asyncpg://nitrite:password@postgres:5432/nitrite"
    DATABASE_POOL_SIZE: int = 20
    DATABASE_MAX_OVERFLOW: int = 10

    # Redis
    REDIS_URL: str = "redis://redis:6379/0"

    # Celery
    CELERY_BROKER_URL: str = "redis://redis:6379/1"
    CELERY_RESULT_BACKEND: str = "redis://redis:6379/2"

    # CORS
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://localhost:80",
    ]

    # Auth
    JWT_SECRET_KEY: str = "your-jwt-secret-key"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # App Settings
    MAX_CONCURRENT_DOWNLOADS: int = 3
    DOWNLOAD_TIMEOUT: int = 300
    INSTALL_TIMEOUT: int = 600

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
