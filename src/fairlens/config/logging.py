"""
Logging Configuration and Secret Redaction for FairLens.

Ensures that API keys, Bearer tokens, and sensitive prompt data
are never printed to logs or standard error.
"""

import logging
import re
from typing import Optional

# Regex pattern to match potential secrets like sk-..., Bearer tokens, or raw keys
SECRET_PATTERNS = [
    re.compile(r"sk-[a-zA-Z0-9\-_]{8,}", re.IGNORECASE),
    re.compile(r"gho_[a-zA-Z0-9\-_]{8,}", re.IGNORECASE),
    re.compile(r"(Bearer\s+)[a-zA-Z0-9\-_]{8,}", re.IGNORECASE),
    re.compile(r"((?:key|token|password|secret)[\s=:]+)[a-zA-Z0-9\-_]{8,}", re.IGNORECASE),
    re.compile(r"(api_key[\"']?\s*[:=]\s*[\"']?)[a-zA-Z0-9\-_]{8,}", re.IGNORECASE),
]


class SecretMaskingFilter(logging.Filter):
    """Logging filter that scrubs sensitive tokens from all log messages."""

    def filter(self, record: logging.LogRecord) -> bool:
        if isinstance(record.msg, str):
            record.msg = self.mask_text(record.msg)
        if record.args:
            if isinstance(record.args, dict):
                record.args = {k: self.mask_text(v) if isinstance(v, str) else v for k, v in record.args.items()}
            elif isinstance(record.args, (list, tuple)):
                record.args = tuple(self.mask_text(a) if isinstance(a, str) else a for a in record.args)
        return True

    @staticmethod
    def mask_text(text: str) -> str:
        """Replace matches of secret patterns with redacted placeholders."""
        # Replace sk- and gho- tokens directly
        text = re.sub(r"sk-[a-zA-Z0-9\-_]{8,}", "[REDACTED_SECRET]", text, flags=re.IGNORECASE)
        text = re.sub(r"gho_[a-zA-Z0-9\-_]{8,}", "[REDACTED_SECRET]", text, flags=re.IGNORECASE)
        # Replace Bearer tokens
        text = re.sub(r"(Bearer\s+)[a-zA-Z0-9\-_]{8,}", r"\1[REDACTED_SECRET]", text, flags=re.IGNORECASE)
        # Replace key= / token= / password= tokens
        text = re.sub(r"((?:key|token|password|secret)[\s=:]+)[a-zA-Z0-9\-_]{8,}", r"\1[REDACTED_SECRET]", text, flags=re.IGNORECASE)
        # Replace api_key in JSON / config
        text = re.sub(r"(api_key[\"']?\s*[:=]\s*[\"']?)[a-zA-Z0-9\-_]{8,}", r"\1[REDACTED_SECRET]", text, flags=re.IGNORECASE)
        return text


def setup_logging(level: str = "INFO", log_file: Optional[str] = None) -> None:
    """Configure root logging with formatting and secret masking."""
    numeric_level = getattr(logging, level.upper(), logging.INFO)
    formatter = logging.Formatter(
        fmt="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    root_logger = logging.getLogger("fairlens")
    root_logger.setLevel(numeric_level)
    root_logger.handlers.clear()

    # Stream Handler (stdout/stderr)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    stream_handler.addFilter(SecretMaskingFilter())
    root_logger.addHandler(stream_handler)

    if log_file:
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setFormatter(formatter)
        file_handler.addFilter(SecretMaskingFilter())
        root_logger.addHandler(file_handler)


def get_logger(name: str) -> logging.Logger:
    """Get a child logger under the 'fairlens' namespace."""
    if not name.startswith("fairlens"):
        name = f"fairlens.{name}"
    return logging.getLogger(name)
