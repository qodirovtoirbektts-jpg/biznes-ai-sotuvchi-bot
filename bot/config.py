import os
from typing import List
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

DEFAULT_BOT_TOKEN = "9277921986:AAFriz9__oOJgaqrhNdW3NeIfjdg1jZcBM8"


class Settings(BaseSettings):
    BOT_TOKEN: str = Field(default_factory=lambda: os.getenv("BOT_TOKEN") or DEFAULT_BOT_TOKEN)
    ADMIN_IDS: List[int] = Field(default_factory=list)
    GEMINI_API_KEY: str = Field(default="")
    GEMINI_MODEL: str = Field(default="gemini-1.5-flash")
    DATABASE_URL: str = Field(default="sqlite+aiosqlite:///sotuvchi.db")
    STORE_NAME: str = Field(default="Biznes AI Do'koni")
    STORE_DESCRIPTION: str = Field(default="Universal internet do'koni va professional xizmatlar markazi")
    STORE_PHONE: str = Field(default="+998901234567")
    DELIVERY_PRICE: int = Field(default=20000)

    @field_validator("ADMIN_IDS", mode="before")
    @classmethod
    def parse_admin_ids(cls, v):
        if isinstance(v, str):
            if not v.strip():
                return []
            return [int(x.strip()) for x in v.split(",") if x.strip().isdigit()]
        if isinstance(v, int):
            return [v]
        return v or []

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()
