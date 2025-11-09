"""Caching service for API responses."""

import logging
import hashlib
import json
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, Callable
from functools import wraps
import asyncio

logger = logging.getLogger(__name__)


class CacheService:
    """Simple in-memory TTL cache for API responses."""

    def __init__(self):
        """Initialize cache service."""
        self._cache: Dict[str, Dict[str, Any]] = {}
        self._stats = {
            "hits": 0,
            "misses": 0,
            "evictions": 0
        }

    def _generate_key(self, prefix: str, *args, **kwargs) -> str:
        """
        Generate cache key from function arguments.

        Args:
            prefix: Cache key prefix
            *args: Positional arguments
            **kwargs: Keyword arguments

        Returns:
            Cache key
        """
        # Create a deterministic string from args and kwargs
        key_data = {
            "args": args,
            "kwargs": sorted(kwargs.items())
        }
        key_str = json.dumps(key_data, sort_keys=True, default=str)
        key_hash = hashlib.md5(key_str.encode()).hexdigest()
        return f"{prefix}:{key_hash}"

    def get(self, key: str) -> Optional[Any]:
        """
        Get value from cache.

        Args:
            key: Cache key

        Returns:
            Cached value or None if not found/expired
        """
        if key not in self._cache:
            self._stats["misses"] += 1
            return None

        entry = self._cache[key]
        expires_at = entry["expires_at"]

        # Check if expired
        if datetime.now() > expires_at:
            del self._cache[key]
            self._stats["misses"] += 1
            self._stats["evictions"] += 1
            logger.debug(f"Cache expired: {key}")
            return None

        self._stats["hits"] += 1
        logger.debug(f"Cache hit: {key}")
        return entry["value"]

    def set(self, key: str, value: Any, ttl_seconds: int = 300):
        """
        Set value in cache.

        Args:
            key: Cache key
            value: Value to cache
            ttl_seconds: Time to live in seconds (default: 5 minutes)
        """
        expires_at = datetime.now() + timedelta(seconds=ttl_seconds)
        self._cache[key] = {
            "value": value,
            "expires_at": expires_at,
            "created_at": datetime.now()
        }
        logger.debug(f"Cache set: {key} (TTL: {ttl_seconds}s)")

    def delete(self, key: str):
        """
        Delete value from cache.

        Args:
            key: Cache key
        """
        if key in self._cache:
            del self._cache[key]
            logger.debug(f"Cache deleted: {key}")

    def clear(self):
        """Clear all cache entries."""
        self._cache.clear()
        logger.info("Cache cleared")

    def get_stats(self) -> Dict[str, int]:
        """
        Get cache statistics.

        Returns:
            Cache statistics
        """
        total_requests = self._stats["hits"] + self._stats["misses"]
        hit_rate = (self._stats["hits"] / total_requests * 100) if total_requests > 0 else 0

        return {
            **self._stats,
            "total_requests": total_requests,
            "hit_rate": round(hit_rate, 2),
            "cache_size": len(self._cache)
        }

    def cleanup_expired(self):
        """Remove all expired entries from cache."""
        now = datetime.now()
        expired_keys = [
            key for key, entry in self._cache.items()
            if now > entry["expires_at"]
        ]

        for key in expired_keys:
            del self._cache[key]
            self._stats["evictions"] += 1

        if expired_keys:
            logger.info(f"Cleaned up {len(expired_keys)} expired cache entries")


# Global cache instance
_cache = CacheService()


def get_cache() -> CacheService:
    """Get global cache instance."""
    return _cache


def cached(ttl_seconds: int = 300, key_prefix: str = "default"):
    """
    Decorator to cache async function results.

    Args:
        ttl_seconds: Time to live in seconds (default: 5 minutes)
        key_prefix: Cache key prefix

    Returns:
        Decorated function

    Example:
        @cached(ttl_seconds=600, key_prefix="weather")
        async def get_weather(lat, lon):
            return await fetch_weather_api(lat, lon)
    """
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            cache = get_cache()

            # Generate cache key
            cache_key = cache._generate_key(key_prefix, *args, **kwargs)

            # Try to get from cache
            cached_value = cache.get(cache_key)
            if cached_value is not None:
                logger.debug(f"Cache hit for {func.__name__}")
                return cached_value

            # Execute function
            logger.debug(f"Cache miss for {func.__name__}, executing...")
            result = await func(*args, **kwargs)

            # Store in cache
            cache.set(cache_key, result, ttl_seconds)

            return result

        return wrapper
    return decorator


# Background task to cleanup expired entries every 5 minutes
async def cleanup_task():
    """Background task to cleanup expired cache entries."""
    while True:
        await asyncio.sleep(300)  # 5 minutes
        get_cache().cleanup_expired()
