from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


TRUE_VALUES = {"1", "true", "yes", "on"}


def _read_path_list(env_name: str) -> tuple[str, ...]:
    raw_value = os.getenv(env_name, "")
    if not raw_value:
        return ()

    return tuple(
        candidate.strip()
        for candidate in raw_value.split(os.pathsep)
        if candidate.strip()
    )


@dataclass(frozen=True)
class Settings:
    base_url: str = os.getenv("BASE_URL", "https://automationteststore.com/")
    browser: str = os.getenv("BROWSER", "chrome").lower()
    chrome_binary: str = os.getenv("CHROME_BINARY", "")
    chrome_binary_candidates: tuple[str, ...] = _read_path_list("CHROME_BINARY_CANDIDATES")
    headless: bool = os.getenv("HEADLESS", "true").lower() in TRUE_VALUES
    window_size: str = os.getenv("WINDOW_SIZE", "1662,934")
    explicit_wait: int = int(os.getenv("EXPLICIT_WAIT", "20"))
    page_load_timeout: int = int(os.getenv("PAGE_LOAD_TIMEOUT", "60"))
    random_seed: int = int(os.getenv("TEST_RANDOM_SEED", "20260419"))

    @property
    def project_root(self) -> Path:
        return Path(__file__).resolve().parent.parent


SETTINGS = Settings()
