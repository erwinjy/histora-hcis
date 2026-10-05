from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="HCIS_", env_file=".env", extra="ignore")
    app_version: str = "0.2.0"
    schema_version: str = "0001"
    workspace_root: Path = Path("./data")
    database_url: str = "sqlite:///./data/hcis.db"

settings = Settings()
