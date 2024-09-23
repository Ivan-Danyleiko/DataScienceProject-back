from pathlib import Path
from pydantic import ConfigDict
from pydantic_settings import BaseSettings

env_file = Path(__file__).parent.parent.parent.parent / ".env"

class Settings(BaseSettings):
    sqlalchemy_database_url: str
    secret_key: str
    algorithm: str
    mail_username: str | None = None
    mail_password: str | None = None
    mail_from: str | None = None
    mail_from_name: str | None = None
    mail_port: int | None = None
    mail_server: str | None = None
    cors_origins: str | None = None
    # rate_limiter_times: int
    # rate_limiter_seconds: int

    model_config = ConfigDict(extra='ignore', env_file=env_file if env_file.exists() else None, env_file_encoding = "utf-8")

settings = Settings()
