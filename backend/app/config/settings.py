"""Application configuration via environment variables."""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    openai_api_key: str = ""
    openai_model: str = "gpt-4o-mini"
    database_url: str = "sqlite+aiosqlite:///./ghosttrace.db"
    cors_origins: str = "http://localhost:3000"
    demo_mode: bool = False

    @property
    def cors_origin_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]

    @property
    def use_demo_fallback(self) -> bool:
        return self.demo_mode or not self.openai_api_key


@lru_cache
def get_settings() -> Settings:
    return Settings()
