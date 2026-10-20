"""
Central Configuration System for FairLens.

Handles environment variables, default settings, budget limits,
and secret masking in compliance with FairLens security guidelines.
"""

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

# Optional dotenv loading if python-dotenv is available
try:
    from dotenv import load_dotenv
    # Load .env only if it exists, without failing if missing
    env_path = Path(".env")
    if env_path.exists():
        load_dotenv(dotenv_path=env_path)
except ImportError:
    pass


@dataclass
class Settings:
    """FairLens central application settings with validation and secret masking."""

    # Application Environment
    env: str = field(default_factory=lambda: os.getenv("FAIRLENS_ENV", "development"))
    log_level: str = field(default_factory=lambda: os.getenv("FAIRLENS_LOG_LEVEL", "INFO").upper())
    offline_mode: bool = field(
        default_factory=lambda: os.getenv("FAIRLENS_OFFLINE_MODE", "true").lower() in ("true", "1", "yes")
    )

    # OpenRouter API Configuration
    openrouter_api_key: Optional[str] = field(
        default_factory=lambda: os.getenv("OPENROUTER_API_KEY") or None
    )
    openrouter_endpoint: str = field(
        default_factory=lambda: os.getenv(
            "OPENROUTER_ENDPOINT", "https://openrouter.ai/api/v1/chat/completions"
        )
    )
    openrouter_model: str = field(
        default_factory=lambda: os.getenv(
            "OPENROUTER_MODEL", "nvidia/nemotron-3-ultra-550b-a55b"
        )
    )
    openrouter_timeout_seconds: int = field(
        default_factory=lambda: int(os.getenv("OPENROUTER_TIMEOUT_SECONDS", "60"))
    )
    openrouter_max_retries: int = field(
        default_factory=lambda: int(os.getenv("OPENROUTER_MAX_RETRIES", "3"))
    )
    openrouter_cache_dir: Path = field(
        default_factory=lambda: Path(os.getenv("OPENROUTER_CACHE_DIR", ".fairlens_cache/openrouter"))
    )

    # Cost Estimation & Spending Limits (USD)
    max_spend_usd: float = field(
        default_factory=lambda: float(os.getenv("FAIRLENS_MAX_SPEND_USD", "5.00"))
    )
    warn_spend_usd: float = field(
        default_factory=lambda: float(os.getenv("FAIRLENS_WARN_SPEND_USD", "2.00"))
    )
    # Default reference prices per 1M tokens ($0.00 for verified free endpoint, with fallback estimates)
    input_price_per_m: float = field(
        default_factory=lambda: float(os.getenv("OPENROUTER_INPUT_PRICE_PER_M", "0.60"))
    )
    output_price_per_m: float = field(
        default_factory=lambda: float(os.getenv("OPENROUTER_OUTPUT_PRICE_PER_M", "3.60"))
    )

    # Discovery Engine Cache Settings
    discovery_cache_dir: Path = field(
        default_factory=lambda: Path(os.getenv("DISCOVERY_CACHE_DIR", ".fairlens_cache/discovery"))
    )
    discovery_cache_ttl_hours: int = field(
        default_factory=lambda: int(os.getenv("DISCOVERY_CACHE_TTL_HOURS", "24"))
    )

    # Optional Provider Tokens
    huggingface_token: Optional[str] = field(
        default_factory=lambda: os.getenv("HUGGINGFACE_TOKEN") or None
    )
    kaggle_username: Optional[str] = field(
        default_factory=lambda: os.getenv("KAGGLE_USERNAME") or None
    )
    kaggle_key: Optional[str] = field(
        default_factory=lambda: os.getenv("KAGGLE_KEY") or None
    )
    data_gov_api_key: Optional[str] = field(
        default_factory=lambda: os.getenv("DATA_GOV_API_KEY") or None
    )
    zenodo_access_token: Optional[str] = field(
        default_factory=lambda: os.getenv("ZENODO_ACCESS_TOKEN") or None
    )

    def __post_init__(self):
        """Validate configuration parameters."""
        if self.openrouter_timeout_seconds <= 0:
            raise ValueError(f"openrouter_timeout_seconds must be positive, got {self.openrouter_timeout_seconds}")
        if self.openrouter_max_retries < 0:
            raise ValueError(f"openrouter_max_retries cannot be negative, got {self.openrouter_max_retries}")
        if self.max_spend_usd < 0:
            raise ValueError(f"max_spend_usd cannot be negative, got {self.max_spend_usd}")
        if self.input_price_per_m < 0 or self.output_price_per_m < 0:
            raise ValueError("Token prices cannot be negative")

    def has_openrouter_credentials(self) -> bool:
        """Check if a valid, non-placeholder OpenRouter API key is configured."""
        if not self.openrouter_api_key:
            return False
        k = self.openrouter_api_key.strip()
        return bool(k and not k.startswith("your_") and not k.startswith("sk-placeholder"))

    def __repr__(self) -> str:
        """Safe string representation that masks all secrets."""
        def mask(val: Optional[str]) -> str:
            if not val:
                return "<not-set>"
            if len(val) <= 8:
                return "***"
            return f"{val[:4]}...{val[-4:]}"

        return (
            f"Settings(\n"
            f"  env={self.env},\n"
            f"  log_level={self.log_level},\n"
            f"  offline_mode={self.offline_mode},\n"
            f"  openrouter_model={self.openrouter_model},\n"
            f"  openrouter_api_key={mask(self.openrouter_api_key)},\n"
            f"  openrouter_timeout_seconds={self.openrouter_timeout_seconds},\n"
            f"  openrouter_max_retries={self.openrouter_max_retries},\n"
            f"  max_spend_usd={self.max_spend_usd},\n"
            f"  warn_spend_usd={self.warn_spend_usd},\n"
            f"  input_price_per_m={self.input_price_per_m},\n"
            f"  output_price_per_m={self.output_price_per_m},\n"
            f"  huggingface_token={mask(self.huggingface_token)},\n"
            f"  kaggle_key={mask(self.kaggle_key)},\n"
            f"  data_gov_api_key={mask(self.data_gov_api_key)},\n"
            f"  zenodo_access_token={mask(self.zenodo_access_token)}\n"
            f")"
        )


_cached_settings: Optional[Settings] = None


def get_settings(reload: bool = False) -> Settings:
    """Retrieve the singleton Settings instance."""
    global _cached_settings
    if _cached_settings is None or reload:
        _cached_settings = Settings()
    return _cached_settings
