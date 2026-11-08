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
    
    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 1440

    # Browser origins allowed to call the API. Defaults to the frontend's local
    # dev server; set cors_origins in .env to add deployed addresses.
    cors_origins: list[str] = [
        "http://127.0.0.1:5500",
        "http://localhost:5500",
    ]

    # Where clients reach this API from the browser. Used to build absolute
    # URLs in responses, so a page served from another origin can load them.
    public_base_url: str = "http://localhost:8000"

    # Read values from the .env file.
    model_config = SettingsConfigDict(env_file=".env")


# Create one settings object. Other files import and use this.
settings = Settings()
