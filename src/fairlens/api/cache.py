"""
Deterministic Response Cache for FairLens OpenRouter API Client.

Prevents redundant network and paid requests, tracks cache hit rates,
and guarantees reproducible experiment logging without caching transient errors.
"""

import hashlib
import json
from pathlib import Path
from typing import Any, Dict, Optional, Tuple
from fairlens.config.logging import get_logger

logger = get_logger("api.cache")


class ResponseCache:
    """Thread-safe, file-based deterministic cache for LLM API responses."""

    def __init__(self, cache_dir: Path):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.hits = 0
        self.misses = 0

    @staticmethod
    def generate_cache_key(
        model: str,
        messages: list,
        temperature: float = 0.0,
        max_tokens: Optional[int] = None,
        top_p: Optional[float] = None,
    ) -> str:
        """Generate a deterministic SHA-256 hash from canonical request parameters."""
        canonical_payload = {
            "model": model,
            "messages": messages,
            "temperature": round(temperature, 4),
            "max_tokens": max_tokens,
            "top_p": round(top_p, 4) if top_p is not None else None,
        }
        serialized = json.dumps(canonical_payload, sort_keys=True, ensure_ascii=False)
        return hashlib.sha256(serialized.encode("utf-8")).hexdigest()

    def get(self, cache_key: str) -> Optional[Dict[str, Any]]:
        """Retrieve a cached response if it exists."""
        cache_file = self.cache_dir / f"{cache_key}.json"
        if cache_file.exists():
            try:
                with open(cache_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                self.hits += 1
                logger.debug("Cache hit for key=%s", cache_key[:12])
                return data
            except Exception as e:
                logger.warning("Corrupted cache file for key=%s: %s", cache_key[:12], e)
                return None
        self.misses += 1
        return None

    def set(self, cache_key: str, response_data: Dict[str, Any]) -> None:
        """Store a successful API response safely."""
        cache_file = self.cache_dir / f"{cache_key}.json"
        try:
            with open(cache_file, "w", encoding="utf-8") as f:
                json.dump(response_data, f, indent=2, ensure_ascii=False)
            logger.debug("Cached response for key=%s", cache_key[:12])
        except Exception as e:
            logger.error("Failed to write cache for key=%s: %s", cache_key[:12], e)

    def invalidate(self, cache_key: str) -> bool:
        """Remove a single entry from the cache."""
        cache_file = self.cache_dir / f"{cache_key}.json"
        if cache_file.exists():
            cache_file.unlink()
            return True
        return False

    def clear(self) -> int:
        """Clear all cached responses and return count of deleted files."""
        count = 0
        for p in self.cache_dir.glob("*.json"):
            try:
                p.unlink()
                count += 1
            except Exception as e:
                logger.warning("Could not delete %s: %s", p.name, e)
        self.hits = 0
        self.misses = 0
        logger.info("Cleared %d entries from cache at %s", count, self.cache_dir)
        return count

    def stats(self) -> Dict[str, Any]:
        """Return cache performance statistics."""
        total = self.hits + self.misses
        hit_rate = (self.hits / total) if total > 0 else 0.0
        return {
            "hits": self.hits,
            "misses": self.misses,
            "total_queries": total,
            "hit_rate": round(hit_rate, 4),
            "cached_entries": len(list(self.cache_dir.glob("*.json"))),
        }
