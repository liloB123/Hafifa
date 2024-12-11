from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str = 'postgresql://postgres:postgres@localhost/hafifa'

settings = Settings()