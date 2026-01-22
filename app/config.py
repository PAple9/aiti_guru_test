from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    db_url: str = f"postgresql+asyncpg://admin:admin@localhost:5432/postgres"
    db_echo: bool = False


settings = Settings()
