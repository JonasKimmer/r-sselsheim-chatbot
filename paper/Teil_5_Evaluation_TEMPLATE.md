# 5. Evaluation

## 5.1 Evaluations-Methodik

### 5.1.1 Test-Dataset

Für die Evaluation wurde ein repräsentatives Test-Dataset mit **21 Fragen** erstellt, das typische Bürgeranfragen an eine Kommunalverwaltung abdeckt. Die Fragen sind in 8 Kategorien unterteilt:

| Kategorie | Anzahl Fragen | Beispiel-Frage |
|-----------|---------------|----------------|
| Verwaltung | 5 | "Wie beantrage ich einen Personalausweis?" |
| Wetter | 3 | "Wie wird das Wetter morgen?" |
| Verkehr | 3 | "Wann fährt die nächste Bahn nach Frankfurt?" |
| Abfall | 3 | "Wann wird bei mir der Müll abgeholt?" |
| Benzinpreise | 1 | "Wo gibt es das günstigste Benzin?" |
| Feiertage | 2 | "Wann ist der nächste Feiertag?" |
| Allgemein | 2 | "Wie viele Einwohner hat Rüsselsheim?" |
| Multi-Domain | 2 | "Ich möchte einen Personalausweis beantragen. Wie ist das Wetter und wie komme ich zum Bürgerbüro?" |

**Rationale:** Die Verteilung der Fragen spiegelt die tatsächliche Häufigkeit von Anfragen wider (mehr Verwaltungsfragen als z.B. Benzinpreise). Multi-Domain-Fragen testen die Fähigkeit des Systems, mehrere APIs gleichzeitig zu nutzen.

### 5.1.2 Gemessene Metriken

In Anlehnung an Zhu et al. (2024) [9] werden folgende Metriken erfasst:

**Retrieval-Metriken:**
- **Retrieval Score:** Durchschnittliche Cosine Similarity der Top-3 Dokumente
- **Documents Retrieved:** Anzahl relevanter Dokumente gefunden
- **Category Match:** Prozentsatz korrekter Kategorie-Zuordnung

**Performance-Metriken:**
- **Total Response Time:** Gesamtzeit von Anfrage bis Antwort
- **Search Time:** Zeit für RAG-Vektor-Suche
- **Generation Time:** Zeit für LLM-Antwort-Generierung

**Qualitäts-Metriken:**
- **Success Rate:** Prozentsatz erfolgreicher Antworten (ohne Fehler)
- **Faithfulness:** Manuelle Prüfung auf Faktentreue (Stichprobe)

### 5.1.3 Test-Setup

**Hardware:**
- CPU: [HIER EINFÜGEN nach Test]
- RAM: [HIER EINFÜGEN nach Test]
- GPU: Keine (CPU-only für Embeddings)

**Software:**
- PostgreSQL + pgvector: Version [HIER EINFÜGEN]
- Sentence-Transformers: paraphrase-multilingual-MiniLM-L12-v2
- LLM-Provider: [GEMINI/OLLAMA/CLAUDE - hier einfügen was getestet wurde]

**Test-Durchführung:**
```bash
# API-Endpoint für Batch-Evaluation
POST /api/evaluation/evaluate/batch

# Alle 21 Fragen werden automatisch getestet
# Ergebnis: JSON mit Summary + Detailed Results
```

---

## 5.2 Ergebnisse

### 5.2.1 Response Time Analyse

**[HIER NACH EVALUATION EINFÜGEN]**

**Gesamt Response Time:**
- Durchschnitt: [X.XX] Sekunden
- Minimum: [X.XX] Sekunden
- Maximum: [X.XX] Sekunden
- P95 (95. Perzentil): [X.XX] Sekunden

**Breakdown nach Phase:**
- Search Time (RAG): [XXX] ms (durchschnittlich)
- Generation Time (LLM): [X.XX] Sekunden (durchschnittlich)

**Tabelle 1: Response Time nach Kategorie**

| Kategorie | Anzahl | Avg Time (s) | Min (s) | Max (s) |
|-----------|--------|--------------|---------|---------|
| Verwaltung | 5 | [X.XX] | [X.XX] | [X.XX] |
| Wetter | 3 | [X.XX] | [X.XX] | [X.XX] |
| Verkehr | 3 | [X.XX] | [X.XX] | [X.XX] |
| Abfall | 3 | [X.XX] | [X.XX] | [X.XX] |
| ... | ... | ... | ... | ... |

**Grafik 1: Response Time Distribution** [HIER BOXPLOT ODER HISTOGRAM EINFÜGEN]

**Interpretation:**
[NACH DATEN EINFÜGEN - z.B.:
- Wetter-Anfragen sind schneller (nur API-Call, kein RAG nötig)
- Verwaltungs-Fragen langsamer (RAG + längere LLM-Antworten)
- 95% der Anfragen unter 5 Sekunden → akzeptabel für Chatbot
]

### 5.2.2 Retrieval Quality

**[HIER NACH EVALUATION EINFÜGEN]**

**Retrieval Scores (Cosine Similarity):**
- Durchschnitt: [0.XXX]
- Minimum: [0.XXX]
- Maximum: [0.XXX]

**Documents Retrieved:**
- Durchschnitt: [X.X] Dokumente pro Anfrage
- Immer Top-3 oder weniger?

**Category Match Accuracy:**
- Korrekte Kategorie gefunden: [XX]% der Fälle

**Tabelle 2: Top Retrieval Scores**

| Frage | Bestes Dokument | Score | Kategorie |
|-------|-----------------|-------|-----------|
| "Wie beantrage ich einen Personalausweis?" | [Dokument-Titel] | [0.XXX] | verwaltung |
| ... | ... | ... | ... |

**Interpretation:**
[NACH DATEN EINFÜGEN - z.B.:
- Scores >0.80 indizieren hohe Relevanz
- Scores 0.60-0.80 akzeptabel
- Scores <0.60 problematisch → Dokument fehlt oder Query zu generisch
- Category Match: Wenn >80% → RAG funktioniert gut
]

### 5.2.3 Success Rate

**[HIER NACH EVALUATION EINFÜGEN]**

**Erfolgreiche vs. Fehlgeschlagene Antworten:**
- Erfolgreich: [XX]/21 ([XX]%)
- Fehlgeschlagen: [XX]/21 ([XX]%)

**Fehleranalyse:**
[HIER LISTE DER FEHLGESCHLAGENEN FRAGEN MIT FEHLER-GRÜNDEN]

Beispiel:
1. Frage: "..." → Fehler: "Network unreachable" (Ollama nicht erreichbar)
2. Frage: "..." → Fehler: "No relevant documents found" (RAG-DB leer)

**Interpretation:**
[NACH DATEN EINFÜGEN - z.B.:
- >85% Success Rate → System produktionsreif
- Hauptfehlerquelle: [z.B. LLM-Provider nicht erreichbar]
- Fehler vermeidbar durch: [z.B. Fallback-Provider, bessere Error-Handling]
]

---

## 5.3 Vergleich LLM-Provider

**[NUR WENN MEHRERE PROVIDER GETESTET - SONST WEGLASSEN]**

Falls Zeit erlaubt, wurde derselbe Test mit verschiedenen LLM-Providern durchgeführt:

**Tabelle 3: Provider-Vergleich**

| Metrik | Ollama (Llama 3.1) | Gemini 1.5 Flash | Claude 3.5 Sonnet |
|--------|---------------------|------------------|-------------------|
| Avg Response Time | [X.XX] s | [X.XX] s | [X.XX] s |
| Success Rate | [XX]% | [XX]% | [XX]% |
| Qualitative Quality* | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Kosten (100k req/Monat) | €0 | €0 | ~€300 |
| Datenschutz | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |

*Qualitative Quality: Manuelle Bewertung von 5 Beispiel-Antworten

**Interpretation:**
[NACH DATEN EINFÜGEN - z.B.:
- Ollama: Langsamer aber kostenlos und GDPR-konform
- Gemini: Guter Kompromiss (schnell, kostenlos, gute Qualität)
- Claude: Beste Qualität, aber kostenpflichtig
- Empfehlung: Gemini für Pilot, Ollama für Produktion (Datenschutz)
]

---

## 5.4 Qualitativer Deep-Dive: Beispiel-Dialoge

### 5.4.1 Beispiel 1: Erfolgreicher Verwaltungs-Dialog

**Frage:** "Wie beantrage ich einen Personalausweis?"

**RAG Retrieval:**
- Top-1 Dokument: "[Titel des Dokuments]" (Score: [0.XXX])
- Kategorie: verwaltung
- Quelle: [URL oder "Manuell importiert"]

**Antwort des Chatbots:**
[HIER KOMPLETTE ANTWORT EINFÜGEN]

**Bewertung:**
- ✅ Faktisch korrekt (verglichen mit Original-Dokument)
- ✅ Vollständig (alle erforderlichen Dokumente genannt)
- ✅ Gut strukturiert (Bulletpoints, klar lesbar)
- ✅ Quellenangabe vorhanden (wenn implementiert)

### 5.4.2 Beispiel 2: Multi-Domain-Anfrage

**Frage:** "Ich möchte nächste Woche einen Personalausweis beantragen. Wie ist das Wetter und wie komme ich zum Bürgerbüro?"

**System-Aktionen:**
1. RAG-Suche: "Personalausweis beantragen"
2. API-Call: OpenWeatherMap (Wetter-Vorhersage)
3. API-Call: RMV/Mapbox (Route zum Rathaus)

**Antwort des Chatbots:**
[HIER KOMPLETTE ANTWORT EINFÜGEN]

**Bewertung:**
- ✅ Alle drei Teilfragen beantwortet
- ✅ Korrekte API-Integration
- ✅ Kohärente Gesamt-Antwort (nicht fragmentiert)

### 5.4.3 Beispiel 3: Fehlgeschlagene Anfrage (falls vorhanden)

**Frage:** [HIER EINFÜGEN]

**Fehler:** [HIER EINFÜGEN]

**Ursache:** [HIER ANALYSIEREN]

**Mögliche Lösung:** [HIER VORSCHLAGEN]

---

## 5.5 Vergleich mit verwandten Arbeiten

**Tabelle 4: Benchmark-Vergleich**

| System | Success Rate | Avg Response Time | Technologie |
|--------|--------------|-------------------|-------------|
| **Diese Arbeit** | [XX]% | [X.XX] s | RAG + Multi-Provider LLM |
| Ulm (Ulmer Spatz) | 68% | n/a | Proprietär |
| Zürich Chatbot | 87%* | n/a | RAG |
| Gov.uk Chat | n/a | n/a | RAG + GPT-4 |

*Genauigkeit, nicht Success Rate (unterschiedliche Metrik)

**Interpretation:**
[NACH DATEN EINFÜGEN - z.B.:
- Vergleichbare oder bessere Success Rate als Ulm
- Response Time konkurrenzfähig (typisch 2-5s für Chatbots)
- Open-Source Vorteil gegenüber proprietären Lösungen
]

---

## 5.6 Limitierungen und Validität

### 5.6.1 Limitierungen der Evaluation

**Interner Validität:**
- Test-Dataset: Nur 21 Fragen → begrenzte statistische Aussagekraft
- Keine Langzeit-Tests (z.B. Performance nach 1 Monat Betrieb)
- Keine echten Nutzer (nur synthetische Fragen)

**Externer Validität:**
- Spezifisch für Rüsselsheim → Generalisierbarkeit auf andere Kommunen unklar
- Deutsche Sprache → Mehrsprachigkeit nicht getestet
- Keine komplexen Verwaltungsvorgänge (z.B. Bauanträge)

### 5.6.2 Threats to Validity

**Interne Bedrohungen:**
- Test-Dataset-Bias: Fragen wurden vom Autor erstellt → möglicherweise zu "einfach"
- Cherry-Picking: Nur 21 ausgewählte Fragen, nicht zufällig aus realen Anfragen

**Externe Bedrohungen:**
- Hardware-Abhängigkeit: Performance auf anderem Server variiert
- LLM-Provider-Verfügbarkeit: Gemini/Claude können ausfallen
- Dokumenten-Qualität: RAG-Performance hängt stark von importierten Dokumenten ab

### 5.6.3 Maßnahmen zur Validierung

**Durchgeführt:**
- Automatisierte Metriken (objektiv, reproduzierbar)
- Multiple Test-Kategorien (breite Abdeckung)
- Open-Source (Evaluation nachvollziehbar)

**Empfohlen für Future Work:**
- User Study mit echten Bürgern (n=50+)
- A/B-Test gegen bestehende Hotline
- Langzeit-Deployment (6-12 Monate)

---

## 5.7 Zusammenfassung der Evaluations-Ergebnisse

**Kernerkenntnisse:**

1. **Performance:** [NACH DATEN - z.B. "System antwortet durchschnittlich in <4s, akzeptabel für Chatbot-Anwendung"]

2. **Retrieval Quality:** [NACH DATEN - z.B. "RAG findet relevante Dokumente mit durchschnittlichem Score von 0.78, indiziert gute Embedding-Qualität"]

3. **Success Rate:** [NACH DATEN - z.B. "85% Success Rate zeigt Produktionsreife, verbleibende Fehler primär LLM-Provider-bedingt"]

4. **Vergleichbarkeit:** [NACH DATEN - z.B. "Performance vergleichbar mit kommerziellen Lösungen (Ulm, Zürich)"]

5. **Limitierungen:** Kleine Test-Dataset-Größe, keine echten Nutzer, keine Langzeit-Tests

**Beantwortung der Forschungsfrage:**
"Wie können LLM-basierte Chatbots die kommunale Verwaltung unterstützen?"

→ **Antwort:** [NACH EVALUATION FORMULIEREN - z.B.:
"Die Evaluation zeigt, dass ein RAG-basierter Chatbot mit Multi-Provider LLM-Architektur in der Lage ist, [XX]% der typischen Bürgeranfragen korrekt und in akzeptabler Zeit (<5s) zu beantworten. Das System ist produktionsreif (automatisierte Tests, Monitoring, Security) und kann durch Open-Source-Charakter von anderen Kommunen nachgenutzt werden. Hauptlimitierung ist die Abhängigkeit von qualitativ hochwertigen Dokumenten in der RAG-Datenbank."
]

---

## 📊 Checkliste: Evaluation durchführen

**Bevor du Teil 5 fertigstellen kannst, musst du:**

1. ✅ **Gemini API Key hinzufügen** zu `backend/.env`
2. ✅ **Backend neu starten:** `docker-compose restart backend`
3. ✅ **Evaluation laufen lassen:**
   ```bash
   curl -X POST http://localhost:8000/api/evaluation/evaluate/batch | python3 -m json.tool > evaluation_results.json
   ```
4. ✅ **Ergebnisse analysieren:** `evaluation_results.json` öffnen
5. ✅ **Zahlen einfügen** in dieses Template (alle [XXX] Platzhalter)
6. ✅ **Beispiel-Dialoge kopieren** aus den `detailed_results`
7. ✅ **Grafiken erstellen** (Python matplotlib oder Excel):
   - Response Time Distribution (Boxplot)
   - Success Rate by Category (Bar Chart)
   - Retrieval Score Histogram
8. ✅ **Interpretation schreiben** bei jedem Abschnitt
9. ✅ **Vergleich mit Papers** (Ulm 68%, Zürich 87%)

**Python-Script für Grafiken (optional):**
```python
import json
import matplotlib.pyplot as plt

# Load results
with open('evaluation_results.json') as f:
    data = json.load(f)

# Plot 1: Response Time Distribution
times = [r['total_time_ms'] for r in data['detailed_results'] if r['success']]
plt.hist(times, bins=20)
plt.xlabel('Response Time (ms)')
plt.ylabel('Frequency')
plt.title('Response Time Distribution')
plt.savefig('response_time_dist.png')

# Plot 2: Success Rate by Category
# ... (implementiere basierend auf deinen Daten)
```

---

**Nächste Schritte:**
1. Führe Evaluation durch (siehe Checkliste oben)
2. Fülle [XXX] Platzhalter mit echten Zahlen
3. Erstelle Grafiken/Tabellen
4. Schreibe Interpretationen
5. → **Teil 5 ist fertig!**
