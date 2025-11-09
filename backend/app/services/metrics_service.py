"""Monitoring and metrics service."""

import logging
import time
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from collections import defaultdict, deque

logger = logging.getLogger(__name__)


class MetricsService:
    """Service for collecting and reporting application metrics."""

    def __init__(self, max_history: int = 1000):
        """
        Initialize metrics service.

        Args:
            max_history: Maximum number of metrics to keep in history
        """
        self.max_history = max_history

        # API endpoint metrics
        self.endpoint_metrics = defaultdict(lambda: {
            "count": 0,
            "total_time": 0.0,
            "min_time": float('inf'),
            "max_time": 0.0,
            "errors": 0,
            "last_called": None
        })

        # Request history (last N requests)
        self.request_history = deque(maxlen=max_history)

        # Error tracking
        self.error_history = deque(maxlen=100)

        # System start time
        self.start_time = datetime.now()

    def record_request(
        self,
        endpoint: str,
        duration_ms: float,
        status_code: int,
        error: Optional[str] = None
    ):
        """
        Record a request metric.

        Args:
            endpoint: API endpoint path
            duration_ms: Request duration in milliseconds
            status_code: HTTP status code
            error: Error message if request failed
        """
        metrics = self.endpoint_metrics[endpoint]

        # Update counters
        metrics["count"] += 1
        metrics["total_time"] += duration_ms
        metrics["min_time"] = min(metrics["min_time"], duration_ms)
        metrics["max_time"] = max(metrics["max_time"], duration_ms)
        metrics["last_called"] = datetime.now()

        if status_code >= 400 or error:
            metrics["errors"] += 1

        # Add to request history
        self.request_history.append({
            "timestamp": datetime.now(),
            "endpoint": endpoint,
            "duration_ms": round(duration_ms, 2),
            "status_code": status_code,
            "error": error
        })

        # Track errors separately
        if error:
            self.error_history.append({
                "timestamp": datetime.now(),
                "endpoint": endpoint,
                "error": error,
                "status_code": status_code
            })

            logger.warning(f"Error on {endpoint}: {error}")

    def get_endpoint_stats(self, endpoint: Optional[str] = None) -> Dict[str, Any]:
        """
        Get statistics for endpoint(s).

        Args:
            endpoint: Specific endpoint or None for all

        Returns:
            Endpoint statistics
        """
        if endpoint:
            metrics = self.endpoint_metrics.get(endpoint)
            if not metrics:
                return {}

            return self._format_endpoint_metrics(endpoint, metrics)

        # Return all endpoints
        return {
            endpoint: self._format_endpoint_metrics(endpoint, metrics)
            for endpoint, metrics in self.endpoint_metrics.items()
        }

    def _format_endpoint_metrics(self, endpoint: str, metrics: Dict) -> Dict[str, Any]:
        """Format endpoint metrics for output."""
        count = metrics["count"]
        avg_time = metrics["total_time"] / count if count > 0 else 0

        return {
            "endpoint": endpoint,
            "total_requests": count,
            "total_errors": metrics["errors"],
            "error_rate": round(metrics["errors"] / count * 100, 2) if count > 0 else 0,
            "avg_response_time_ms": round(avg_time, 2),
            "min_response_time_ms": round(metrics["min_time"], 2) if metrics["min_time"] != float('inf') else 0,
            "max_response_time_ms": round(metrics["max_time"], 2),
            "last_called": metrics["last_called"].isoformat() if metrics["last_called"] else None
        }

    def get_recent_requests(self, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Get recent request history.

        Args:
            limit: Maximum number of requests to return

        Returns:
            Recent request history
        """
        recent = list(self.request_history)[-limit:]
        return [
            {
                **req,
                "timestamp": req["timestamp"].isoformat()
            }
            for req in reversed(recent)
        ]

    def get_recent_errors(self, limit: int = 20) -> List[Dict[str, Any]]:
        """
        Get recent errors.

        Args:
            limit: Maximum number of errors to return

        Returns:
            Recent error history
        """
        recent = list(self.error_history)[-limit:]
        return [
            {
                **err,
                "timestamp": err["timestamp"].isoformat()
            }
            for err in reversed(recent)
        ]

    def get_system_health(self) -> Dict[str, Any]:
        """
        Get overall system health metrics.

        Returns:
            System health information
        """
        total_requests = sum(m["count"] for m in self.endpoint_metrics.values())
        total_errors = sum(m["errors"] for m in self.endpoint_metrics.values())

        uptime = datetime.now() - self.start_time
        uptime_seconds = int(uptime.total_seconds())

        return {
            "status": "healthy" if total_errors / max(total_requests, 1) < 0.1 else "degraded",
            "uptime_seconds": uptime_seconds,
            "uptime_formatted": str(uptime).split('.')[0],
            "total_requests": total_requests,
            "total_errors": total_errors,
            "error_rate": round(total_errors / max(total_requests, 1) * 100, 2),
            "endpoints_tracked": len(self.endpoint_metrics),
            "start_time": self.start_time.isoformat()
        }

    def reset_metrics(self):
        """Reset all metrics."""
        self.endpoint_metrics.clear()
        self.request_history.clear()
        self.error_history.clear()
        self.start_time = datetime.now()
        logger.info("Metrics reset")


# Global metrics instance
_metrics = MetricsService()


def get_metrics() -> MetricsService:
    """Get global metrics instance."""
    return _metrics


# Middleware helper for timing requests
class RequestTimer:
    """Context manager for timing requests."""

    def __init__(self, endpoint: str):
        """Initialize timer."""
        self.endpoint = endpoint
        self.start_time = None
        self.duration_ms = None

    def __enter__(self):
        """Start timing."""
        self.start_time = time.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Stop timing and record metric."""
        self.duration_ms = (time.time() - self.start_time) * 1000

        status_code = 500 if exc_type else 200
        error = str(exc_val) if exc_val else None

        get_metrics().record_request(
            self.endpoint,
            self.duration_ms,
            status_code,
            error
        )
