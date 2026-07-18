# This module centralizes configuration values for the application.
# Keeping settings in one place makes the project easier to maintain and deploy in Docker.

import os
from pathlib import Path


class Settings:
    # We read application metadata from environment variables when available.
    app_name: str = os.getenv("APP_NAME", "Smart Buddy Study")
    app_version: str = os.getenv("APP_VERSION", "0.1.0")

    # We keep the data directory configurable so the persistence path can be changed easily.
    data_dir: Path = Path(os.getenv("DATA_DIR", "data"))
    vector_db_dir: Path = Path(os.getenv("VECTOR_DB_DIR", str(data_dir / "chroma")))

    # We expose a default topic list to seed the initial knowledge base with study material.
    default_topics: tuple[str, ...] = (
        "python",
        "algorithms",
        "data structures",
        "machine learning",
        "study habits",
    )


settings = Settings()
