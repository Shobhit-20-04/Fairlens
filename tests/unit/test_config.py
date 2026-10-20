"""
Unit tests for FairLens configuration and logging security.
"""

import logging
import unittest
from fairlens.config.logging import SecretMaskingFilter
from fairlens.config.settings import Settings


class TestSettings(unittest.TestCase):
    """Test suite for configuration validation and secret masking."""

    def test_default_settings(self):
        """Verify sensible default settings are populated."""
        s = Settings()
        self.assertEqual(s.env, "development")
        self.assertEqual(s.log_level, "INFO")
        self.assertEqual(s.openrouter_timeout_seconds, 60)
        self.assertEqual(s.openrouter_max_retries, 3)
        self.assertGreater(s.max_spend_usd, 0.0)

    def test_validation_errors(self):
        """Ensure invalid settings raise descriptive ValueError."""
        with self.assertRaises(ValueError):
            Settings(openrouter_timeout_seconds=-5)

        with self.assertRaises(ValueError):
            Settings(openrouter_max_retries=-1)

        with self.assertRaises(ValueError):
            Settings(max_spend_usd=-10.0)

        with self.assertRaises(ValueError):
            Settings(input_price_per_m=-0.5)

    def test_secret_masking_in_repr(self):
        """Ensure secrets are never printed in plaintext repr."""
        raw_key = "sk-ant-api03-abcdef1234567890abcdef1234567890"
        s = Settings(openrouter_api_key=raw_key, huggingface_token="hf_secret_token_12345")
        representation = repr(s)

        self.assertNotIn(raw_key, representation)
        self.assertIn("sk-a...7890", representation)
        self.assertNotIn("hf_secret_token_12345", representation)

    def test_secret_masking_filter(self):
        """Verify the logging filter scrubs sensitive tokens."""
        filt = SecretMaskingFilter()
        record = logging.LogRecord(
            name="test",
            level=logging.INFO,
            pathname="",
            lineno=0,
            msg="Sending request with Bearer abcdef1234567890 and key sk-1234567890abcdef",
            args=(),
            exc_info=None,
        )
        filt.filter(record)
        self.assertNotIn("abcdef1234567890", record.msg)
        self.assertNotIn("sk-1234567890abcdef", record.msg)
        self.assertIn("[REDACTED_SECRET]", record.msg)

    def test_has_openrouter_credentials(self):
        """Test credential detection logic."""
        s_none = Settings(openrouter_api_key=None)
        self.assertFalse(s_none.has_openrouter_credentials())

        s_placeholder = Settings(openrouter_api_key="your_openrouter_api_key_here")
        self.assertFalse(s_placeholder.has_openrouter_credentials())

        s_valid = Settings(openrouter_api_key="sk-or-v1-abcdef1234567890")
        self.assertTrue(s_valid.has_openrouter_credentials())


if __name__ == "__main__":
    unittest.main()
