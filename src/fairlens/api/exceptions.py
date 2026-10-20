"""
Custom exceptions for FairLens API and execution layer.
"""

class FairLensError(Exception):
    """Base exception for all FairLens operations."""
    pass


class FairLensAPIError(FairLensError):
    """Raised when an external API call fails."""
    def __init__(self, message: str, status_code: int = 500, response_text: str = ""):
        super().__init__(f"API Error ({status_code}): {message}")
        self.status_code = status_code
        self.response_text = response_text


class FairLensAuthenticationError(FairLensAPIError):
    """Raised when API credentials are missing, invalid, or expired."""
    def __init__(self, message: str = "Missing or invalid API credentials", status_code: int = 401):
        super().__init__(message, status_code)


class FairLensRateLimitError(FairLensAPIError):
    """Raised when an API endpoint rate limit is exceeded."""
    def __init__(self, message: str = "Rate limit exceeded", retry_after: int = 60):
        super().__init__(f"{message} (retry after {retry_after}s)", status_code=429)
        self.retry_after = retry_after


class FairLensTimeoutError(FairLensAPIError):
    """Raised when an API request times out."""
    def __init__(self, message: str = "Request timed out"):
        super().__init__(message, status_code=408)


class FairLensBudgetExceededError(FairLensError):
    """Raised when estimated or actual API cost exceeds configured spending limit."""
    def __init__(self, estimated_cost: float, max_budget: float):
        super().__init__(
            f"Operation blocked: Projected cost (${estimated_cost:.4f}) exceeds configured budget limit (${max_budget:.2f})."
        )
        self.estimated_cost = estimated_cost
        self.max_budget = max_budget
