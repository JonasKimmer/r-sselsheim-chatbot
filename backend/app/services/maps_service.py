"""Maps and geocoding service using Nominatim/OpenStreetMap (free)."""

import logging
import httpx
from typing import Dict, List, Optional
from .cache_service import cached
from .retry_service import async_retry

logger = logging.getLogger(__name__)

NOMINATIM_URL = "https://nominatim.openstreetmap.org"
USER_AGENT = "RuesselsheimChatbot/1.0"


@cached(ttl_seconds=1800, key_prefix="geocode")  # Cache for 30 minutes
@async_retry(max_attempts=3, delay_seconds=1.0, backoff_factor=2.0)
async def geocode_address(address: str, limit: int = 5) -> List[Dict]:
    """
    Geocode an address to coordinates.

    Args:
        address: Address to geocode
        limit: Maximum number of results

    Returns:
        List of geocoding results with coordinates
    """
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            params = {
                "q": address,
                "format": "json",
                "limit": limit,
                "addressdetails": 1,
                "accept-language": "de"
            }
            headers = {
                "User-Agent": USER_AGENT
            }

            response = await client.get(
                f"{NOMINATIM_URL}/search",
                params=params,
                headers=headers
            )
            response.raise_for_status()

            results = response.json()

            parsed_results = []
            for result in results:
                parsed_results.append({
                    "display_name": result.get("display_name"),
                    "latitude": float(result.get("lat", 0)),
                    "longitude": float(result.get("lon", 0)),
                    "address": result.get("address", {}),
                    "type": result.get("type"),
                    "importance": result.get("importance")
                })

            logger.info(f"Geocoded address '{address}': {len(parsed_results)} results")
            return parsed_results

    except httpx.HTTPError as e:
        logger.error(f"HTTP error geocoding address: {e}")
        raise Exception(f"Fehler beim Geocoding: {str(e)}")
    except Exception as e:
        logger.error(f"Error geocoding address: {e}")
        raise Exception(f"Fehler beim Geocoding: {str(e)}")


@cached(ttl_seconds=3600, key_prefix="reverse_geocode")  # Cache for 1 hour
@async_retry(max_attempts=3, delay_seconds=1.0, backoff_factor=2.0)
async def reverse_geocode(lat: float, lon: float) -> Dict:
    """
    Reverse geocode coordinates to address.

    Args:
        lat: Latitude
        lon: Longitude

    Returns:
        Address information
    """
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            params = {
                "lat": lat,
                "lon": lon,
                "format": "json",
                "addressdetails": 1,
                "accept-language": "de"
            }
            headers = {
                "User-Agent": USER_AGENT
            }

            response = await client.get(
                f"{NOMINATIM_URL}/reverse",
                params=params,
                headers=headers
            )
            response.raise_for_status()

            result = response.json()

            parsed_result = {
                "display_name": result.get("display_name"),
                "latitude": lat,
                "longitude": lon,
                "address": result.get("address", {}),
                "type": result.get("type")
            }

            logger.info(f"Reverse geocoded ({lat}, {lon})")
            return parsed_result

    except httpx.HTTPError as e:
        logger.error(f"HTTP error reverse geocoding: {e}")
        raise Exception(f"Fehler beim Reverse Geocoding: {str(e)}")
    except Exception as e:
        logger.error(f"Error reverse geocoding: {e}")
        raise Exception(f"Fehler beim Reverse Geocoding: {str(e)}")


@cached(ttl_seconds=900, key_prefix="nearby")  # Cache for 15 minutes
@async_retry(max_attempts=3, delay_seconds=1.0, backoff_factor=2.0)
async def search_nearby(
    lat: float,
    lon: float,
    query: str,
    radius: int = 5000
) -> List[Dict]:
    """
    Search for places nearby.

    Args:
        lat: Latitude
        lon: Longitude
        query: Search query (e.g., "restaurant", "apotheke", "parkplatz")
        radius: Search radius in meters (max 50000)

    Returns:
        List of nearby places
    """
    try:
        # Limit radius to 50km
        radius = min(radius, 50000)

        async with httpx.AsyncClient(timeout=10.0) as client:
            # Search in a bounding box around the coordinates
            # Approximate: 1 degree ≈ 111km
            radius_deg = radius / 111000

            params = {
                "q": query,
                "format": "json",
                "limit": 20,
                "addressdetails": 1,
                "accept-language": "de",
                "bounded": 1,
                "viewbox": f"{lon - radius_deg},{lat + radius_deg},{lon + radius_deg},{lat - radius_deg}"
            }
            headers = {
                "User-Agent": USER_AGENT
            }

            response = await client.get(
                f"{NOMINATIM_URL}/search",
                params=params,
                headers=headers
            )
            response.raise_for_status()

            results = response.json()

            parsed_results = []
            for result in results:
                result_lat = float(result.get("lat", 0))
                result_lon = float(result.get("lon", 0))

                # Calculate approximate distance
                distance = _calculate_distance(lat, lon, result_lat, result_lon)

                if distance <= radius:
                    parsed_results.append({
                        "display_name": result.get("display_name"),
                        "latitude": result_lat,
                        "longitude": result_lon,
                        "address": result.get("address", {}),
                        "type": result.get("type"),
                        "distance_meters": round(distance),
                        "importance": result.get("importance")
                    })

            # Sort by distance
            parsed_results.sort(key=lambda x: x["distance_meters"])

            logger.info(f"Found {len(parsed_results)} places near ({lat}, {lon})")
            return parsed_results

    except httpx.HTTPError as e:
        logger.error(f"HTTP error searching nearby: {e}")
        raise Exception(f"Fehler bei der Umgebungssuche: {str(e)}")
    except Exception as e:
        logger.error(f"Error searching nearby: {e}")
        raise Exception(f"Fehler bei der Umgebungssuche: {str(e)}")


def _calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate distance between two coordinates using Haversine formula.

    Returns distance in meters.
    """
    from math import radians, sin, cos, sqrt, atan2

    R = 6371000  # Earth radius in meters

    lat1_rad = radians(lat1)
    lat2_rad = radians(lat2)
    delta_lat = radians(lat2 - lat1)
    delta_lon = radians(lon2 - lon1)

    a = sin(delta_lat / 2) ** 2 + cos(lat1_rad) * cos(lat2_rad) * sin(delta_lon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    return distance
