# Rüsselsheim Chatbot 🏛️

Ein KI-gestützter Chatbot für die Stadt Rüsselsheim am Main, der Bürgerinnen und Bürgern bei Fragen zu städtischen Dienstleistungen hilft.

> 💰 **NEU:** Jetzt **100% kostenlos** nutzbar mit Google Gemini! Siehe [Kostenlose Setup-Anleitung](docs/FREE_SETUP.md)

## 🎯 Features

### Phase 1 (Implementiert)
- ✅ **RAG-System** für Stadt-Informationen mit pgvector
- ✅ **Semantische Suche** in Dokumenten
- ✅ **Chat-API** mit Multi-Turn-Gesprächen
- ✅ **Intent-Erkennung** (Information, Termin, Formular)
- ✅ **Web-Interface** mit moderner Chat-UI
- ✅ **Flexible LLM-Integration** - Google Gemini (kostenlos) oder Claude (bezahlt)
- ✅ **Lokale oder Cloud Embeddings** - vollständig konfigurierbar
- ✅ **PostgreSQL** mit pgvector für Vektorspeicherung
- ✅ **100% kostenlos nutzbar** mit Gemini + lokalen Embeddings

## 🏗️ Tech-Stack

### Backend
- **FastAPI** - Modernes Python Web Framework
- **PostgreSQL + pgvector** - Vektordatenbank
- **LLM:** Google Gemini (kostenlos) ODER Anthropic Claude (bezahlt)
- **Embeddings:** Lokale Modelle (kostenlos) ODER OpenAI (bezahlt)
- **SQLAlchemy** - ORM für Datenbankzugriff
- **Pydantic** - Datenvalidierung

### Frontend
- **React 18** - UI Framework
- **Tailwind CSS** - Styling
- **Vite** - Build Tool
- **Axios** - HTTP Client

### Infrastructure
- **Docker & Docker Compose** - Containerisierung
- **Uvicorn** - ASGI Server

## 📁 Projektstruktur

```
r-sselsheim-chatbot/
├── backend/                    # FastAPI Backend
│   ├── app/
│   │   ├── api/               # API Endpoints
│   │   │   ├── chat.py        # Chat-Endpoints
│   │   │   ├── documents.py   # Dokumenten-Management
│   │   │   └── health.py      # Health-Check
│   │   ├── db/                # Datenbankverbindung
│   │   ├── models/            # SQLAlchemy Models
│   │   │   ├── chat.py        # Chat & Session Models
│   │   │   └── document.py    # Dokument Model
│   │   ├── services/          # Business Logic
│   │   │   ├── chat_service.py      # Chat-Verwaltung
│   │   │   ├── rag_service.py       # RAG-System
│   │   │   └── embedding_service.py # Embeddings
│   │   ├── config.py          # Konfiguration
│   │   └── main.py            # FastAPI App
│   ├── scripts/
│   │   └── import_data.py     # Datenimport
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/                   # React Frontend
│   ├── src/
│   │   ├── components/        # React Komponenten
│   │   │   ├── ChatContainer.jsx
│   │   │   ├── ChatMessage.jsx
│   │   │   ├── ChatInput.jsx
│   │   │   └── Header.jsx
│   │   ├── services/          # API Services
│   │   │   └── api.js
│   │   ├── styles/
│   │   │   └── index.css
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── package.json
│   ├── vite.config.js
│   └── Dockerfile
├── data/                       # Beispieldaten
│   └── ruesselsheim_data.json
├── docker-compose.yml
├── Makefile
├── .env.example
└── README.md
```

## 🚀 Quick Start

### Voraussetzungen

- Docker & Docker Compose
- **Eine** der folgenden API-Keys:
  - **Google Gemini API Key** - **KOSTENLOS** (empfohlen) 🆓
  - **ODER** Anthropic Claude API Key - bezahlt

> 💡 **Empfehlung:** Nutzen Sie Gemini für kostenlosen Betrieb! Siehe [Kostenlose Setup-Anleitung](docs/FREE_SETUP.md)

### Installation

1. **Repository klonen**
   ```bash
   git clone <repository-url>
   cd r-sselsheim-chatbot
   ```

2. **Umgebungsvariablen konfigurieren**
   ```bash
   cp .env.example .env
   ```

   **Option A: Kostenlos mit Gemini (empfohlen)** 🆓
   ```env
   LLM_PROVIDER=gemini
   GEMINI_API_KEY=your_gemini_key_here  # Kostenlos bei https://makersuite.google.com/app/apikey
   EMBEDDING_PROVIDER=local  # Lokale Embeddings (kostenlos)
   ```

   **Option B: Mit Claude (bezahlt)**
   ```env
   LLM_PROVIDER=claude
   ANTHROPIC_API_KEY=your_anthropic_key_here
   EMBEDDING_PROVIDER=local  # Lokale Embeddings (kostenlos)
   ```

   > 💡 **Kostenlos:** [Gemini API-Key erstellen](https://makersuite.google.com/app/apikey) (keine Kreditkarte nötig)
   > 📖 **Details:** [Kostenlose Setup-Anleitung](docs/FREE_SETUP.md) | [Embedding-Optionen](docs/EMBEDDINGS.md)

3. **Mit Make installieren (empfohlen)**
   ```bash
   make install
   ```

   Oder manuell:
   ```bash
   # Container bauen
   docker-compose build

   # Services starten
   docker-compose up -d

   # Beispieldaten importieren
   docker-compose exec backend python scripts/import_data.py
   ```

4. **Zugriff auf die Anwendung**
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:8000
   - API Dokumentation: http://localhost:8000/docs

## 🛠️ Entwicklung

### Make Commands

```bash
make help           # Zeigt alle verfügbaren Commands
make up             # Startet alle Services
make down           # Stoppt alle Services
make logs           # Zeigt Logs aller Services
make logs-backend   # Zeigt Backend Logs
make logs-frontend  # Zeigt Frontend Logs
make restart        # Startet alle Services neu
make clean          # Entfernt alle Container und Volumes
make import-data    # Importiert Beispieldaten
make shell-backend  # Öffnet Shell im Backend Container
make shell-db       # Öffnet PostgreSQL Shell
```

### Backend entwickeln

1. **Backend Shell öffnen**
   ```bash
   make shell-backend
   ```

2. **Tests ausführen**
   ```bash
   pytest
   ```

3. **Code formatieren**
   ```bash
   black app/
   flake8 app/
   ```

### Frontend entwickeln

1. **Abhängigkeiten installieren**
   ```bash
   cd frontend
   npm install
   ```

2. **Development Server starten**
   ```bash
   npm run dev
   ```

3. **Build erstellen**
   ```bash
   npm run build
   ```

## 📊 API Dokumentation

### Chat Endpoints

**POST /api/chat/**
```json
{
  "message": "Wann hat der Bürgerservice geöffnet?",
  "session_id": "optional-session-id"
}
```

Response:
```json
{
  "session_id": "uuid",
  "message": "Der Bürgerservice...",
  "intent": "information",
  "context_used": true
}
```

**GET /api/chat/{session_id}/history**

Gibt die Chat-Historie für eine Session zurück.

### Document Endpoints

**POST /api/documents/**

Erstellt ein neues Dokument in der Wissensdatenbank.

**POST /api/documents/search**
```json
{
  "query": "KFZ Anmeldung",
  "limit": 5
}
```

## 🎨 Features im Detail

### RAG-System

Das RAG (Retrieval Augmented Generation) System:
- Nutzt pgvector für effiziente Vektorsuche
- OpenAI Embeddings (text-embedding-3-small)
- Semantische Suche mit Cosine-Similarity
- Kontext-Retrieval für präzise Antworten

### Intent-Erkennung

Der Chatbot erkennt automatisch die Absicht:
- **Information**: Allgemeine Fragen
- **Termin**: Terminvereinbarung gewünscht
- **Formular**: Download/Antrag benötigt

### Chat-Management

- Multi-Turn Gespräche mit Context
- Session-basierte Chat-Historie
- Persistente Speicherung in PostgreSQL

## 📚 Beispieldaten

Das System enthält Beispieldaten für:
- ✅ Bürgerservice (Personalausweis, Meldewesen)
- ✅ KFZ-Zulassung (Anmeldung, Ummeldung, Abmeldung)
- ✅ Abfallwirtschaft (Müllabfuhr, Sperrmüll, Wertstoffhof)
- ✅ Öffnungszeiten und Kontakte
- ✅ Weitere kommunale Dienstleistungen

## 🔒 Sicherheit

- Environment Variables für API-Keys
- Input-Validierung mit Pydantic
- CORS-Konfiguration
- SQL-Injection Schutz durch ORM
- Error-Handling und Logging

## 📈 Monitoring & Logging

- Strukturiertes Logging mit Python Logging
- Health-Check Endpoint
- Database Connection Monitoring

## 🔄 Deployment

### Production-Ready Features

- ✅ Docker-basiertes Deployment
- ✅ Environment-basierte Konfiguration
- ✅ Health Checks
- ✅ Database Migrations (Alembic)
- ✅ Error Handling
- ✅ Logging

### Production Deployment

1. **Environment konfigurieren**
   ```bash
   ENVIRONMENT=production
   LOG_LEVEL=WARNING
   ```

2. **SSL/TLS konfigurieren** (mit nginx oder Traefik)

3. **Database Backups** einrichten

4. **Monitoring** aufsetzen (z.B. Prometheus, Grafana)

## 🧪 Testing

```bash
# Backend Tests
cd backend
pytest

# Frontend Tests
cd frontend
npm test
```

## ❓ FAQ

### Ist der Chatbot wirklich 100% kostenlos nutzbar?

**Ja!** Mit der Gemini + lokale Embeddings Konfiguration entstehen **keine API-Kosten**. Sie brauchen nur einen kostenlosen Gemini API-Key (keine Kreditkarte erforderlich). Siehe [Kostenlose Setup-Anleitung](docs/FREE_SETUP.md).

### Welche API-Keys brauche ich?

**Für kostenlosen Betrieb:**
- ✅ Google Gemini API-Key (kostenlos)
- ✅ Das war's!

**Optional (für bessere Qualität, aber kostenpflichtig):**
- Anthropic Claude API-Key (statt Gemini)
- OpenAI API-Key (nur für Embeddings, wenn nicht lokal)

### Gemini vs. Claude - was ist besser?

| Feature | Gemini (kostenlos) | Claude (bezahlt) |
|---------|-------------------|------------------|
| Kosten | **€0/Monat** | ~€30-50/Monat |
| Qualität | Sehr gut | Exzellent |
| Deutsch | ✅ Sehr gut | ✅ Exzellent |
| Limits | 1500 Anfragen/Tag | Praktisch unbegrenzt |

**Empfehlung:** Starten Sie mit Gemini. Upgraden Sie nur bei Bedarf.

### Was ist der Unterschied zwischen lokalen und OpenAI Embeddings?

- **Lokal**: Kostenlos, datenschutzfreundlich, sehr gut für Deutsch
- **OpenAI**: Minimal bessere Qualität, aber kostenpflichtig (~$0.13 per 1000 Dokumente)

Für kommunale Anwendungen sind lokale Embeddings vollkommen ausreichend.

### Wie wechsle ich zwischen Embedding-Providern?

1. `.env` anpassen: `EMBEDDING_PROVIDER=local` oder `openai`
2. Dimension in `backend/app/models/document.py` anpassen
3. Datenbank neu initialisieren
4. Daten neu importieren

Details: [docs/EMBEDDINGS.md](docs/EMBEDDINGS.md)

### Welches lokale Embedding-Modell soll ich nutzen?

Für deutsche Texte empfehlen wir:
- **Standard**: `paraphrase-multilingual-MiniLM-L12-v2` (schnell, gute Qualität)
- **Bessere Qualität**: `paraphrase-multilingual-mpnet-base-v2` (langsamer, sehr gut)

## 🤝 Beitragen

1. Fork das Repository
2. Feature Branch erstellen (`git checkout -b feature/AmazingFeature`)
3. Änderungen committen (`git commit -m 'Add AmazingFeature'`)
4. Branch pushen (`git push origin feature/AmazingFeature`)
5. Pull Request öffnen

## 📝 TODO / Roadmap

### Phase 2
- [ ] Benutzer-Authentifizierung
- [ ] Online-Terminvereinbarung
- [ ] Formular-Download Integration
- [ ] Multi-Language Support
- [ ] Voice Input/Output
- [ ] Admin-Dashboard

### Phase 3
- [ ] Analytics & Reporting
- [ ] Feedback-System
- [ ] Integration mit kommunalen Systemen
- [ ] Mobile App

## 📄 Lizenz

Dieses Projekt ist für die Stadt Rüsselsheim am Main entwickelt.

## 👥 Kontakt

Bei Fragen oder Problemen öffnen Sie bitte ein Issue im Repository.

## 🙏 Danksagungen

- Anthropic für Claude AI
- OpenAI für Embeddings
- pgvector Team für die PostgreSQL Extension
- FastAPI und React Communities

---

Entwickelt mit ❤️ für die Stadt Rüsselsheim am Main
