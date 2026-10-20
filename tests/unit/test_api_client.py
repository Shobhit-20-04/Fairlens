"""
Unit tests for FairLens OpenRouter API client and deterministic response cache.
"""

import shutil
import tempfile
import unittest
from pathlib import Path

from fairlens.api.cache import ResponseCache
from fairlens.api.client import OpenRouterClient
from fairlens.api.exceptions import FairLensAuthenticationError
from fairlens.config.settings import Settings


class TestAPIClientAndCache(unittest.TestCase):
    """Test suite for OpenRouter client and local cache."""

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.cache_dir = Path(self.temp_dir) / "test_cache"
        self.cache = ResponseCache(self.cache_dir)
        self.settings = Settings(
            offline_mode=True,
            openrouter_cache_dir=self.cache_dir,
            openrouter_api_key=None,
        )
        self.client = OpenRouterClient(settings=self.settings, mock_mode=True, cache=self.cache)

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_mock_completion(self):
        """Verify mock completion returns valid structured dictionary."""
        messages = [{"role": "user", "content": "Assess Section 420 IPC applicability."}]
        resp = self.client.complete(messages, use_cache=False)

        self.assertIn("id", resp)
        self.assertIn("content", resp)
        self.assertIn("usage", resp)
        self.assertFalse(resp["cached"])
        self.assertEqual(resp["status_code"], 200)
        self.assertIn("Section 420 IPC", resp["content"])

    def test_cache_hit_and_miss(self):
        """Test deterministic cache hit on identical query and miss on perturbation."""
        messages1 = [{"role": "user", "content": "Case A: Contract dispute under Indian Law"}]
        messages2 = [{"role": "user", "content": "Case B: Perturbed Contract dispute under Indian Law"}]

        # First call -> Cache Miss, stored to cache
        resp1 = self.client.complete(messages1, use_cache=True)
        self.assertFalse(resp1["cached"])
        self.assertEqual(self.cache.misses, 1)
        self.assertEqual(self.cache.hits, 0)

        # Second call with identical payload -> Cache Hit
        resp1_cached = self.client.complete(messages1, use_cache=True)
        self.assertTrue(resp1_cached["cached"])
        self.assertEqual(self.cache.hits, 1)

        # Call with different payload -> Cache Miss
        resp2 = self.client.complete(messages2, use_cache=True)
        self.assertFalse(resp2["cached"])
        self.assertEqual(self.cache.misses, 2)

    def test_cache_invalidation_and_clear(self):
        """Test cache invalidation of specific keys and clearing entire cache."""
        messages = [{"role": "user", "content": "Test cache clear"}]
        key = ResponseCache.generate_cache_key("nvidia/nemotron-3-ultra-550b-a55b", messages)

        self.client.complete(messages, use_cache=True)
        self.assertTrue((self.cache_dir / f"{key}.json").exists())

        # Invalidate single key
        invalidated = self.cache.invalidate(key)
        self.assertTrue(invalidated)
        self.assertFalse((self.cache_dir / f"{key}.json").exists())

        # Populate again and clear
        self.client.complete(messages, use_cache=True)
        cleared_count = self.cache.clear()
        self.assertGreaterEqual(cleared_count, 1)
        self.assertEqual(len(list(self.cache_dir.glob("*.json"))), 0)

    def test_live_network_without_credentials_raises_auth_error(self):
        """Verify that live mode without API credentials raises FairLensAuthenticationError."""
        live_settings = Settings(
            offline_mode=False,
            openrouter_api_key=None,
            openrouter_cache_dir=self.cache_dir,
        )
        live_client = OpenRouterClient(settings=live_settings, mock_mode=False, cache=self.cache)

        with self.assertRaises(FairLensAuthenticationError):
            live_client.complete([{"role": "user", "content": "Live test"}], use_cache=False)


if __name__ == "__main__":
    unittest.main()
