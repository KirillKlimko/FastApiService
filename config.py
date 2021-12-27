from dotenv import load_dotenv
from passlib.context import CryptContext
from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    DB_USER: str = Field(..., env='DB_USER')
    DB_PASSWORD: str = Field(..., env='DB_PASSWORD')
    DB_HOST: str = Field(..., env='DB_HOST')
    DB_NAME: str = Field(..., env='DB_NAME')

    SECRET_KEY: str = Field(..., env='SECRET_KEY')
    ALGORITHM: str = Field(..., env='ALGORITHM')
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(
        ..., env='ACCESS_TOKEN_EXPIRE_MINUTES'
    )

    @property
    def database_url(self):
        return f'postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}/{self.DB_NAME}'

    @property
    def pwd_context(self):
        pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
        return pwd_context


load_dotenv()
settings = Settings()
