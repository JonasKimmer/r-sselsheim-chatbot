"""Retry service for handling transient failures."""

import logging
import asyncio
from typing import Callable, Type, Tuple
from functools import wraps
import httpx

logger = logging.getLogger(__name__)


def async_retry(
    max_attempts: int = 3,
    delay_seconds: float = 1.0,
    backoff_factor: float = 2.0,
    exceptions: Tuple[Type[Exception], ...] = (httpx.HTTPError, asyncio.TimeoutError)
):
    """
    Decorator to retry async functions with exponential backoff.

    Args:
        max_attempts: Maximum number of retry attempts
        delay_seconds: Initial delay between retries in seconds
        backoff_factor: Multiplier for delay after each retry
        exceptions: Tuple of exceptions to catch and retry

    Returns:
        Decorated function

    Example:
        @async_retry(max_attempts=3, delay_seconds=1.0, backoff_factor=2.0)
        async def fetch_weather():
            async with httpx.AsyncClient() as client:
                response = await client.get("https://api.example.com/weather")
                return response.json()
    """
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            last_exception = None
            current_delay = delay_seconds

            for attempt in range(1, max_attempts + 1):
                try:
                    return await func(*args, **kwargs)

                except exceptions as e:
                    last_exception = e

                    if attempt == max_attempts:
                        logger.error(
                            f"Function {func.__name__} failed after {max_attempts} attempts: {e}"
                        )
                        raise

                    logger.warning(
                        f"Function {func.__name__} failed (attempt {attempt}/{max_attempts}): {e}. "
                        f"Retrying in {current_delay}s..."
                    )

                    await asyncio.sleep(current_delay)
                    current_delay *= backoff_factor

            # Should never reach here, but just in case
            if last_exception:
                raise last_exception

        return wrapper
    return decorator


class CircuitBreaker:
    """
    Circuit breaker pattern for API calls.

    Prevents cascading failures by stopping requests to failing services.
    """

    def __init__(
        self,
        failure_threshold: int = 5,
        recovery_timeout: int = 60,
        expected_exception: Type[Exception] = Exception
    ):
        """
        Initialize circuit breaker.

        Args:
            failure_threshold: Number of failures before opening circuit
            recovery_timeout: Seconds to wait before attempting recovery
            expected_exception: Exception type to track
        """
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.expected_exception = expected_exception

        self.failure_count = 0
        self.last_failure_time = None
        self.state = "closed"  # closed, open, half_open

    def call(self, func: Callable):
        """
        Decorator for circuit breaker pattern.

        Args:
            func: Function to wrap

        Returns:
            Decorated function
        """
        @wraps(func)
        async def wrapper(*args, **kwargs):
            if self.state == "open":
                if self._should_attempt_recovery():
                    self.state = "half_open"
                    logger.info(f"Circuit breaker for {func.__name__} is half-open (attempting recovery)")
                else:
                    raise Exception(
                        f"Circuit breaker is OPEN for {func.__name__}. "
                        f"Service unavailable. Retry after {self.recovery_timeout}s."
                    )

            try:
                result = await func(*args, **kwargs)

                # Success - reset failure count if in half-open state
                if self.state == "half_open":
                    self._on_success()
                    logger.info(f"Circuit breaker for {func.__name__} is now CLOSED (recovered)")

                return result

            except self.expected_exception as e:
                self._on_failure()
                logger.error(f"Circuit breaker recorded failure for {func.__name__}: {e}")
                raise

        return wrapper

    def _should_attempt_recovery(self) -> bool:
        """Check if enough time has passed to attempt recovery."""
        if self.last_failure_time is None:
            return True

        import time
        return (time.time() - self.last_failure_time) >= self.recovery_timeout

    def _on_success(self):
        """Handle successful call."""
        self.failure_count = 0
        self.state = "closed"

    def _on_failure(self):
        """Handle failed call."""
        self.failure_count += 1
        import time
        self.last_failure_time = time.time()

        if self.failure_count >= self.failure_threshold:
            self.state = "open"
            logger.error(
                f"Circuit breaker OPENED after {self.failure_count} failures. "
                f"Will retry in {self.recovery_timeout}s."
            )

    def reset(self):
        """Manually reset circuit breaker."""
        self.failure_count = 0
        self.last_failure_time = None
        self.state = "closed"
        logger.info("Circuit breaker manually reset to CLOSED state")
