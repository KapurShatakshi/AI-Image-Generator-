from functools import lru_cache
from pathlib import Path
from pydantic import BaseSettings, Field

class Settings(BaseSettings):
    openai_api_key: str | None = Field(None, env="OPENAI_API_KEY")
    model_provider: str = Field("", env="MODEL_PROVIDER")
    sd_model: str = "stabilityai/stable-diffusion-2-1"
    output_dir: Path = Path.cwd() / "generated"
    class Config:
        env_file = Path(__file__).parent / ".env"

@lru_cache
def get_settings() -> Settings:
    s = Settings()
    s.output_dir.mkdir(exist_ok=True)
    return s
