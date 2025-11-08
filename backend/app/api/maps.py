"""Maps and geocoding API endpoints."""

import logging
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from ..services.maps_service import geocode_address, reverse_geocode, search_nearby

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/maps", tags=["maps"])


class GeocodeResult(BaseModel):
    """Geocoding result."""
    display_name: str = Field(..., description="Full address display name")
    latitude: float = Field(..., description="Latitude")
    longitude: float = Field(..., description="Longitude")
    address: Dict[str, Any] = Field(..., description="Address components")
    type: Optional[str] = Field(None, description="Place type")
    importance: Optional[float] = Field(None, description="Result importance score")


class NearbyPlace(BaseModel):
    """Nearby place result."""
    display_name: str = Field(..., description="Full address display name")
    latitude: float = Field(..., description="Latitude")
    longitude: float = Field(..., description="Longitude")
    address: Dict[str, Any] = Field(..., description="Address components")
    type: Optional[str] = Field(None, description="Place type")
    distance_meters: int = Field(..., description="Distance in meters")
    importance: Optional[float] = Field(None, description="Result importance score")


@router.get("/geocode", response_model=List[GeocodeResult])
async def geocode(
    address: str = Query(..., description="Adresse zum Geocodieren"),
    limit: int = Query(5, ge=1, le=20, description="Maximale Anzahl Ergebnisse")
):
    """
    Adresse in Koordinaten umwandeln (Geocoding).

    Wandelt eine Adresse in geografische Koordinaten um.

    **Kostenlos:** Nutzt Nominatim/OpenStreetMap (keine API-Key erforderlich)

    **Beispiele:**
    - `/api/maps/geocode?address=Rathaus Rüsselsheim`
    - `/api/maps/geocode?address=Bahnhofstraße 1, 65428 Rüsselsheim`
    - `/api/maps/geocode?address=Frankfurt Hauptbahnhof`
    """
    try:
        results = await geocode_address(address, limit)
        if not results:
            raise HTTPException(status_code=404, detail="Keine Ergebnisse gefunden")
        return results
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in geocode endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/reverse-geocode", response_model=GeocodeResult)
async def reverse(
    lat: float = Query(..., description="Breitengrad"),
    lon: float = Query(..., description="Längengrad")
):
    """
    Koordinaten in Adresse umwandeln (Reverse Geocoding).

    Wandelt geografische Koordinaten in eine Adresse um.

    **Kostenlos:** Nutzt Nominatim/OpenStreetMap (keine API-Key erforderlich)

    **Beispiel:**
    - `/api/maps/reverse-geocode?lat=49.9897&lon=8.4189` (Rüsselsheim Rathaus)
    """
    try:
        result = await reverse_geocode(lat, lon)
        return result
    except Exception as e:
        logger.error(f"Error in reverse geocode endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/nearby", response_model=List[NearbyPlace])
async def nearby(
    lat: float = Query(..., description="Breitengrad"),
    lon: float = Query(..., description="Längengrad"),
    query: str = Query(..., description="Suchbegriff (z.B. 'restaurant', 'apotheke', 'parkplatz')"),
    radius: int = Query(5000, ge=100, le=50000, description="Suchradius in Metern (100-50000)")
):
    """
    Orte in der Nähe suchen.

    Sucht nach Orten in der Umgebung der angegebenen Koordinaten.

    **Kostenlos:** Nutzt Nominatim/OpenStreetMap (keine API-Key erforderlich)

    **Beispiele:**
    - `/api/maps/nearby?lat=49.9897&lon=8.4189&query=restaurant&radius=2000`
    - `/api/maps/nearby?lat=49.9897&lon=8.4189&query=apotheke&radius=1000`
    - `/api/maps/nearby?lat=49.9897&lon=8.4189&query=parkplatz&radius=500`

    **Nützliche Suchbegriffe:**
    - restaurant, café, bäckerei
    - apotheke, arzt, krankenhaus
    - parkplatz, tankstelle
    - supermarkt, einkaufszentrum
    - schule, kindergarten
    - bank, post
    """
    try:
        results = await search_nearby(lat, lon, query, radius)
        if not results:
            raise HTTPException(
                status_code=404,
                detail=f"Keine '{query}' in {radius}m Umkreis gefunden"
            )
        return results
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in nearby endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))
