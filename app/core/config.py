# BaseSettings: a base class that can read values from the .env file.
# SettingsConfigDict: tells the settings class which file to read.
from pydantic_settings import BaseSettings, SettingsConfigDict

# Settings class: holds all config values read from the .env file.
class Settings(BaseSettings):
    db_host: str
    db_port: int
    db_user: str
    db_password: str = ""  # empty if no password is set
    db_name: str

    # Read values from the .env file.
    model_config = SettingsConfigDict(env_file=".env")


# Create one settings object. Other files import and use this.
settings = Settings()
