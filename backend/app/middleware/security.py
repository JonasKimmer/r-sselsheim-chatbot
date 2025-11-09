"""Security middleware and input validation."""

import logging
import re
from typing import Optional
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
import time

logger = logging.getLogger(__name__)


class SecurityMiddleware(BaseHTTPMiddleware):
    """Middleware for security checks and rate limiting."""

    def __init__(self, app, rate_limit_requests: int = 100, rate_limit_window: int = 60):
        """
        Initialize security middleware.

        Args:
            app: FastAPI application
            rate_limit_requests: Maximum requests per window
            rate_limit_window: Time window in seconds
        """
        super().__init__(app)
        self.rate_limit_requests = rate_limit_requests
        self.rate_limit_window = rate_limit_window
        self.request_counts = {}  # {ip: [(timestamp, count)]}

    async def dispatch(self, request: Request, call_next):
        """Process request with security checks."""
        client_ip = self._get_client_ip(request)

        # Rate limiting
        if self._is_rate_limited(client_ip):
            logger.warning(f"Rate limit exceeded for IP: {client_ip}")
            return JSONResponse(
                status_code=429,
                content={
                    "detail": "Rate limit exceeded. Please try again later.",
                    "retry_after": self.rate_limit_window
                }
            )

        # Track request
        self._track_request(client_ip)

        # Add security headers
        response = await call_next(request)

        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"

        return response

    def _get_client_ip(self, request: Request) -> str:
        """Get client IP address from request."""
        forwarded = request.headers.get("X-Forwarded-For")
        if forwarded:
            return forwarded.split(",")[0].strip()
        return request.client.host if request.client else "unknown"

    def _is_rate_limited(self, client_ip: str) -> bool:
        """Check if client has exceeded rate limit."""
        current_time = time.time()
        cutoff_time = current_time - self.rate_limit_window

        if client_ip not in self.request_counts:
            return False

        # Remove old entries
        self.request_counts[client_ip] = [
            t for t in self.request_counts[client_ip]
            if t > cutoff_time
        ]

        # Check if exceeded
        return len(self.request_counts[client_ip]) >= self.rate_limit_requests

    def _track_request(self, client_ip: str):
        """Track request for rate limiting."""
        current_time = time.time()

        if client_ip not in self.request_counts:
            self.request_counts[client_ip] = []

        self.request_counts[client_ip].append(current_time)


class InputValidator:
    """Utility class for input validation and sanitization."""

    # SQL injection patterns
    SQL_INJECTION_PATTERNS = [
        r"(\b(SELECT|INSERT|UPDATE|DELETE|DROP|CREATE|ALTER|EXEC|EXECUTE)\b)",
        r"(--|\#|\/\*|\*\/)",
        r"(\bOR\b.*=.*)",
        r"(\bAND\b.*=.*)",
        r"(;.*)",
        r"(\bUNION\b.*\bSELECT\b)"
    ]

    # XSS patterns
    XSS_PATTERNS = [
        r"<script[^>]*>.*?</script>",
        r"javascript:",
        r"on\w+\s*=",
        r"<iframe",
        r"<object",
        r"<embed"
    ]

    @classmethod
    def sanitize_text(cls, text: str, max_length: int = 10000) -> str:
        """
        Sanitize user input text.

        Args:
            text: Input text
            max_length: Maximum allowed length

        Returns:
            Sanitized text

        Raises:
            HTTPException: If input contains malicious content
        """
        if not text:
            return ""

        # Check length
        if len(text) > max_length:
            raise HTTPException(
                status_code=400,
                detail=f"Input too long. Maximum {max_length} characters allowed."
            )

        # Check for SQL injection
        if cls._contains_sql_injection(text):
            logger.warning(f"SQL injection attempt detected: {text[:100]}")
            raise HTTPException(
                status_code=400,
                detail="Input contains potentially malicious content."
            )

        # Check for XSS
        if cls._contains_xss(text):
            logger.warning(f"XSS attempt detected: {text[:100]}")
            raise HTTPException(
                status_code=400,
                detail="Input contains potentially malicious content."
            )

        # Basic sanitization (remove control characters)
        sanitized = re.sub(r'[\x00-\x08\x0B-\x0C\x0E-\x1F\x7F]', '', text)

        return sanitized.strip()

    @classmethod
    def _contains_sql_injection(cls, text: str) -> bool:
        """Check if text contains SQL injection patterns."""
        text_upper = text.upper()

        for pattern in cls.SQL_INJECTION_PATTERNS:
            if re.search(pattern, text_upper, re.IGNORECASE):
                return True

        return False

    @classmethod
    def _contains_xss(cls, text: str) -> bool:
        """Check if text contains XSS patterns."""
        for pattern in cls.XSS_PATTERNS:
            if re.search(pattern, text, re.IGNORECASE):
                return True

        return False

    @classmethod
    def validate_session_id(cls, session_id: Optional[str]) -> str:
        """
        Validate and sanitize session ID.

        Args:
            session_id: Session ID to validate

        Returns:
            Sanitized session ID

        Raises:
            HTTPException: If session ID is invalid
        """
        if not session_id:
            return ""

        # Session IDs should be alphanumeric with hyphens/underscores
        if not re.match(r'^[a-zA-Z0-9\-_]{1,100}$', session_id):
            raise HTTPException(
                status_code=400,
                detail="Invalid session ID format."
            )

        return session_id

    @classmethod
    def validate_coordinates(cls, lat: float, lon: float) -> tuple[float, float]:
        """
        Validate geographic coordinates.

        Args:
            lat: Latitude
            lon: Longitude

        Returns:
            Validated coordinates

        Raises:
            HTTPException: If coordinates are invalid
        """
        if not (-90 <= lat <= 90):
            raise HTTPException(
                status_code=400,
                detail="Latitude must be between -90 and 90."
            )

        if not (-180 <= lon <= 180):
            raise HTTPException(
                status_code=400,
                detail="Longitude must be between -180 and 180."
            )

        return lat, lon

    @classmethod
    def validate_limit(cls, limit: int, max_limit: int = 100) -> int:
        """
        Validate pagination limit.

        Args:
            limit: Requested limit
            max_limit: Maximum allowed limit

        Returns:
            Validated limit

        Raises:
            HTTPException: If limit is invalid
        """
        if limit < 1:
            raise HTTPException(
                status_code=400,
                detail="Limit must be at least 1."
            )

        if limit > max_limit:
            raise HTTPException(
                status_code=400,
                detail=f"Limit cannot exceed {max_limit}."
            )

        return limit
