from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL:str
    ACCESS_TOKEN_TIME: int
    ALGORITHM: str
    REFRESH_TOKEN_TIME: int
    SECRET_KEY: str
    REDIS_URL: str
    CELERY_BROKER_URL: str
    CELERY_RESULT_BACKEND: str
    EMAIL_FROM: str
    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_USERNAME: str
    SMTP_PASSWORD: str
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    AWS_REGION: str
    AWS_S3_BUCKET: str

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )

settings = Settings()

DATABASE_URL = settings.DATABASE_URL
ACCESS_TOKEN_TIME = settings.ACCESS_TOKEN_TIME
ALGORITHM = settings.ALGORITHM
REFRESH_TOKEN_TIME = settings.REFRESH_TOKEN_TIME
SECRET_KEY = settings.SECRET_KEY
REDIS_URL= settings.REDIS_URL
CELERY_BROKER_URL= settings.CELERY_BROKER_URL
CELERY_RESULT_BACKEND= settings.CELERY_RESULT_BACKEND
EMAIL_FROM = settings.EMAIL_FROM
SMTP_HOST = settings.SMTP_HOST
SMTP_PORT = settings.SMTP_PORT
SMTP_USERNAME = settings.SMTP_USERNAME
SMTP_PASSWORD = settings.SMTP_PASSWORD
AWS_ACCESS_KEY_ID = settings.AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY = settings.AWS_SECRET_ACCESS_KEY
AWS_REGION = settings.AWS_REGION
AWS_S3_BUCKET = settings.AWS_S3_BUCKET