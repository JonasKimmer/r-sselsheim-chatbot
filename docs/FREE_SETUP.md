# 100% Kostenlose Setup-Anleitung 🆓

Dieser Chatbot kann **komplett kostenlos** betrieben werden!

## 🦙 NEU: Ollama - Die beste kostenlose Option!

**Wir empfehlen jetzt Ollama statt Gemini!**

- ✅ 100% lokal & privat (DSGVO-konform)
- ✅ Unbegrenzte Anfragen (keine API-Limits)
- ✅ Offline-fähig (kein Internet nötig)
- ✅ Sehr schnell (besonders auf M1/M2/M3/M4 Macs)

**👉 Siehe [OLLAMA_SETUP.md](./OLLAMA_SETUP.md) für die vollständige Anleitung!**

---

## 💰 Kostenvergleich

| Komponente | Option 1 (Beste) | Option 2 | Option 3 (Bezahlt) |
|------------|------------------|----------|-------------------|
| **LLM (Chat)** | Ollama (100% lokal) | Google Gemini (Cloud, kostenlos) | Anthropic Claude (~$3 per 1M tokens) |
| **Embeddings** | Lokale Modelle (kostenlos) | Lokale Modelle (kostenlos) | OpenAI (~$0.13 per 1K docs) |
| **Datenbank** | PostgreSQL (open source) | PostgreSQL (open source) | PostgreSQL (open source) |
| **Hosting** | Docker lokal | Docker lokal oder Cloud Free Tier | Cloud |
| **Datenschutz** | ⭐⭐⭐⭐⭐ Perfekt | ⭐⭐ Google Server | ⭐⭐ Anthropic Server |

## 🎯 Kostenlose Konfiguration

### 1. Google Gemini API Key erstellen

**Gemini ist kostenlos** und bietet großzügige Limits:
- ✅ **60 Anfragen pro Minute** (kostenlos)
- ✅ **1500 Anfragen pro Tag** (kostenlos)
- ✅ Keine Kreditkarte erforderlich

**API-Key erstellen:**
1. Gehe zu: https://makersuite.google.com/app/apikey
2. Melde dich mit deinem Google-Konto an
3. Klicke auf "Create API Key"
4. Kopiere den API-Key

### 2. .env Datei konfigurieren

```bash
cp .env.example .env
nano .env
```

**Minimale Konfiguration (100% kostenlos):**
```env
# LLM: Gemini (kostenlos)
LLM_PROVIDER=gemini
GEMINI_API_KEY=dein_gemini_api_key_hier

# Embeddings: Lokal (kostenlos)
EMBEDDING_PROVIDER=local

# Datenbank (Standard)
POSTGRES_USER=ruesselsheim_bot
POSTGRES_PASSWORD=change_me_in_production
POSTGRES_DB=ruesselsheim_chatbot
```

Das war's! Keine weiteren API-Keys nötig.

### 3. Starten

```bash
make install
```

oder manuell:

```bash
docker-compose build
docker-compose up -d
docker-compose exec backend python scripts/import_data.py
```

## 🚀 Zugriff

- **Frontend:** http://localhost:5173
- **Backend API:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs

## 📊 Gemini Free Tier Limits

### Gemini 1.5 Flash (Empfohlen für kostenlosen Betrieb)

- **Rate Limits:**
  - 15 RPM (Requests per Minute)
  - 1 Million TPM (Tokens per Minute)
  - 1,500 RPD (Requests per Day)

- **Eigenschaften:**
  - Schnell
  - Mehrsprachig (inkl. Deutsch)
  - Kostenlos

### Gemini 1.5 Pro (Höhere Qualität)

- **Rate Limits:**
  - 2 RPM (Requests per Minute)
  - 32,000 TPM (Tokens per Minute)
  - 50 RPD (Requests per Day)

- **Eigenschaften:**
  - Bessere Qualität
  - Langsamer
  - Kostenlos

**Auswahl in .env:**
```env
# Für schnellere Antworten (Standard):
GEMINI_MODEL=gemini-1.5-flash

# Für bessere Qualität:
GEMINI_MODEL=gemini-1.5-pro
```

## 💡 Tipps für kostenlosen Betrieb

### 1. Rate Limiting implementieren

Falls Sie mehr Traffic erwarten, fügen Sie Rate Limiting hinzu:

```python
# backend/app/main.py
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.post("/api/chat/")
@limiter.limit("10/minute")  # Max 10 Anfragen pro Minute
async def chat(...):
    ...
```

### 2. Caching für häufige Fragen

Implementieren Sie ein einfaches Caching:

```python
from functools import lru_cache

@lru_cache(maxsize=100)
def get_cached_response(query: str):
    # Cached responses für häufige Fragen
    pass
```

### 3. Monitoring

Überwachen Sie Ihre API-Nutzung:
- Gemini Dashboard: https://makersuite.google.com/
- Zeigt aktuelle Nutzung und Limits

## 🔄 Von kostenlos auf bezahlt wechseln

Falls Sie später auf Claude upgraden möchten:

1. **Anthropic API-Key besorgen:**
   - https://console.anthropic.com/

2. **.env anpassen:**
   ```env
   LLM_PROVIDER=claude
   ANTHROPIC_API_KEY=sk-ant-...
   ```

3. **Neustart:**
   ```bash
   make restart
   ```

## ⚠️ Wichtige Hinweise

### Gemini API Quotas

Wenn Sie die Free-Tier-Limits überschreiten:
- **Gemini:** Requests werden mit 429 (Too Many Requests) abgelehnt
- **Lösung:** Warten Sie oder implementieren Sie Request-Queuing

### Production Deployment

Für Production empfehlen wir:
1. **Request-Queuing** für hohen Traffic
2. **Caching** für häufige Fragen
3. **Monitoring** der API-Limits
4. **Backup-Plan** falls Limits erreicht werden

## 🌟 Kosten bei Scale

Beispiel: Kommunale Website mit 1000 Anfragen/Tag

### Kostenlose Option (Gemini + Lokal)
- **Kosten:** €0
- **Limit:** 1500 Anfragen/Tag (ausreichend)
- **Hosting:** €0 (lokaler Server) oder ~€5/Monat (Cloud)

### Bezahlte Option (Claude + OpenAI)
- **Kosten:** ~€30-50/Monat
- **Limit:** Praktisch unbegrenzt
- **Qualität:** Minimal besser

**Empfehlung:** Starten Sie kostenlos mit Gemini. Upgraden Sie nur bei Bedarf.

## 📝 Zusammenfassung

**Für komplett kostenlosen Betrieb:**

```env
LLM_PROVIDER=gemini
GEMINI_API_KEY=your_key
EMBEDDING_PROVIDER=local
```

**Das gibt Ihnen:**
- ✅ Bis zu 1500 Chat-Anfragen/Tag kostenlos
- ✅ Unbegrenzte Embeddings (lokal)
- ✅ Keine Kreditkarte erforderlich
- ✅ Perfekt für kleine bis mittlere kommunale Websites

## 🆘 Troubleshooting

### "API key not valid"
➡️ Prüfen Sie ob der Gemini API-Key korrekt ist

### "Quota exceeded"
➡️ Sie haben die kostenlosen Limits erreicht. Warten Sie bis zum nächsten Tag oder upgraden Sie.

### "Model not found"
➡️ Prüfen Sie ob `GEMINI_MODEL` korrekt gesetzt ist (gemini-1.5-flash oder gemini-1.5-pro)

## 📚 Weitere Ressourcen

- [Gemini API Docs](https://ai.google.dev/docs)
- [Gemini Pricing](https://ai.google.dev/pricing)
- [API Key erstellen](https://makersuite.google.com/app/apikey)

---

**Happy coding! 🎉**
