from pathlib import Path
from pydantic import ConfigDict, validator
from pydantic_settings import BaseSettings

env_file = Path(__file__).parent.parent.parent.parent / ".env"

class Settings(BaseSettings):
    sqlalchemy_database_url: str
    secret_key: str
    algorithm: str
    mail_username: str
    mail_password: str
    mail_from: str
    mail_from_name: str
    mail_port: int
    mail_server: str
    cors_origins: str

    @validator('mail_port', pre=True)
    def parse_mail_port(cls, v):
        if isinstance(v, int):
            return v
        try:
            return int(v)
        except ValueError:
            raise ValueError("MAIL_PORT must be a valid integer")

    model_config = ConfigDict(extra='ignore', env_file=env_file if env_file.exists() else None, env_file_encoding = "utf-8")

settings = Settings()