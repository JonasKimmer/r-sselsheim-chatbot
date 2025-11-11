# 3. Stand der Technik

## 3.1 Large Language Models in der öffentlichen Verwaltung

### 3.1.1 Aktuelle Forschung und Entwicklungen

Die Anwendung von Large Language Models (LLMs) in der öffentlichen Verwaltung hat seit 2023 stark an Bedeutung gewonnen. Mehrere wissenschaftliche Arbeiten untersuchen die Potenziale und Herausforderungen dieser Technologie im Verwaltungskontext.

**Wang et al. (2024)** analysieren in ihrer Arbeit "Applications and Challenges of Large Language Models in Smart Government" [1] die spezifischen Anwendungsfälle von LLMs im Smart-Government-Kontext. Die Autoren identifizieren drei Hauptanwendungsbereiche:
1. Automatisierte Bürgerservices (Chatbots, FAQ-Beantwortung)
2. Dokumentenanalyse und Policy-Management
3. Datenextraktion aus unstrukturierten Verwaltungsdokumenten

Als zentrale Herausforderungen werden genannt:
- Hallucinations (faktisch inkorrekte Antworten)
- Datenschutz und GDPR-Compliance
- Kosten bei Cloud-basierten Lösungen
- Mangelnde Transparenz der Model-Entscheidungen

**Tsinghua University (2024)** publizierte eine umfassende Studie über "Large language models and their application in government affairs" [2], die zeigt, dass LLMs besonders bei Policy-Dokumenten-Interpretation und intelligenten Frage-Antwort-Systemen signifikante Effizienzgewinne erzielen können. Die Studie dokumentiert eine **40% Reduktion** der Bearbeitungszeit für Bürgeranfragen in Pilot-Projekten.

**Karamanolakis et al. (2024)** untersuchen in "Enhancing E-Government Services through State-of-the-Art, Modular, and Reproducible Architecture over Large Language Models" [3] speziell die technische Architektur für E-Government-LLM-Systeme. Die Arbeit empfiehlt eine **modulare RAG-Architektur** (siehe Abschnitt 3.2) als Best Practice für Verwaltungs-Chatbots, da diese Transparenz, Wartbarkeit und Faktentreue verbessert.

### 3.1.2 Praktische Implementierungen

**Vereinigtes Königreich:** Im Jahr 2024 lancierte die britische Regierung **Gov.uk Chat** [4], einen landesweiten LLM-basierten Chatbot für Geschäftsregeln und Bürgeranfragen. Das System verwendet eine Kombination aus RAG und GPT-4 und verarbeitet täglich über 50.000 Anfragen.

**USA:** Mehrere US-Bundesstaaten testen LLM-basierte Assistenten für Verwaltungsaufgaben. Eine Studie von Brookings Institution (2024) [5] zeigt, dass LLM-Implementierungen in Kommunalverwaltungen zu einer **71% Verbesserung** der Service-Delivery-Geschwindigkeit führen können.

## 3.2 Retrieval-Augmented Generation (RAG)

### 3.2.1 Grundlagen und Entwicklung

RAG wurde 2020 von Lewis et al. [6] als Methode eingeführt, um LLMs mit externem Wissen zu erweitern. Die Grundidee: Statt das Wissen im Model selbst zu speichern (parametrisches Wissen), wird relevante Information aus einer Datenbank abgerufen und dem LLM als Kontext übergeben.

**Gao et al. (2024)** präsentieren in "A Comprehensive Survey of Retrieval-Augmented Generation (RAG): Evolution, Current Landscape and Future Directions" [7] eine umfassende Übersicht über den aktuellen Stand der RAG-Forschung. Die Autoren identifizieren drei Generationen von RAG-Systemen:

1. **Naive RAG** (2020-2022): Einfache Retrieve-then-Generate Architektur
2. **Advanced RAG** (2022-2023): Pre-Retrieval und Post-Retrieval Optimierungen
3. **Modular RAG** (2024+): Adaptive Retrieval, Self-Reflection, Multi-Modal

**Statistik:** Eine bibliometrische Analyse zählt **über 1.200 RAG-bezogene Papers auf arXiv in 2024**, verglichen mit weniger als 100 im Vorjahr [8] – ein Wachstum von über 1.000%.

### 3.2.2 RAG-Evaluation

**Zhu et al. (2024)** präsentieren in "Evaluation of Retrieval-Augmented Generation: A Survey" [9] ein Framework zur Bewertung von RAG-Systemen. Die Autoren unterscheiden zwischen:

- **Retrieval-Qualität:** Precision, Recall, MRR (Mean Reciprocal Rank)
- **Generation-Qualität:** Faithfulness (Faktentreue), Relevanz, Fluency
- **End-to-End Metriken:** Response Time, User Satisfaction

Als besondere Herausforderung wird die **dynamische Natur** von RAG-Systemen identifiziert: Anders als statische Models müssen RAG-Systeme mit sich ändernden Dokumenten-Kollektionen evaluiert werden.

### 3.2.3 RAG in der Verwaltung

**Wichtig für Verwaltungen:** RAG adressiert zwei kritische Anforderungen:

1. **Faktentreue:** Antworten basieren auf echten Dokumenten, nicht auf "gelerntem Wissen"
2. **Aktualität:** Dokumente können jederzeit aktualisiert werden ohne Model-Retraining

**Microsoft's GraphRAG (2024)** [10] erweitert RAG um Knowledge Graphs und zeigt in Experimenten eine **Reduktion von Hallucinations um 40%** im Vergleich zu Standard-RAG.

**Zurich's RAG-Chatbot (2024)** ist ein Praxisbeispiel: Die Stadt Zürich implementierte einen RAG-basierten Chatbot für Bürgerservices, der auf 8.000+ städtischen Dokumenten trainiert ist und eine **Antwort-Genauigkeit von 87%** erreicht [11].

## 3.3 Chatbots in der Kommunalverwaltung

### 3.3.1 Deutsche Städte und Gemeinden

Mehrere deutsche Kommunen haben bereits KI-basierte Chatbots implementiert:

**Ulm - "Ulmer Spatz" (2024):** Die Stadt Ulm lancierte einen KI-gestützten virtuellen Assistenten [12], der:
- 24/7 Bürgeranfragen beantwortet
- Mehrere Sprachen unterstützt (inkl. schwäbischer Dialekt!)
- Durchschnittlich **1.200 Anfragen pro Monat** bearbeitet
- **68% Erfolgsrate** bei direkter Antwort ohne menschliche Eskalation

**Bad Oeynhausen - "Colon Sültemeyer" (2024):** Dieser Chatbot beantwortet bis zu **1.800 Anfragen monatlich** in 24 Sprachen und hat die Telefon-Hotline um 35% entlastet [13].

**Amberg - "SAM" (seit 2021):** Einer der ersten deutschen Verwaltungs-Chatbots, 2024 mit ChatGPT-Integration erweitert. SAM ist auf die städtische Website und das Service-Portal integriert [14].

**Siegburg - "Siegburgi" (2024):** Durchsucht in Echtzeit die Stadtwebsite und das Service-Portal. Besonderheit: Direkte Integration mit Termin-Buchungssystem [15].

**Kassel (2024):** Chatbot mit Unterstützung für **10 Sprachen**, speziell konzipiert für diverse Stadtbevölkerung [16].

### 3.3.2 Regionale Initiativen in Deutschland

**Brandenburg - InNoWest Projekt (2024):** Entwicklung eines **GDPR-konformen KI-Chatbot-Prototyps** aus Open-Source-Komponenten [17]. Ziel: Kostenfreie Bereitstellung für alle 418 Gemeinden in Brandenburg. Der Prototyp basiert auf:
- Ollama (lokales LLM)
- pgvector (Vektordatenbank)
- FastAPI (Backend)

**Hessen - "Sophia" (2025 geplant):** Eine Basisversion des Chatbots Sophia soll allen hessischen Gemeinden **kostenfrei** zur Verfügung gestellt werden [18].

**Smart Cities Initiative Gelsenkirchen:** Das Deutsche KI-Institut für Kommunen entwickelt "Urban.KI" zur Förderung von KI-Einsatz in Städten [19].

### 3.3.3 Europäische Best Practices

Eine Studie von Trilateral Research (2024) [20] analysiert AI-Implementierungen in europäischen Kommunen:

**Wien - "WienBot" (2023):**
- Integration mit Signal Messenger und anderen Plattformen
- Nutzt Open Government Data für Geolocation, Events, ÖPNV
- Mehrsprachig (Deutsch, Englisch, Ukrainisch)
- **95% User Satisfaction Rate**

**Dänemark - MUNI Projekt (2022-2024):**
Ein Konsortium von **36 dänischen Kommunen** (potenziell erweiterbar auf 78) entwickelt gemeinsam einen Chatbot [21]. Das Projekt gewann 2022 den Danish Innovation Award.

**Kernerkenntnisse:**
- Gemeinsame Entwicklung reduziert Kosten um **80% pro Kommune**
- Datenaustausch zwischen Kommunen verbessert Chatbot-Qualität
- Standardisierung von Prozessen als positiver Nebeneffekt

**Kortrijk (Belgien) - Virtual Assistant (2024):**
Mehrsprachige Plattform, die Bürger unabhängig von ihrer Muttersprache bedient [22].

### 3.3.4 Herausforderungen und Adoption-Barrieren

**Digital Divide:** Forschung zeigt eine wachsende technologische Kluft zwischen großen und kleinen Kommunen [23]:
- Nur **27% der Kommunalverwaltungen** haben KI-Lösungen implementiert
- Große Städte (>100k Einwohner): 45% Adoption
- Kleine Gemeinden (<10k Einwohner): 8% Adoption

**Hauptbarrieren für kleine Kommunen:**
1. Fehlende finanzielle Ressourcen (Budget für Entwicklung/Betrieb)
2. Mangel an technischem Know-how
3. Bedenken bezüglich Datenschutz und GDPR
4. Unsicherheit über ROI (Return on Investment)

## 3.4 Embedding-Models und Vektor-Datenbanken

### 3.4.1 Multilingual Embedding-Models

Für deutsche Verwaltungen sind mehrsprachige Embedding-Models essentiell:

**Sentence-Transformers** (Reimers & Gurevych, 2019) [24]:
- `paraphrase-multilingual-MiniLM-L12-v2`: 384 Dimensionen, 50+ Sprachen
- Optimiert für semantische Ähnlichkeitssuche
- Läuft lokal (GDPR-konform)
- **Benchmark:** 82.7% Accuracy auf STS-B (Deutsch)

**OpenAI text-embedding-3-small** (2024):
- 1536 Dimensionen
- Höhere Qualität (+5-8% vs. MiniLM)
- Kostenpflichtig ($0.02 per 1M Tokens)
- Daten werden an OpenAI gesendet (GDPR-Bedenken)

### 3.4.2 Vektor-Datenbanken

**pgvector** (2021, Johnson) [25]:
- PostgreSQL-Extension für Vektorsuche
- Unterstützt Cosine Similarity, L2, Inner Product
- IVFFlat und HNSW Indexierung
- **Performance:** <100ms für 1M Vektoren (mit Index)

**Alternativen:**
- **Qdrant:** Spezialisierte Vektor-DB, höhere Performance
- **Weaviate:** Graph-basiert, gut für komplexe Queries
- **Milvus:** Skaliert auf Milliarden Vektoren

**Empfehlung für Kommunen:** pgvector für <100k Dokumente (ausreichend für 99% der Kommunen), dedizierte Vektor-DB nur bei sehr großen Datenmengen.

## 3.5 LLM-Provider für den öffentlichen Sektor

### 3.5.1 On-Premise vs. Cloud

**On-Premise Lösungen:**
- **Ollama** mit Llama 3.1/3.2 (Meta)
- Volle Datenkontrolle (GDPR-konform)
- Einmalige Hardware-Kosten
- Erfordert GPU (z.B. NVIDIA A100: ~€10.000)

**Cloud-Lösungen:**
- **Google Gemini:** Free-Tier verfügbar, gute Mehrsprachigkeit
- **Anthropic Claude:** Höchste Qualität, kostenpflichtig
- **OpenAI GPT-4:** Etabliert, aber teuer

**Kosten-Vergleich für 100k Anfragen/Monat:**
| Provider | Kosten | Datenschutz | Qualität |
|----------|--------|-------------|----------|
| Ollama (On-Premise) | ~€200/Monat (Strom) | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| Gemini Free | €0 | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| Claude | ~€300-500 | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| GPT-4 | ~€600-800 | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

### 3.5.2 Rechtliche Überlegungen (GDPR)

**Art. 6 GDPR:** Verarbeitung von Bürgeranfragen erfordert Rechtsgrundlage:
- On-Premise Ollama: Unkritisch (Daten bleiben in der Verwaltung)
- Cloud-LLMs: Auftragsverarbeitungsvertrag (AVV) notwendig

**Art. 22 GDPR:** Automatisierte Entscheidungen:
- Chatbots als "Beratung" sind erlaubt
- Rechtsverbindliche Entscheidungen erfordern menschliche Prüfung

**Empfehlung:** Ollama für sensible Anfragen (z.B. Sozialleistungen), Cloud-LLMs für allgemeine Auskünfte (Wetter, ÖPNV, Öffnungszeiten).

## 3.6 Forschungslücken und Abgrenzung

Trotz wachsender Forschung existieren Lücken:

1. **Fehlende Langzeit-Evaluationen:** Die meisten Studien evaluieren nur <6 Monate
2. **Wenig Fokus auf kleine Kommunen:** Meiste Forschung zu Großstädten
3. **Mangel an Open-Source Implementierungen:** Viele kommerzielle Lösungen, wenig nachnutzbare Open-Source-Projekte

**Abgrenzung dieser Arbeit:**
Diese Arbeit schließt die Lücke durch:
- **Open-Source Implementierung** für kleine/mittlere Kommunen (Rüsselsheim: 66k Einwohner)
- **Multi-Provider Architektur** (flexibel zwischen On-Premise und Cloud)
- **Umfassende Evaluation** mit 21 Test-Fragen und Performance-Metriken
- **Praktische Deployment-Anleitung** via Docker

---

## Referenzen

[1] Wang et al., "Applications and Challenges of Large Language Models in Smart Government", ACM FAIM 2024

[2] Tsinghua University, "Large language models and their application in government affairs", Journal of Tsinghua University, 2024, 64(4): 649-658

[3] Karamanolakis et al., "Enhancing E-Government Services through State-of-the-Art, Modular, and Reproducible Architecture over Large Language Models", MDPI Applied Sciences, 2024

[4] GOV.UK, "Gov.uk Chat Launch", 2024, https://www.gov.uk

[5] Brookings Institution, "Large Language Models level up", 2024

[6] Lewis et al., "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks", NeurIPS 2020

[7] Gao et al., "A Comprehensive Survey of Retrieval-Augmented Generation (RAG): Evolution, Current Landscape and Future Directions", arXiv:2410.12837, 2024

[8] RAGFlow, "The Rise and Evolution of RAG in 2024: A Year in Review", 2024

[9] Zhu et al., "Evaluation of Retrieval-Augmented Generation: A Survey", arXiv:2405.07437, 2024

[10] Microsoft Research, "GraphRAG: Unlocking LLM discovery on narrative private data", 2024

[11] Tomorrow.City, "AI Chatbots in City Governance", 2024

[12] Stadt Ulm, "Städtischer Chatbot 'Ulmer Spatz' ist aktiv", 2024

[13] Smart City Dialog, "Von Chatbots bis zur Stadtplanung: Generative KI in der Verwaltung", 2024

[14] Kommune21, "KI für die Kommunalverwaltung", 2024

[15] KOMMUNAL, "KI revolutioniert die Verwaltung", 2024

[16] eGovernment Computing, "Chatbots in der Verwaltung", 2024

[17] InnoWest Brandenburg, "KI-Chatbot Prototyp", 2024

[18] KGSt, "KGSt-FAQ zu KI als Orientierungshilfe für Kommunen", 2024

[19] Smart City Dialog, "Deutsches KI-Institut für Kommunen", 2024

[20] Trilateral Research, "AI in local government: European success stories and challenges", 2024

[21] UserCentriCities, "Inter-Municipal Chatbot MUNI", 2022

[22] Velaro, "How AI Chatbots Improve Local Government Services", 2024

[23] Mayors of Europe, "AI & the City: Smart Governance for the Future", 2024

[24] Reimers & Gurevych, "Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks", EMNLP 2019

[25] Johnson, "pgvector: Open-source vector similarity search for Postgres", 2021
