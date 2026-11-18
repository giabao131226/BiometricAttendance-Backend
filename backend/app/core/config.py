from pydantic_settings import BaseSettings

class Setting(BaseSettings):
    DATABASE_URL: str
    model_config = {"env_file": ".env"}

setting = Setting()