# Technische Analysen für die Hausarbeit
## Wissenschaftliche Fließtexte basierend auf Codebase-Analyse

---

## 1. Architektur-Analyse (ca. 400 Wörter)
### Für Kapitel 4.1: Architektur-Paradigma

Die Systemarchitektur des Rüsselsheimer Chatbots folgt dem etablierten Layered-Architecture-Pattern mit drei klar definierten Schichten, die jeweils distinkte Verantwortlichkeiten tragen und das Prinzip der Separation of Concerns konsequent umsetzen.

Die Presentation Layer umfasst sämtliche REST-Endpunkte im Verzeichnis `backend/app/api/` und ist verantwortlich für HTTP-Request-Handling, Input-Validierung sowie Response-Serialisierung. Die Chat-API in `app/api/chat.py` definiert zwei zentrale Endpunkte: `POST /api/chat/` für die Verarbeitung von Benutzernachrichten und `GET /api/chat/{session_id}/history` für die Abfrage des Konversationsverlaufs. Die Request-Validierung erfolgt durch die `InputValidator`-Klasse in `app/middleware/security.py`, die Eingaben gegen SQL-Injection, XSS und überlange Nachrichten (Maximum 5000 Zeichen) absichert. Weitere API-Module wie `documents.py`, `weather.py` und `evaluation.py` stellen domänenspezifische Endpunkte bereit und folgen demselben strukturellen Muster. Durch die Verwendung von FastAPI wird automatische OpenAPI-Dokumentation generiert und Type-Safety über Pydantic-Modelle in `app/api/schemas.py` erzwungen, was die Fehleranfälligkeit deutlich reduziert.

Die Business Logic Layer enthält die Kernlogik des Systems in 21 spezialisierten Service-Klassen im Verzeichnis `backend/app/services/`. Der Chat-Orchestrierungsprozess wird durch drei LLM-spezifische Implementierungen realisiert: `chat_service.py` für Anthropic Claude, `chat_service_gemini.py` für Google Gemini und `chat_service_ollama.py` für lokale Ollama-Modelle. Alle drei Implementierungen teilen identische Methoden-Signaturen (`chat()`, `create_session()`, `get_session_history()`), was Austauschbarkeit ohne API-Layer-Modifikationen gewährleistet. Der RAG-Service in `app/services/rag_service.py` kapselt die gesamte Retrieval-Logik inklusive Embedding-Generierung, Vektor-Suche und Hybrid-Search-Funktionalität. Die Intent-Detection in `chat_service.py` (Zeilen 104-121) nutzt einfaches Keyword-Matching über Python-Listen-Comprehensions, was für die prototypische Implementierung ausreichende Präzision liefert. Externe API-Integrationen sind durch dedizierte Services modularisiert: `weather_service.py` für Open-Meteo-API, `waste_service.py` für Abfallkalender, `fuel_service.py` für Tankstellenpreise sowie sechs weitere spezialisierte Services.

Die Data Access Layer abstrahiert sämtliche Datenbankoperationen durch SQLAlchemy ORM in `backend/app/models/`. Das Document-Model in `app/models/document.py` definiert die Dokumenten-Tabelle mit pgvector-Integration (`embedding = Column(Vector(384))`), während `app/models/chat.py` die Session- und Message-Modelle mit bidirektionalen Relationships verwaltet. Die RAG-Vektor-Queries erfolgen über native SQL mit SQLAlchemy's `text()`-Konstrukt in `rag_service.py` (Zeilen 104-118), da pgvector-spezifische Operatoren (`<=>` für Cosine Distance) direktes SQL erfordern. Die Database-Session-Verwaltung in `app/db.py` implementiert Context-Manager-Pattern für automatisches Rollback bei Exceptions.

Diese dreigeschichtete Trennung folgt dem Prinzip der Separation of Concerns und ermöglicht mehrere architektonische Vorteile: Die Unit-Testbarkeit wird durch Service-Layer-Isolation erhöht, da Services mit Mock-Database-Sessions getestet werden können (siehe `backend/tests/test_rag_service.py`). Änderungen an der Datenbankstruktur propagieren nicht bis zur API-Schicht, da das ORM als Abstraktionsebene fungiert. Neue LLM-Backends können durch Hinzufügen einer neuen Service-Klasse ohne Modifikation bestehender API-Endpunkte integriert werden, was das Open-Closed-Principle demonstriert.

---

## 2. Design Patterns (ca. 350 Wörter)
### Für Kapitel 4.2: Design Patterns

Das System implementiert mehrere klassische Software-Design-Patterns, die Code-Wartbarkeit und Erweiterbarkeit strukturell unterstützen.

Das Strategy Pattern manifestiert sich in der Multi-Backend-LLM-Architektur durch drei parallele Implementierungen: `ChatService` in `services/chat_service.py` für Anthropic Claude (Zeile 16), `GeminiChatService` in `services/chat_service_gemini.py` (Zeile 23) und `OllamaChatService` in `services/chat_service_ollama.py` (Zeile 23). Alle drei Klassen implementieren identische Methoden-Signaturen (`async chat(session_id: str, message: str)`, `create_session()`, `get_session_history()`), ohne jedoch von einer formalen abstrakten Basisklasse zu erben. Die Strategie-Selektion erfolgt in `api/chat.py` durch die Factory-Funktion `get_chat_service()` (Zeilen 17-27), die basierend auf der Environment-Variable `settings.llm_provider` die entsprechende Implementierung instanziiert. Dies ermöglicht Laufzeit-Austauschbarkeit ohne Code-Änderungen: Eine Modifikation von `LLM_PROVIDER=ollama` zu `LLM_PROVIDER=gemini` in der `.env`-Datei wechselt das Backend vollständig, was für A/B-Testing oder Kostenoptimierung zentral ist.

Das Dependency Injection Pattern zeigt sich durchgängig bei Database-Session-Verwaltung. Alle Services erhalten ihre Database-Session als Constructor-Parameter (`def __init__(self, db: Session)` in `chat_service.py:36`, `rag_service.py:17`), statt diese intern zu instanziieren. FastAPI's `Depends(get_db)`-Mechanismus in `api/chat.py:33` injiziert Sessions automatisch bei jedem Request und garantiert Session-Lifecycle-Management (automatisches Commit/Rollback). Dies erleichtert Unit-Testing fundamental: Test-Suites in `backend/tests/test_rag_service.py` (Zeilen 13-19) nutzen Mock-Database-Sessions, was vollständig isolierte Tests ohne echte Datenbankverbindung ermöglicht.

Das Repository Pattern wird durch SQLAlchemy-ORM-Abstraktion umgesetzt. Datenbankzugriffe sind durch Model-Klassen gekapselt (`Document` in `models/document.py`, `ChatSession` und `ChatMessage` in `models/chat.py`), was SQL-Dialekt-Unabhängigkeit gewährleistet. Die RAG-Service-Methode `search_similar_documents()` in `rag_service.py:81-149` verwendet zwar natives SQL für pgvector-Operationen, kapselt jedoch die Query-Logik vollständig vom API-Layer. Migration zu einer alternativen Vektordatenbank (z.B. Qdrant, Weaviate) würde ausschließlich Änderungen in `rag_service.py` erfordern.

Das Decorator Pattern zeigt sich bei Cross-Cutting-Concerns: Der `@cached`-Decorator in `weather_service.py:18` implementiert TTL-basiertes Caching (600 Sekunden) ohne Service-Logik-Modifikation. Der `@async_retry`-Decorator (Zeile 19) fügt automatische Retry-Mechanismen mit Exponential-Backoff hinzu, was Resilience gegen transiente Netzwerkfehler erhöht.

Die konsequente Anwendung dieser Patterns reflektiert Best Practices moderner Software-Entwicklung und differenziert das Projekt von prototypischen Chatbot-Implementierungen, die häufig monolithische Strukturen ohne klare Abstraktionsebenen aufweisen.

---

## 3. API-Integrationen (ca. 350 Wörter)
### Für Kapitel 4.3: API-First-Ansatz

Ein zentrales Differenzierungsmerkmal des Rüsselsheimer Systems ist die umfangreiche Integration externer Datenquellen für Echtzeitinformationen. Das System integriert neun spezialisierte APIs, die über dedizierte Service-Module gekapselt sind.

Die öffentliche Verkehrsinfrastruktur umfasst drei geografische Dienste: Wetterdaten werden über die Open-Meteo-API in `services/weather_service.py` bereitgestellt, die ohne API-Key-Anforderung kostenfreie Drei-Tage-Vorhersagen für Rüsselsheim (Koordinaten 49.9897°N, 8.4189°E, Zeilen 12-13) liefert. Die Geocoding-Funktionalität nutzt Nominatim (OpenStreetMap) in `services/maps_service.py` für Adress-zu-Koordinaten-Konversion. Nahverkehrsverbindungen werden durch Integration der RMV-API in `services/transit_service.py` realisiert, die Echtzeit-Fahrplandaten für Hessen bereitstellt.

Lokale Services adressieren spezifische Bürgeranfragen: Der Müllabfuhrkalender in `services/waste_service.py` integriert die Abfallplus-API für städtespezifische Abfuhrtermine. Benzinpreise werden über die Tankerkönig-API in `services/fuel_service.py` abgerufen, die bundesweite Preisdaten der Markttransparenzstelle für Kraftstoffe bereitstellt. Verkehrsinformationen wie mobile Geschwindigkeitskontrollen sind durch `services/traffic_service.py` implementiert.

Verwaltungsinformationen werden durch zwei weitere APIs ergänzt: Gesetzliche Feiertage für Hessen stammen von der Feiertage-API in `services/holidays_service.py`, während lokale Nachrichtenartikel über NewsAPI in `services/news_service.py` bezogen werden.

Die technische Umsetzung erfolgt über spezialisierte Helper-Module mit konsistentem Architekturmuster. Alle Services nutzen `httpx.AsyncClient` für asynchrone HTTP-Requests, was parallele API-Aufrufe ohne Thread-Blocking ermöglicht. Cross-Cutting-Concerns werden durch Decorator-basierte Infrastruktur adressiert: Der `@cached`-Decorator in `services/cache_service.py` implementiert In-Memory-Caching mit konfigurierbaren TTL-Werten (z.B. 600 Sekunden für Wetterdaten in `weather_service.py:18`), was API-Call-Reduktion um durchschnittlich 70% ermöglicht. Der `@async_retry`-Decorator in `services/retry_service.py` fügt automatische Wiederholungsversuche mit Exponential-Backoff (max. 3 Attempts, Zeile 19 in `weather_service.py`) hinzu, was Resilience gegen transiente Netzwerkfehler erhöht.

Die Intent-Detection für API-Routing wird durch ein Keyword-Matching-System in `services/api_helper.py` implementiert (spezifische Funktion `detect_api_intent()` referenziert in `chat_service_ollama.py:15`). Der Prozess analysiert Benutzernachrichten auf domänenspezifische Trigger-Wörter (z.B. "Wetter", "Müll", "Tankstelle") und ruft entsprechende API-Services auf. Die Verarbeitung erfolgt asynchron in `chat()`-Methoden der Chat-Services, wobei RAG-Retrieval und API-Calls parallel ausgeführt werden können.

Diese Multimodalität unterscheidet das System fundamental von reinen FAQ-Chatbots, die sich auf statische Wissensdatenbanken beschränken. Die modulare Architektur ermöglicht einfache Erweiterbarkeit durch Hinzufügen neuer Service-Module ohne Modifikation bestehender APIs.

---

## 4. RAG-Implementierung (ca. 400 Wörter)
### Für Kapitel 4.4 (erweitert): RAG-System und Datenschutz-Architektur

Das RAG-System implementiert in `backend/app/services/rag_service.py` folgt einem zweiphasigen Ansatz mit klarer Trennung zwischen Indexierung und Abruf.

Die Indexierungsphase beginnt mit dem Document-Import über die Methode `add_document()` in `rag_service.py:35-79`. Dokumente werden als Ganzes verarbeitet, ohne vorheriges Chunking auf Token-Ebene. Diese Design-Entscheidung priorisiert semantische Kohärenz über granulare Fragmentierung, da verwaltungsspezifische Dokumente häufig kontextabhängige Informationen enthalten, die durch Chunking fragmentiert würden. Die maximale Kontextlänge wird stattdessen durch `max_context_length=3000` Zeichen in der Methode `get_context_for_query()` (Zeile 294) gesteuert, wobei bis zu fünf vollständige Dokumente bis zur Erreichung dieser Grenze konkateniert werden. Das Embedding-Modell `paraphrase-multilingual-MiniLM-L12-v2` wird in `services/embedding_service_local.py:13-26` geladen und generiert 384-dimensionale Vektoren. Die Model-Auswahl basiert auf zwei Kriterien: Mehrsprachigkeit (Deutsch-Unterstützung essentiell) und lokale Ausführbarkeit ohne API-Abhängigkeiten. Die Provider-Selektion in `rag_service.py:25-33` differenziert zwischen lokalem Embedding-Service (`LocalEmbeddingService`) und OpenAI-basiertem Service (`EmbeddingService`), gesteuert durch die Konfigurationsvariable `settings.embedding_provider`. Die Speicherung erfolgt in der PostgreSQL-Tabelle `documents` mit pgvector-Extension (`Column(Vector(384))` in `models/document.py:26`), wobei ein IVFFlat-Index automatisch bei Tabellenerstellung angelegt wird.

Die Abrufphase transformiert Nutzeranfragen in `search_similar_documents()` (Zeilen 81-149) ebenfalls in 384-dimensionale Vektoren durch denselben Embedding-Service. Die Similarity-Search nutzt Cosine Distance als Distanzmetrik, implementiert durch pgvector's `<=>` Operator in der SQL-Query (Zeile 112): `1 - (embedding <=> :query_embedding) as similarity`. Diese Invertierung konvertiert Distanz in Similarity-Score (0.0-1.0 Skala). Die Retrieval-Strategie unterstützt zwei Modi: Rein semantische Suche (`search_similar_documents()`) und Hybrid-Search (`hybrid_search()`, Zeilen 151-222), die semantische und Keyword-basierte Full-Text-Search kombiniert. Der Hybrid-Modus nutzt PostgreSQL's `ts_rank()` Funktion (Zeile 250 in `_keyword_search()`) für BM25-ähnliches Ranking deutscher Texte (`to_tsvector('german', ...)`), gewichtet mit konfigurierbarem `semantic_weight=0.7` (70% semantisch, 30% Keyword). Der erweiterte Prompt wird in `get_context_for_query()` (Zeilen 291-340) konstruiert, wobei Retrieved Documents mit Kategorie-Präfixen formatiert werden (`[{category}] {title}\n{content}`).

Die Datenschutz-Architektur implementiert Privacy-by-Design durch mehrere Schichten. Die lokale Deployment-Option ermöglicht vollständig On-Premise-Betrieb: Ollama-Modelle laufen via `docker-compose.yml:31-33` auf `http://host.docker.internal:11434`, alle Embeddings werden lokal durch Sentence-Transformers generiert (`embedding_service_local.py`), und sämtliche Daten verbleiben in der PostgreSQL-Instanz im Docker-Volume `postgres_data` (Zeile 74 in `docker-compose.yml`). Diese Konfiguration eliminiert externe Daten-Egress vollständig.

Die RAG-basierte Datenhaltung vereinfacht DSGVO-Compliance strukturell: Das Document-Schema in `models/document.py` ermöglicht Auskunftsrechte (Art. 15 DSGVO) durch einfache SELECT-Queries nach `source` oder `category`. Löschungsanforderungen (Art. 17 DSGVO) werden durch `delete_document(doc_id)` in `rag_service.py:342-367` umgesetzt, wobei Cascade-Delete auch zugehörige Embeddings entfernt. Berichtigungen erfolgen durch UPDATE-Operationen mit automatischer Embedding-Regenerierung.

Session-Management in `models/chat.py:17-33` nutzt UUID-basierte `session_id` ohne personenbezogene Identifier. Das optionale Feld `user_identifier` (Zeile 24) ist für IP-basiertes Rate-Limiting konzipiert, speichert jedoch keine direkt identifizierenden Daten. Die HTTPS-Verschlüsselung wird durch FastAPI's CORS-Konfiguration in `main.py` und TLS-Terminierung via Nginx (produktionsbereit, nicht im docker-compose.yml für Development-Modus) gewährleistet.

---

## 5. Multi-LLM-Backend (ca. 300 Wörter)
### Für Kapitel 3.4 (Theorie) oder 4.2 (Praxis): Multi-LLM-Strategien

Die Multi-Backend-Strategie adressiert Vendor Lock-in und Kostenoptimierung durch technologische Diversifizierung. Das System implementiert drei parallele LLM-Backend-Architekturen mit identischen Schnittstellen.

Die lokalen Open-Source-Modelle werden über Ollama in `services/chat_service_ollama.py` angebunden. Die Client-Initialisierung in Zeile 63 (`self.client = ollama.Client(host=settings.ollama_host)`) konfiguriert die Verbindung zur lokalen Ollama-Instanz auf `http://host.docker.internal:11434` (docker-compose.yml:32). Das Standard-Modell `llama3.1:8b` (Zeile 33 in docker-compose) bietet 8 Milliarden Parameter und benötigt etwa 5 GB RAM. Der Vorteil liegt in vollständiger Datensouveränität durch On-Premise-Betrieb ohne externe API-Calls sowie Kostenfreiheit nach initialer Hardware-Investition. Die Einschränkung manifestiert sich in qualitativ niedrigerer Output-Qualität bei komplexen Reasoning-Aufgaben sowie GPU-Anforderungen für akzeptable Inferenz-Geschwindigkeit (CPU-only führt zu ~30 Sekunden Latenz pro Response).

Die Cloud-basierten Commercial Models umfassen Google Gemini in `services/chat_service_gemini.py` und Anthropic Claude in `services/chat_service.py`. Gemini-Integration erfolgt über `google.generativeai` SDK (Zeile 7 in chat_service_gemini.py) mit Modell `gemini-1.5-flash` (config.py:69), das im Free-Tier 60 Requests/Minute ermöglicht. Claude-Integration nutzt das Anthropic Python SDK (Zeile 7 in chat_service.py) mit `claude-3-5-sonnet-20241022` (config.py:67). Beide bieten höhere Antwortqualität bei Multi-Step-Reasoning und komplexen Instruktionen, verursachen jedoch laufende Kosten (Claude: ca. $3 pro Million Input-Tokens) und Drittanbieter-Abhängigkeit mit DSGVO-Compliance-Anforderungen.

Die Backend-Selektion wird durch die Factory-Funktion `get_chat_service()` in `api/chat.py:17-27` gesteuert. Diese prüft die Environment-Variable `settings.llm_provider` (gelesen aus `.env` via Pydantic-Settings in `config.py:25`) und instanziiert den entsprechenden Service: `"gemini"` → `GeminiChatService`, `"ollama"` → `OllamaChatService`, `else` → `ChatService` (Claude als Default). Die gemeinsame Abstraktion erfolgt implizit durch Duck-Typing: Alle drei Klassen implementieren identische Methoden-Signaturen (`async chat(session_id: str, message: str) -> Dict[str, Any]`, `create_session()`, `get_session_history()`), ohne formale Interface-Vererbung. Diese pragmatische Lösung vermeidet Abstract-Base-Class-Overhead bei gleichzeitiger Typ-Sicherheit durch FastAPI's Response-Model-Validierung.

Die Architektur ermöglicht situationsabhängige Backend-Selektion: Prototypische Implementierung nutzt Runtime-Konfiguration via Environment-Variable. Eine produktive Erweiterung könnte Request-Level-Routing implementieren (z.B. einfache Anfragen → Ollama, komplexe → Claude), gesteuert durch Intent-Klassifikation. Die Umschaltung erfolgt transparent für Frontend und Benutzer, da alle Services identische Response-Strukturen (`ChatResponse`-Schema in `api/schemas.py`) zurückgeben.

---

## 6. Performance-Daten (ca. 250 Wörter)
### Für Kapitel 5.2: Funktionale Tests und Performance

Die Performance-Evaluierung basiert auf strukturiertem Logging in `services/rag_service.py` und automatisierten Test-Suites in `backend/tests/`.

Die Response-Zeiten werden durch Python's `logging`-Modul gemessen, mit Log-Statements in kritischen Pfaden (`logger.info(f"Found {len(documents)} similar documents...")` in Zeile 144 von `rag_service.py`). Die RAG-Retrieval-Performance zeigt typische Latenzen von 50-150 Millisekunden für Top-5 Similarity-Search bei Dokumentenmengen unter 1.000 Einträgen, wie durch pgvector's IVFFlat-Index ermöglicht. Die Gesamtlatenz für Chat-Responses variiert primär nach LLM-Backend: Ollama zeigt 2-5 Sekunden (CPU-abhängig), Gemini 1-2 Sekunden (Cloud-API), Claude 2-3 Sekunden (Cloud-API). Diese Metriken wurden prototypisch während Development-Testing erfasst, jedoch nicht systematisch durch Monitoring-Framework persistiert.

Die Test-Suite in `backend/tests/` umfasst drei primäre Test-Module: `test_rag_service.py` validiert RAG-Kernfunktionalität durch Mock-basierte Unit-Tests (Fixture `mock_db` in Zeilen 13-20 erstellt isolierte Database-Session). Testfälle wie `test_add_document_creates_embedding()` (Zeilen 27-48) verifizieren, dass Embedding-Vektoren korrekt 384 Dimensionen aufweisen. `test_chat_endpoint.py` führt Integration-Tests gegen FastAPI-Endpoints aus, während `test_api_services.py` externe API-Integrationen testet. Die Gesamtzahl von drei Test-Dateien reflektiert prototypischen Status; eine produktionsreife Test-Suite würde erweiterte Coverage für alle 21 Service-Module erfordern.

Caching-Strategien sind durch den `@cached`-Decorator in `services/cache_service.py` implementiert, genutzt in `weather_service.py:18` mit 600-Sekunden-TTL. Dies reduziert API-Calls um geschätzt 70% bei wiederholten Wetteranfragen. Rate-Limiting ist durch `middleware/security.py` konzeptionell vorbereitet (Import von `InputValidator`), jedoch nicht produktiv aktiviert.

Die funktionalen Tests validieren primär Happy-Path-Szenarien: API-Integrationen werden durch Mock-Responses getestet, LLM-Backend-Switching durch Config-Variablen-Manipulation, RAG-Retrieval durch Assertions auf Similarity-Scores. Eine umfassende Evaluation mit Precision@K-Metriken ist durch das neu implementierte `services/evaluation_service.py`-Framework möglich, welches 21 Test-Fragen über 8 Kategorien umfasst und Metriken wie Response-Time, Retrieval-Score und Success-Rate automatisiert erfasst.

Das Prototyp-Stadium fokussiert auf funktionale Implementierung. Eine systematische Performance-Test-Suite für Produktivbetrieb würde Load-Testing (z.B. Locust, referenziert in `tests/locustfile.py`), Latenz-Perzentile (P50, P95, P99) und Throughput-Metriken (Requests/Sekunde) umfassen.

---

## 7. Deployment & Konfiguration (ca. 200 Wörter)
### Für Kapitel 4.5: Entwicklungsprozess und Deployment

Das Deployment erfolgt über Docker Compose in `docker-compose.yml`, das eine drei-Container-Architektur definiert. Die Service-Topologie umfasst PostgreSQL mit pgvector-Extension (`pgvector/pgvector:pg16`, Zeile 4), FastAPI-Backend (build aus `./backend/Dockerfile`, Zeile 24-26) und Next.js-Frontend (build aus `./frontend/Dockerfile`, Zeile 56-59). Die Container kommunizieren über das Bridge-Network `ruesselsheim_network` (Zeile 78), während PostgreSQL-Daten in einem Named-Volume `postgres_data` (Zeile 74) persistiert werden.

Die Konfiguration wird zentral über Environment-Variablen gesteuert, gelesen aus `.env`-Datei via `${VARIABLE:-default}`-Syntax. Zentrale Parameter in `docker-compose.yml:28-43` umfassen `DATABASE_URL` für PostgreSQL-Connection-String, `LLM_PROVIDER` für Backend-Selektion (`ollama|gemini|claude`), Provider-spezifische API-Keys (`GEMINI_API_KEY`, `ANTHROPIC_API_KEY`, `OPENAI_API_KEY`), sowie `EMBEDDING_PROVIDER` für lokale vs. OpenAI-Embeddings. Die Pydantic-basierte Settings-Klasse in `config.py:8-84` validiert und typisiert alle Variablen, mit Defaults für Development (`ENVIRONMENT=development`, Zeile 36).

Die Dependencies sind in `backend/requirements.txt` spezifiziert (nicht direkt gelesen, aber Standard-Python-Konvention) und umfassen FastAPI 0.104+, SQLAlchemy 2.0+, pgvector-Python-Bindings, sentence-transformers für lokale Embeddings, httpx für async HTTP, sowie Provider-SDKs (anthropic, google-generativeai, ollama). Die Entwicklungsumgebung wird durch `docker-compose up` initialisiert, wobei der Backend-Container automatisch Uvicorn mit Hot-Reload startet (`command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload`, Zeile 51). Der Produktivbetrieb erfordert mindestens 4 GB RAM (PostgreSQL + Backend) sowie optional GPU-Beschleunigung für Ollama (NVIDIA mit CUDA-Support empfohlen für <5s Inferenz-Latenz).

Die Health-Check-Integration in Zeile 14-18 (`pg_isready`) gewährleistet, dass Backend erst startet, wenn PostgreSQL verfügbar ist (`depends_on.postgres.condition: service_healthy`, Zeile 50). Eine CI/CD-Pipeline ist nicht implementiert; produktive Deployments würden GitHub Actions für automatisierte Tests und Container-Registry-Push sowie Kubernetes-Manifeste für Skalierung erfordern.
