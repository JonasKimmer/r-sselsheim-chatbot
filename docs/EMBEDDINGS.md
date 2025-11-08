# Embedding-Konfiguration

Der Chatbot benötigt Embeddings (Textvektoren) für die semantische Suche im RAG-System. Es gibt verschiedene Optionen:

## Option 1: Lokale Embeddings (Standard) ⭐

**Vorteile:**
- ✅ Keine API-Keys erforderlich
- ✅ Kostenlos
- ✅ Datenschutzfreundlich (alles lokal)
- ✅ Unterstützt Deutsch sehr gut

**Konfiguration:**
```env
EMBEDDING_PROVIDER=local
LOCAL_EMBEDDING_MODEL=paraphrase-multilingual-MiniLM-L12-v2
```

**Hinweis:** Beim ersten Start wird das Modell (~400MB) automatisch heruntergeladen.

### Verfügbare lokale Modelle

1. **paraphrase-multilingual-MiniLM-L12-v2** (Standard)
   - Dimension: 384
   - Größe: ~420 MB
   - Sprachen: 50+ inkl. Deutsch
   - Geschwindigkeit: Schnell
   - Qualität: Gut

2. **paraphrase-multilingual-mpnet-base-v2**
   - Dimension: 768
   - Größe: ~1 GB
   - Sprachen: 50+ inkl. Deutsch
   - Geschwindigkeit: Mittel
   - Qualität: Sehr gut

3. **distiluse-base-multilingual-cased-v2**
   - Dimension: 512
   - Größe: ~500 MB
   - Sprachen: 15+ inkl. Deutsch
   - Geschwindigkeit: Schnell
   - Qualität: Gut

**Modell wechseln:**
```env
LOCAL_EMBEDDING_MODEL=paraphrase-multilingual-mpnet-base-v2
LOCAL_EMBEDDING_DIM=768
```

**WICHTIG:** Wenn Sie die Dimension ändern, müssen Sie auch `backend/app/models/document.py` anpassen:
```python
embedding = Column(Vector(768))  # Dimension anpassen
```

## Option 2: OpenAI Embeddings

**Vorteile:**
- ✅ Sehr hohe Qualität
- ✅ Kein lokaler Download nötig

**Nachteile:**
- ❌ API-Key erforderlich
- ❌ Kosten pro Request (~$0.00013 per 1K tokens)

**Konfiguration:**
```env
EMBEDDING_PROVIDER=openai
OPENAI_API_KEY=sk-...
OPENAI_EMBEDDING_MODEL=text-embedding-3-small
OPENAI_EMBEDDING_DIM=1536
```

**WICHTIG:** Passen Sie `backend/app/models/document.py` an:
```python
embedding = Column(Vector(1536))  # Für OpenAI
```

## Option 3: Google Gemini Embeddings

Google bietet auch Embeddings an, aber dafür müssten Sie einen eigenen Service implementieren.

**Schritte:**

1. **Erstellen Sie `backend/app/services/embedding_service_gemini.py`:**

```python
"""Gemini embedding service."""

import logging
from typing import List
import google.generativeai as genai

logger = logging.getLogger(__name__)


class GeminiEmbeddingService:
    """Service for generating embeddings using Google Gemini."""

    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = "models/embedding-001"  # Gemini embedding model

    def create_embedding(self, text: str) -> List[float]:
        result = genai.embed_content(
            model=self.model,
            content=text,
            task_type="retrieval_document"
        )
        return result['embedding']

    def create_embeddings(self, texts: List[str]) -> List[List[float]]:
        embeddings = []
        for text in texts:
            result = genai.embed_content(
                model=self.model,
                content=text,
                task_type="retrieval_document"
            )
            embeddings.append(result['embedding'])
        return embeddings
```

2. **requirements.txt erweitern:**
```
google-generativeai>=0.3.0
```

3. **Config anpassen (`backend/app/config.py`):**
```python
embedding_provider: str = "gemini"
gemini_api_key: str = ""
```

4. **RAG-Service anpassen (`backend/app/services/rag_service.py`):**
```python
elif settings.embedding_provider == "gemini":
    from .embedding_service_gemini import GeminiEmbeddingService
    self.embedding_service = GeminiEmbeddingService(settings.gemini_api_key)
```

5. **Document Model anpassen:**
```python
embedding = Column(Vector(768))  # Gemini embedding dimension
```

## Empfehlung für Rüsselsheim-Chatbot

**Start:** Nutzen Sie **lokale Embeddings** (Option 1)
- Kein API-Key erforderlich
- Kostenlos
- Sehr gute Deutsch-Unterstützung
- Schnell genug für kommunale Anfragen

**Production:** Testen Sie beide Varianten und wählen Sie basierend auf:
- Budget (lokal = kostenlos, OpenAI = ~$0.10 pro 1000 Anfragen)
- Qualität (OpenAI minimal besser, aber lokal ausreichend)
- Datenschutz (lokal bevorzugt für kommunale Daten)

## Wechsel zwischen Embedding-Providern

Wenn Sie den Provider wechseln:

1. **Backup der Datenbank** erstellen
2. **Tabellen löschen:**
   ```bash
   make shell-db
   DROP TABLE documents;
   \q
   ```
3. **Dimension in `document.py` anpassen**
4. **`.env` aktualisieren**
5. **Services neu starten:**
   ```bash
   make down
   make up
   ```
6. **Daten neu importieren:**
   ```bash
   make import-data
   ```

## Performance-Vergleich

| Provider | Dimension | Kosten/1K Docs | Qualität (DE) | Geschwindigkeit |
|----------|-----------|----------------|---------------|-----------------|
| Local (MiniLM) | 384 | Kostenlos | ⭐⭐⭐⭐ | ⚡⚡⚡ |
| Local (MPNet) | 768 | Kostenlos | ⭐⭐⭐⭐⭐ | ⚡⚡ |
| OpenAI | 1536 | ~$0.13 | ⭐⭐⭐⭐⭐ | ⚡⚡⚡ |
| Gemini | 768 | ~$0.025 | ⭐⭐⭐⭐ | ⚡⚡⚡ |

## Troubleshooting

### "Dimension mismatch" Fehler
➡️ Stellen Sie sicher, dass die Dimension in `document.py` mit Ihrer Konfiguration übereinstimmt.

### Lokales Modell lädt nicht
➡️ Prüfen Sie Internetverbindung. Beim ersten Start wird das Modell von HuggingFace heruntergeladen.

### OpenAI Embeddings schlagen fehl
➡️ Prüfen Sie Ihren API-Key und ob Sie Credits haben.

## Fragen?

Öffnen Sie ein Issue im Repository oder kontaktieren Sie das Development-Team.
