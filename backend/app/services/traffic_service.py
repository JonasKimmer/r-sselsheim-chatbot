"""Traffic and speed camera service."""

import logging
from typing import List, Dict, Optional
from math import radians, sin, cos, sqrt, atan2

logger = logging.getLogger(__name__)

# Static speed camera database for Rüsselsheim and surroundings
# Data based on publicly available information
SPEED_CAMERAS = [
    {
        "id": 1,
        "name": "B43 Rüsselsheim Richtung Mainz",
        "latitude": 49.9903,
        "longitude": 8.4102,
        "street": "Mainzer Straße / B43",
        "type": "fixed",
        "speed_limit": 50,
        "direction": "Richtung Mainz",
        "description": "Festinstallierter Blitzer auf der B43"
    },
    {
        "id": 2,
        "name": "B486 Rüsselsheim Richtung Raunheim",
        "latitude": 50.0012,
        "longitude": 8.4356,
        "street": "Bahnhofstraße / B486",
        "type": "fixed",
        "speed_limit": 50,
        "direction": "Richtung Raunheim",
        "description": "Festinstallierter Blitzer auf der B486"
    },
    {
        "id": 3,
        "name": "Eisenstraße Rüsselsheim",
        "latitude": 49.9876,
        "longitude": 8.4231,
        "street": "Eisenstraße",
        "type": "fixed",
        "speed_limit": 50,
        "direction": "Beide Richtungen",
        "description": "Festinstallierter Blitzer in der Eisenstraße"
    },
    {
        "id": 4,
        "name": "A67 AS Rüsselsheim",
        "latitude": 49.9956,
        "longitude": 8.4445,
        "street": "A67",
        "type": "fixed",
        "speed_limit": 120,
        "direction": "Richtung Darmstadt",
        "description": "Blitzer an der Anschlussstelle Rüsselsheim"
    },
    {
        "id": 5,
        "name": "B43 Bauschheim",
        "latitude": 49.9745,
        "longitude": 8.3989,
        "street": "B43",
        "type": "mobile_frequent",
        "speed_limit": 70,
        "direction": "Beide Richtungen",
        "description": "Häufige mobile Geschwindigkeitskontrolle"
    },
    {
        "id": 6,
        "name": "Opelkreisel",
        "latitude": 49.9889,
        "longitude": 8.4167,
        "street": "Am Opelkreisel",
        "type": "fixed",
        "speed_limit": 50,
        "direction": "Kreisverkehr",
        "description": "Blitzer am Opelkreisel"
    }
]


def _calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate distance between two coordinates using Haversine formula.

    Returns distance in meters.
    """
    R = 6371000  # Earth radius in meters

    lat1_rad = radians(lat1)
    lat2_rad = radians(lat2)
    delta_lat = radians(lat2 - lat1)
    delta_lon = radians(lon2 - lon1)

    a = sin(delta_lat / 2) ** 2 + cos(lat1_rad) * cos(lat2_rad) * sin(delta_lon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    return distance


async def get_speed_cameras(
    lat: Optional[float] = None,
    lon: Optional[float] = None,
    radius: int = 10000
) -> List[Dict]:
    """
    Get speed cameras, optionally filtered by location.

    Args:
        lat: Latitude for nearby search
        lon: Longitude for nearby search
        radius: Search radius in meters (default: 10km)

    Returns:
        List of speed cameras
    """
    cameras = SPEED_CAMERAS.copy()

    # If coordinates provided, filter by distance and add distance info
    if lat is not None and lon is not None:
        filtered_cameras = []
        for camera in cameras:
            distance = _calculate_distance(
                lat, lon,
                camera["latitude"], camera["longitude"]
            )
            if distance <= radius:
                camera_with_distance = camera.copy()
                camera_with_distance["distance_meters"] = round(distance)
                filtered_cameras.append(camera_with_distance)

        # Sort by distance
        filtered_cameras.sort(key=lambda x: x["distance_meters"])
        logger.info(f"Found {len(filtered_cameras)} speed cameras within {radius}m")
        return filtered_cameras
    else:
        logger.info(f"Returned all {len(cameras)} speed cameras")
        return cameras


async def get_speed_camera_by_id(camera_id: int) -> Optional[Dict]:
    """
    Get a specific speed camera by ID.

    Args:
        camera_id: Camera ID

    Returns:
        Speed camera data or None if not found
    """
    for camera in SPEED_CAMERAS:
        if camera["id"] == camera_id:
            logger.info(f"Found speed camera {camera_id}")
            return camera.copy()

    logger.warning(f"Speed camera {camera_id} not found")
    return None


async def get_traffic_info() -> Dict:
    """
    Get general traffic information for Rüsselsheim.

    Returns:
        Traffic information and tips
    """
    return {
        "region": "Rüsselsheim am Main",
        "info": {
            "total_cameras": len(SPEED_CAMERAS),
            "camera_types": {
                "fixed": len([c for c in SPEED_CAMERAS if c["type"] == "fixed"]),
                "mobile_frequent": len([c for c in SPEED_CAMERAS if c["type"] == "mobile_frequent"])
            }
        },
        "tips": [
            "Achten Sie auf die ausgeschilderten Geschwindigkeitsbegrenzungen",
            "Besondere Vorsicht in Tempo-30-Zonen und Schulnähe",
            "Mobile Blitzer können an wechselnden Standorten aufgestellt werden",
            "Bei Regen und schlechter Sicht gelten oft niedrigere Tempolimits"
        ],
        "emergency_numbers": {
            "police": "110",
            "fire_ambulance": "112",
            "traffic_info": "0800 8608050"
        }
    }
