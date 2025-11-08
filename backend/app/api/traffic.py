"""Traffic and speed camera API endpoints."""

import logging
from fastapi import APIRouter, HTTPException, Query, Path
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from ..services.traffic_service import (
    get_speed_cameras,
    get_speed_camera_by_id,
    get_traffic_info
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/traffic", tags=["traffic"])


class SpeedCamera(BaseModel):
    """Speed camera data."""
    id: int = Field(..., description="Camera ID")
    name: str = Field(..., description="Camera name/location")
    latitude: float = Field(..., description="Latitude")
    longitude: float = Field(..., description="Longitude")
    street: str = Field(..., description="Street name")
    type: str = Field(..., description="Camera type (fixed, mobile_frequent)")
    speed_limit: int = Field(..., description="Speed limit in km/h")
    direction: str = Field(..., description="Direction/coverage")
    description: str = Field(..., description="Additional information")
    distance_meters: Optional[int] = Field(None, description="Distance in meters (only when searching nearby)")


class TrafficInfo(BaseModel):
    """General traffic information."""
    region: str = Field(..., description="Region name")
    info: Dict[str, Any] = Field(..., description="Traffic statistics")
    tips: List[str] = Field(..., description="Traffic safety tips")
    emergency_numbers: Dict[str, str] = Field(..., description="Emergency contact numbers")


@router.get("/speed-cameras", response_model=List[SpeedCamera])
async def list_speed_cameras(
    lat: Optional[float] = Query(None, description="Breitengrad für Umkreissuche"),
    lon: Optional[float] = Query(None, description="Längengrad für Umkreissuche"),
    radius: int = Query(10000, ge=100, le=50000, description="Suchradius in Metern (100-50000)")
):
    """
    Blitzer und Geschwindigkeitskontrollen abrufen.

    Zeigt bekannte Blitzer und häufige Kontrollstellen in Rüsselsheim und Umgebung.

    **Kostenlos:** Nutzt statische Datenbank mit öffentlich bekannten Blitzern

    **Typen:**
    - `fixed`: Festinstallierte Blitzer
    - `mobile_frequent`: Häufige mobile Kontrollstellen

    **Beispiele:**
    - `/api/traffic/speed-cameras` - Alle Blitzer
    - `/api/traffic/speed-cameras?lat=49.9897&lon=8.4189&radius=5000` - Blitzer im Umkreis von 5km

    **Hinweis:** Diese Daten dienen der Information. Mobile Blitzer können auch an anderen
    Stellen aufgestellt werden. Bitte beachten Sie immer die Verkehrsregeln.
    """
    try:
        cameras = await get_speed_cameras(lat, lon, radius)
        if not cameras:
            raise HTTPException(
                status_code=404,
                detail="Keine Blitzer im angegebenen Umkreis gefunden"
            )
        return cameras
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in speed cameras endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/speed-cameras/{camera_id}", response_model=SpeedCamera)
async def get_camera_details(
    camera_id: int = Path(..., description="Blitzer-ID")
):
    """
    Details zu einem bestimmten Blitzer abrufen.

    **Beispiel:**
    - `/api/traffic/speed-cameras/1` - Details zum Blitzer mit ID 1
    """
    try:
        camera = await get_speed_camera_by_id(camera_id)
        if not camera:
            raise HTTPException(status_code=404, detail="Blitzer nicht gefunden")
        return camera
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in camera details endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/info", response_model=TrafficInfo)
async def traffic_info():
    """
    Allgemeine Verkehrsinformationen für Rüsselsheim abrufen.

    Liefert Statistiken, Sicherheitstipps und Notfallnummern.

    **Kostenlos:** Keine externe API erforderlich

    **Beispiel:**
    - `/api/traffic/info` - Verkehrsinformationen
    """
    try:
        info = await get_traffic_info()
        return info
    except Exception as e:
        logger.error(f"Error in traffic info endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/nearby-cameras", response_model=List[SpeedCamera])
async def nearby_cameras(
    lat: float = Query(..., description="Breitengrad (z.B. 49.9897 für Rüsselsheim)"),
    lon: float = Query(..., description="Längengrad (z.B. 8.4189 für Rüsselsheim)"),
    radius: int = Query(2000, ge=100, le=50000, description="Suchradius in Metern")
):
    """
    Blitzer in der Nähe finden.

    Findet alle Blitzer im angegebenen Umkreis, sortiert nach Entfernung.

    **Beispiel:**
    - `/api/traffic/nearby-cameras?lat=49.9897&lon=8.4189&radius=3000`
      Findet alle Blitzer in 3km Umkreis um das Rüsselsheimer Rathaus

    **Hinweis:** Die Entfernung wird in Luftlinie berechnet. Tatsächliche Fahrstrecke
    kann länger sein.
    """
    try:
        cameras = await get_speed_cameras(lat, lon, radius)
        if not cameras:
            raise HTTPException(
                status_code=404,
                detail=f"Keine Blitzer im Umkreis von {radius}m gefunden"
            )
        return cameras
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in nearby cameras endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))
