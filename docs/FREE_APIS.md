# Kostenlose APIs für Rüsselsheim Chatbot

Der Chatbot bietet jetzt zusätzliche kostenlose APIs für lokale Dienste in Rüsselsheim:

## 🌤️ Wetter-API

Aktuelle Wetterdaten und Vorhersagen für Rüsselsheim und Umgebung.

### Features
- ✅ Aktuelle Wetterdaten (Temperatur, Luftfeuchtigkeit, Wind, Niederschlag)
- ✅ 3-Tage-Vorhersage
- ✅ Deutsche Wetterbeschreibungen
- ✅ **100% kostenlos** - nutzt Open-Meteo API

### Endpunkte

#### Aktuelles Wetter
```bash
GET /api/weather/
GET /api/weather/?city=Frankfurt&lat=50.1109&lon=8.6821
```

**Response:**
```json
{
  "city": "Rüsselsheim am Main",
  "coordinates": {
    "latitude": 49.9897,
    "longitude": 8.4189
  },
  "current": {
    "temperature": 18.5,
    "feels_like": 17.2,
    "humidity": 65,
    "wind_speed": 12.5,
    "precipitation": 0,
    "weather_code": 2,
    "description": "Teilweise bewölkt",
    "time": "2025-01-08T15:00"
  },
  "forecast": [
    {
      "date": "2025-01-08",
      "temp_max": 20.5,
      "temp_min": 12.3,
      "precipitation": 0,
      "weather_code": 1,
      "description": "Überwiegend klar"
    }
  ]
}
```

#### Wettervorhersage
```bash
GET /api/weather/forecast?days=7
```

## 🗺️ Maps & Geocoding API

Adresssuche und Ortssuche basierend auf OpenStreetMap.

### Features
- ✅ Adresse → Koordinaten (Geocoding)
- ✅ Koordinaten → Adresse (Reverse Geocoding)
- ✅ Umgebungssuche (Restaurants, Apotheken, etc.)
- ✅ **100% kostenlos** - nutzt Nominatim/OpenStreetMap

### Endpunkte

#### Geocoding (Adresse → Koordinaten)
```bash
GET /api/maps/geocode?address=Rathaus+Rüsselsheim
GET /api/maps/geocode?address=Bahnhofstraße+1,+65428+Rüsselsheim&limit=5
```

**Response:**
```json
[
  {
    "display_name": "Rathaus, Marktplatz, Rüsselsheim am Main, ...",
    "latitude": 49.9897,
    "longitude": 8.4189,
    "address": {
      "amenity": "Rathaus",
      "road": "Marktplatz",
      "city": "Rüsselsheim am Main",
      "postcode": "65428",
      "country": "Deutschland"
    },
    "type": "amenity",
    "importance": 0.735
  }
]
```

#### Reverse Geocoding (Koordinaten → Adresse)
```bash
GET /api/maps/reverse-geocode?lat=49.9897&lon=8.4189
```

#### Umgebungssuche
```bash
GET /api/maps/nearby?lat=49.9897&lon=8.4189&query=restaurant&radius=2000
GET /api/maps/nearby?lat=49.9897&lon=8.4189&query=apotheke&radius=1000
```

**Nützliche Suchbegriffe:**
- `restaurant`, `café`, `bäckerei`
- `apotheke`, `arzt`, `krankenhaus`
- `parkplatz`, `tankstelle`
- `supermarkt`, `einkaufszentrum`
- `schule`, `kindergarten`
- `bank`, `post`

## 🚦 Verkehrs-API (Blitzer & Verkehrsinformationen)

Bekannte Blitzer und Verkehrsinformationen für Rüsselsheim.

### Features
- ✅ Festinstallierte Blitzer
- ✅ Häufige mobile Kontrollstellen
- ✅ Umkreissuche
- ✅ Verkehrssicherheitstipps
- ✅ **100% kostenlos** - statische Datenbank

### Endpunkte

#### Alle Blitzer
```bash
GET /api/traffic/speed-cameras
```

#### Blitzer im Umkreis
```bash
GET /api/traffic/speed-cameras?lat=49.9897&lon=8.4189&radius=5000
GET /api/traffic/nearby-cameras?lat=49.9897&lon=8.4189&radius=3000
```

**Response:**
```json
[
  {
    "id": 1,
    "name": "B43 Rüsselsheim Richtung Mainz",
    "latitude": 49.9903,
    "longitude": 8.4102,
    "street": "Mainzer Straße / B43",
    "type": "fixed",
    "speed_limit": 50,
    "direction": "Richtung Mainz",
    "description": "Festinstallierter Blitzer auf der B43",
    "distance_meters": 732
  }
]
```

#### Einzelner Blitzer
```bash
GET /api/traffic/speed-cameras/1
```

#### Verkehrsinformationen
```bash
GET /api/traffic/info
```

**Response:**
```json
{
  "region": "Rüsselsheim am Main",
  "info": {
    "total_cameras": 6,
    "camera_types": {
      "fixed": 5,
      "mobile_frequent": 1
    }
  },
  "tips": [
    "Achten Sie auf die ausgeschilderten Geschwindigkeitsbegrenzungen",
    "Besondere Vorsicht in Tempo-30-Zonen und Schulnähe",
    "Mobile Blitzer können an wechselnden Standorten aufgestellt werden"
  ],
  "emergency_numbers": {
    "police": "110",
    "fire_ambulance": "112",
    "traffic_info": "0800 8608050"
  }
}
```

## 🎯 Verwendung im Chatbot

Diese APIs können direkt vom Chatbot verwendet werden, um Nutzerfragen zu beantworten:

**Beispiele:**
- "Wie ist das Wetter heute in Rüsselsheim?"
- "Zeige mir Restaurants in der Nähe des Rathauses"
- "Wo sind Blitzer auf der B43?"
- "Was ist die Adresse vom Rathaus?"
- "Gibt es Apotheken in der Nähe?"

## 📊 API-Dokumentation

Nach dem Start des Backends ist die vollständige API-Dokumentation verfügbar unter:

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

## 🔒 Datenschutz

Alle APIs nutzen kostenlose, öffentliche Dienste:
- **Open-Meteo:** Keine Registrierung, keine Tracker
- **Nominatim/OSM:** Community-basiert, datenschutzfreundlich
- **Blitzer-Daten:** Statische, öffentlich bekannte Daten

## ⚡ Rate Limits

**Open-Meteo:**
- Keine Registrierung nötig
- Bis zu 10.000 Anfragen/Tag kostenlos

**Nominatim:**
- Max. 1 Anfrage/Sekunde
- User-Agent Header erforderlich (wird automatisch gesetzt)

## 🛠️ Technische Details

Alle neuen Services nutzen:
- **httpx** für asynchrone HTTP-Anfragen
- **FastAPI** für API-Endpunkte mit automatischer Dokumentation
- **Pydantic** für Datenvalidierung

Keine zusätzlichen Dependencies erforderlich - `httpx` ist bereits installiert!

## 🚀 Weitere Möglichkeiten

Zukünftig könnten weitere kostenlose APIs integriert werden:
- 📅 Veranstaltungskalender
- 🚌 Nahverkehrsdaten (RMV)
- 🏛️ Öffnungszeiten öffentlicher Einrichtungen
- 📰 Lokale Nachrichten
- ♻️ Müllabfuhrtermine
