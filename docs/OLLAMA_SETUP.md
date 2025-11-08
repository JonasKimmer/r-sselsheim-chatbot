# 🦙 Ollama Setup - 100% Kostenlos & Lokal

Ollama ist die **beste kostenlose Option** für diesen Chatbot! Alle Daten bleiben auf Ihrem Computer.

## 🌟 Warum Ollama?

| Feature | Ollama (Lokal) | Gemini (Cloud) | Claude (Cloud) |
|---------|---------------|----------------|----------------|
| **Kosten** | 100% kostenlos | Kostenlos (Limits) | €€€ Bezahlt |
| **Datenschutz** | ✅ 100% lokal | ❌ Google Server | ❌ Anthropic Server |
| **Limits** | ✅ Unbegrenzt | 1500 Anfragen/Tag | API-abhängig |
| **Internet** | ✅ Offline nutzbar | ❌ Benötigt Internet | ❌ Benötigt Internet |
| **Geschwindigkeit** | ✅ Sehr schnell (lokal) | Mittel (API) | Langsam (API) |
| **Qualität** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

**Empfehlung:** Ollama ist perfekt für kommunale Anwendungen mit Datenschutzanforderungen!

## 📋 Systemanforderungen

### Minimum:
- **RAM:** 8 GB (für 8B Modelle)
- **Speicher:** 5 GB frei
- **System:** macOS (M1/M2/M3/M4), Linux, Windows

### Empfohlen (für Ihre M4 mit 24GB):
- **RAM:** 16+ GB (Sie haben 24GB ✅)
- **Speicher:** 10+ GB
- **Modell:** llama3.1:8b oder llama3.1:70b

## 🚀 Installation

### 1. Ollama installieren (Mac M4)

Sie haben Ollama bereits installiert! ✅

Falls nicht:
```bash
# Mac M4:
brew install ollama

# oder von Website:
# https://ollama.ai/download
```

### 2. Ollama starten

**Automatischer Start (empfohlen):**
```bash
# Ollama als Service im Hintergrund starten
ollama serve
```

Dies läuft bereits bei Ihnen:
```
Listening on 127.0.0.1:11434
Available at http://127.0.0.1:11434
```

### 3. Llama 3.1 8B Modell herunterladen

```bash
# Llama 3.1 8B (empfohlen, ~4.7 GB)
ollama pull llama3.1:8b

# Prüfen ob das Modell da ist:
ollama list
```

**Erwartete Ausgabe:**
```
NAME              ID              SIZE      MODIFIED
llama3.1:8b      42182419e950    4.7 GB    2 minutes ago
```

### Alternative Modelle:

```bash
# Kleiner & schneller (gut für Tests):
ollama pull llama3.2:3b  # ~2 GB

# Größer & bessere Qualität (wenn genug RAM):
ollama pull llama3.1:70b  # ~40 GB (!)

# Deutsches Modell (optional):
ollama pull leo-hessianai:8b  # Speziell für Deutsch trainiert
```

## ⚙️ Chatbot konfigurieren

### 1. .env Datei erstellen/anpassen

```bash
cp .env.example .env
nano .env
```

### 2. Ollama konfigurieren

**Minimale Konfiguration (Ollama + Lokale Embeddings):**

```env
# ============================================
# LLM: Ollama (100% kostenlos, lokal)
# ============================================
LLM_PROVIDER=ollama

# Ollama Server (läuft auf Ihrem Mac)
OLLAMA_HOST=http://host.docker.internal:11434
OLLAMA_MODEL=llama3.1:8b

# ============================================
# Embeddings: Lokal (100% kostenlos)
# ============================================
EMBEDDING_PROVIDER=local

# ============================================
# Datenbank (Standard)
# ============================================
POSTGRES_USER=ruesselsheim_bot
POSTGRES_PASSWORD=change_me_in_production
POSTGRES_DB=ruesselsheim_chatbot
```

**Wichtig:**
- `OLLAMA_HOST=http://host.docker.internal:11434` - Dies verbindet den Docker Container mit Ihrem Mac
- Für lokales Testen (ohne Docker): `OLLAMA_HOST=http://127.0.0.1:11434`

### 3. Backend neu bauen & starten

```bash
# Container neu bauen (wegen neuer ollama Python-Bibliothek)
docker-compose build backend

# Alles starten
docker-compose up -d

# Testdaten importieren
docker-compose exec backend python scripts/import_data.py
```

## 🧪 Testen

### 1. Prüfen ob Ollama läuft:

```bash
# Direkt auf dem Mac:
curl http://127.0.0.1:11434/api/version

# Sollte antworten mit:
# {"version":"0.1.x"}
```

### 2. Test Chat:

```bash
# Einfacher Test mit Ollama CLI:
ollama run llama3.1:8b "Was sind die Öffnungszeiten des Bürgerservices in Rüsselsheim?"
```

### 3. Backend-Logs prüfen:

```bash
docker-compose logs -f backend

# Sollte zeigen:
# INFO: Ollama chat service initialized
# INFO: Using model llama3.1:8b at http://host.docker.internal:11434
```

### 4. Im Browser testen:

1. **Frontend öffnen:** http://localhost:5173
2. **Nachricht senden:** "Hallo, welche Dienstleistungen bietet Rüsselsheim?"
3. **Antwort erwarten** (ca. 2-5 Sekunden mit M4)

## 🎯 Modell-Vergleich

Ihre M4 mit 24GB kann alle diese Modelle ausführen:

| Modell | Größe | RAM | Qualität | Geschwindigkeit | Deutsch |
|--------|-------|-----|----------|----------------|---------|
| **llama3.2:3b** | ~2 GB | 4+ GB | ⭐⭐⭐ | ⚡⚡⚡ Sehr schnell | ⭐⭐⭐ |
| **llama3.1:8b** ✅ | ~4.7 GB | 8+ GB | ⭐⭐⭐⭐ | ⚡⚡ Schnell | ⭐⭐⭐⭐ |
| **llama3.1:70b** | ~40 GB | 48+ GB | ⭐⭐⭐⭐⭐ | ⚡ Langsam | ⭐⭐⭐⭐⭐ |
| **mistral:7b** | ~4.1 GB | 8+ GB | ⭐⭐⭐⭐ | ⚡⚡ Schnell | ⭐⭐⭐ |
| **leo-hessianai:8b** | ~4.7 GB | 8+ GB | ⭐⭐⭐⭐ | ⚡⚡ Schnell | ⭐⭐⭐⭐⭐ |

**Empfehlung für Sie:**
- **Produktion:** `llama3.1:8b` - Beste Balance aus Qualität und Geschwindigkeit
- **Entwicklung:** `llama3.2:3b` - Schneller für Tests
- **Beste Qualität:** `mistral:7b` - Ähnliche Größe wie llama3.1:8b, oft bessere Antworten

### Modell wechseln:

```env
# In .env ändern:
OLLAMA_MODEL=mistral:7b

# Modell herunterladen:
ollama pull mistral:7b

# Backend neu starten:
docker-compose restart backend
```

## 🔧 Performance-Optimierung

### 1. Ollama Performance Settings

Erstellen Sie `~/.ollama/config.json`:

```json
{
  "num_parallel": 4,
  "num_gpu": 1,
  "num_thread": 8
}
```

Für M4 optimiert:
```json
{
  "num_parallel": 2,
  "num_gpu": 1,
  "num_thread": 10
}
```

### 2. Modell im RAM behalten

```bash
# Modell vorladen (bleibt im RAM):
ollama run llama3.1:8b ""

# Dann läuft der Chatbot sofort ohne Ladezeit
```

### 3. Docker Memory Limits

In `docker-compose.yml` optimieren:

```yaml
backend:
  # ...
  deploy:
    resources:
      limits:
        memory: 4G
      reservations:
        memory: 2G
```

## 📊 Monitoring

### Ollama Logs:

```bash
# Mac Terminal (wo Ollama läuft):
# Zeigt alle Anfragen in Echtzeit
```

### Backend Logs:

```bash
docker-compose logs -f backend

# Suchen nach Ollama-Requests:
docker-compose logs backend | grep -i ollama
```

### Performance messen:

```bash
# Zeit messen für eine Anfrage:
time curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Was sind die Öffnungszeiten?", "session_id": "test"}'
```

**Erwartete Zeiten (M4):**
- Erste Anfrage: 3-5 Sekunden (Modell laden)
- Folge-Anfragen: 1-2 Sekunden

## 🆚 Ollama vs. Cloud LLMs

### Datenschutz-Vergleich:

| Aspekt | Ollama | Gemini | Claude |
|--------|--------|--------|--------|
| **Daten verlassen Server** | ❌ Nein | ✅ Ja | ✅ Ja |
| **DSGVO-konform** | ✅ Vollständig | ⚠️ Komplex | ⚠️ Komplex |
| **Audit-Log** | ✅ Lokal | ❌ Google | ❌ Anthropic |
| **Für Behörden geeignet** | ✅ Ja | ⚠️ Eingeschränkt | ⚠️ Eingeschränkt |

### Kosten-Vergleich:

**Szenario:** 5000 Anfragen/Tag

| Lösung | Monatliche Kosten |
|--------|------------------|
| **Ollama** | €0 (nur Strom: ~€2) |
| **Gemini** | €0 (aber Limits!) |
| **Claude** | ~€150-300 |

## ⚠️ Troubleshooting

### Problem: "Connection refused to 127.0.0.1:11434"

**Lösung:**
```bash
# Prüfen ob Ollama läuft:
ps aux | grep ollama

# Neu starten:
ollama serve
```

### Problem: "Model not found: llama3.1:8b"

**Lösung:**
```bash
# Modell herunterladen:
ollama pull llama3.1:8b

# Verfügbare Modelle anzeigen:
ollama list
```

### Problem: Docker kann Ollama nicht erreichen

**Lösung für Mac:**
```env
# In .env verwenden:
OLLAMA_HOST=http://host.docker.internal:11434

# NICHT: http://127.0.0.1:11434
# NICHT: http://localhost:11434
```

**Lösung für Linux:**
```env
# In .env verwenden:
OLLAMA_HOST=http://172.17.0.1:11434

# Oder Ollama im Host-Netzwerk starten:
ollama serve --host 0.0.0.0
```

### Problem: Antworten zu langsam

**Lösungen:**

1. **Kleineres Modell verwenden:**
   ```bash
   ollama pull llama3.2:3b
   # In .env: OLLAMA_MODEL=llama3.2:3b
   ```

2. **Temperatur reduzieren:**
   ```python
   # In backend/app/services/chat_service_ollama.py anpassen:
   options={
       "temperature": 0.3,  # Statt 0.7 (schneller aber weniger kreativ)
       "num_predict": 2048,  # Statt 4096 (kürzere Antworten)
   }
   ```

3. **Modell vorladen:**
   ```bash
   # Modell im RAM behalten:
   ollama run llama3.1:8b ""
   ```

### Problem: "Out of memory"

**Lösung:**
```bash
# Kleineres Modell verwenden:
ollama pull llama3.2:3b

# Oder andere Apps schließen
```

## 🎓 Erweiterte Konfiguration

### Mehrere Modelle gleichzeitig:

```python
# backend/app/config.py anpassen:
ollama_model: str = "llama3.1:8b"
ollama_embedding_model: str = "nomic-embed-text"  # Für Embeddings
```

### Eigene Modelle trainieren:

```bash
# Modelfile erstellen für Rüsselsheim-spezifisches Fine-Tuning:
ollama create ruesselsheim-bot -f Modelfile
```

### API direkt nutzen (ohne Python):

```bash
curl http://127.0.0.1:11434/api/generate -d '{
  "model": "llama3.1:8b",
  "prompt": "Was ist die Hauptstadt von Deutschland?",
  "stream": false
}'
```

## 📚 Weitere Ressourcen

- **Ollama Website:** https://ollama.ai
- **Ollama GitHub:** https://github.com/ollama/ollama
- **Modell-Library:** https://ollama.ai/library
- **Llama 3.1 Infos:** https://ai.meta.com/blog/meta-llama-3-1/

## 🎉 Zusammenfassung

**Für 100% kostenlosen, lokalen Betrieb:**

```env
LLM_PROVIDER=ollama
OLLAMA_HOST=http://host.docker.internal:11434
OLLAMA_MODEL=llama3.1:8b
EMBEDDING_PROVIDER=local
```

**Das gibt Ihnen:**
- ✅ **Unbegrenzte Anfragen** (keine API-Limits)
- ✅ **100% Datenschutz** (alles lokal)
- ✅ **Offline-fähig** (kein Internet nötig)
- ✅ **Sehr schnell** (M4 Metal performance)
- ✅ **Keine Kosten** (außer Strom)
- ✅ **DSGVO-konform** (keine Drittanbieter)

**Perfekt für kommunale Anwendungen!** 🏛️

---

**Happy coding! 🦙**
