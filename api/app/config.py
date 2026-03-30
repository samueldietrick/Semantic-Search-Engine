from __future__ import annotations

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    qdrant_url: str = "http://localhost:6333"
    collection_name: str = "items"
    embedding_model: str = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    semantic_weight: float = 0.7
    lexical_weight: float = 0.3
    qdrant_prefetch: int = 80
    default_limit: int = 10
    max_limit: int = 50
    cache_ttl_seconds: int = 120
    cache_max_entries: int = 256


@lru_cache
def get_settings() -> Settings:
    return Settings()
