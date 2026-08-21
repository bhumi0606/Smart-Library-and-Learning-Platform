from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL:str
    ACCESS_TOKEN_TIME: int
    ALGORITHM: str
    REFRESH_TOKEN_TIME: int
    SECRET_KEY: str
    
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