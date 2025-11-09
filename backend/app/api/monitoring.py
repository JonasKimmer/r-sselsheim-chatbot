"""Monitoring and health check API endpoints."""

import logging
from fastapi import APIRouter
from typing import Dict, Any
from ..services.cache_service import get_cache
from ..services.metrics_service import get_metrics

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/monitoring", tags=["monitoring"])


@router.get("/health")
async def health_check() -> Dict[str, Any]:
    """
    Health check endpoint.

    Returns:
        System health status
    """
    metrics = get_metrics()
    cache = get_cache()

    health = metrics.get_system_health()
    cache_stats = cache.get_stats()

    return {
        "status": health["status"],
        "uptime": health["uptime_formatted"],
        "system": health,
        "cache": cache_stats
    }


@router.get("/metrics")
async def get_endpoint_metrics() -> Dict[str, Any]:
    """
    Get endpoint performance metrics.

    Returns:
        Endpoint statistics
    """
    metrics = get_metrics()

    return {
        "system": metrics.get_system_health(),
        "endpoints": metrics.get_endpoint_stats(),
        "cache": get_cache().get_stats()
    }


@router.get("/metrics/endpoints/{endpoint:path}")
async def get_specific_endpoint_metrics(endpoint: str) -> Dict[str, Any]:
    """
    Get metrics for specific endpoint.

    Args:
        endpoint: Endpoint path

    Returns:
        Endpoint statistics
    """
    metrics = get_metrics()
    stats = metrics.get_endpoint_stats(endpoint)

    if not stats:
        return {"error": "Endpoint not found or no metrics available"}

    return stats


@router.get("/metrics/requests/recent")
async def get_recent_requests(limit: int = 50) -> Dict[str, Any]:
    """
    Get recent request history.

    Args:
        limit: Maximum number of requests to return (default: 50)

    Returns:
        Recent request history
    """
    metrics = get_metrics()

    return {
        "requests": metrics.get_recent_requests(limit),
        "total": len(metrics.request_history)
    }


@router.get("/metrics/errors/recent")
async def get_recent_errors(limit: int = 20) -> Dict[str, Any]:
    """
    Get recent errors.

    Args:
        limit: Maximum number of errors to return (default: 20)

    Returns:
        Recent error history
    """
    metrics = get_metrics()

    return {
        "errors": metrics.get_recent_errors(limit),
        "total": len(metrics.error_history)
    }


@router.get("/cache/stats")
async def get_cache_stats() -> Dict[str, Any]:
    """
    Get cache statistics.

    Returns:
        Cache statistics including hit rate, size, etc.
    """
    cache = get_cache()

    return cache.get_stats()


@router.post("/cache/clear")
async def clear_cache() -> Dict[str, str]:
    """
    Clear all cached data.

    Returns:
        Success message
    """
    cache = get_cache()
    cache.clear()

    logger.info("Cache manually cleared via API")

    return {
        "status": "success",
        "message": "Cache cleared successfully"
    }


@router.post("/metrics/reset")
async def reset_metrics() -> Dict[str, str]:
    """
    Reset all metrics.

    Returns:
        Success message
    """
    metrics = get_metrics()
    metrics.reset_metrics()

    logger.info("Metrics manually reset via API")

    return {
        "status": "success",
        "message": "Metrics reset successfully"
    }
