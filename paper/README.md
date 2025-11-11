# Hausarbeits-Materialien: LLM-basierter Chatbot für die Verwaltung

Dieses Verzeichnis enthält alle Materialien für die 10-seitige Hausarbeit und die 20-minütige PowerPoint-Präsentation zum Thema **"Die Rolle von Large Language Models in der Verwaltung"**.

---

## 📁 Datei-Übersicht

### ✅ Fertige Kapitel (direkt verwendbar)

| Datei | Beschreibung | Seiten | Status |
|-------|--------------|--------|--------|
| `Teil_3_Stand_der_Technik.md` | LLMs in Verwaltung, RAG, verwandte Projekte | ~2.5 | ✅ Fertig |
| `Teil_4_Loesung_Implementierung.md` | Systemarchitektur, RAG, APIs, Deployment | ~3 | ✅ Fertig |
| `Literatur_Zusammenfassung.md` | 25+ Papers mit Zusammenfassungen + URLs | - | ✅ Fertig |
| `Architektur_Diagramme.md` | 6 Mermaid-Diagramme für Paper + Präsentation | - | ✅ Fertig |
| `PowerPoint_Praesentation.md` | 16 Folien-Templates mit Content | - | ✅ Fertig |

### ⚠️ Templates (müssen ausgefüllt werden)

| Datei | Beschreibung | Was fehlt |
|-------|--------------|-----------|
| `Teil_5_Evaluation_TEMPLATE.md` | Evaluation mit Metriken | Echte Test-Daten einfügen |

### ❌ Noch zu schreiben (von DIR)

Die folgenden Teile musst **du selbst** schreiben:
- **Teil 1: Einleitung** (0.5-1 Seite)
- **Teil 2: Motivation** (0.5 Seite)
- **Teil 6: Diskussion** (1 Seite)
- **Teil 7: Zusammenfassung** (0.5 Seite)

---

## 📊 Struktur der Hausarbeit (8-10 Seiten)

```
1. Einleitung (0.5-1 Seite) ← DU
2. Motivation (0.5 Seite) ← DU
3. Stand der Technik (2-2.5 Seiten) ← FERTIG ✅
4. Lösung: Implementierung (2.5-3 Seiten) ← FERTIG ✅
5. Evaluation (1.5-2 Seiten) ← TEMPLATE (Daten einfügen)
6. Diskussion (1 Seite) ← DU
7. Zusammenfassung (0.5 Seite) ← DU
Referenzen ← Siehe Literatur_Zusammenfassung.md
```

---

## 🚀 Schnellstart: Evaluation durchführen

### Schritt 1: Gemini API Key eintragen

```bash
# backend/.env erstellen/bearbeiten
nano backend/.env

# Folgende Zeile ändern:
GEMINI_API_KEY=your_actual_key_here  # Von https://ai.google.dev/
```

### Schritt 2: Backend neu starten

```bash
cd /home/user/r-sselsheim-chatbot
docker-compose restart backend
```

### Schritt 3: Evaluation laufen lassen

```bash
# Test-Fragen anzeigen
curl http://localhost:8000/api/evaluation/test-questions | python3 -m json.tool

# RAG-Statistiken
curl http://localhost:8000/api/evaluation/rag/statistics | python3 -m json.tool

# BATCH-EVALUATION (21 Fragen)
curl -X POST http://localhost:8000/api/evaluation/evaluate/batch \
  | python3 -m json.tool > evaluation_results.json

# Ergebnisse anzeigen
cat evaluation_results.json
```

### Schritt 4: Ergebnisse in Teil_5 einfügen

1. Öffne `evaluation_results.json`
2. Kopiere Werte aus `summary`:
   - `avg_response_time_ms` → Teil 5, Abschnitt 5.2.1
   - `success_rate_percent` → Teil 5, Abschnitt 5.2.3
   - `avg_retrieval_score` → Teil 5, Abschnitt 5.2.2
3. Kopiere Beispiel-Dialoge aus `detailed_results`
4. Erstelle Grafiken (siehe Python-Script in Teil 5)

---

## 📝 Hausarbeit schreiben: Workflow

### Option A: LaTeX (IEEE/ACM Template)

1. **Template herunterladen:**
   - IEEE: https://www.ieee.org/conferences/publishing/templates.html
   - ACM: https://www.acm.org/publications/proceedings-template

2. **Markdown → LaTeX konvertieren:**
   ```bash
   pandoc Teil_3_Stand_der_Technik.md -o Teil_3.tex
   pandoc Teil_4_Loesung_Implementierung.md -o Teil_4.tex
   ```

3. **Mermaid-Diagramme → PDF:**
   - Gehe zu https://mermaid.live
   - Kopiere Diagramm-Code aus `Architektur_Diagramme.md`
   - Export als SVG/PDF (300 DPI)

4. **Bilder einbinden:**
   ```latex
   \begin{figure}[h]
     \centering
     \includegraphics[width=0.8\textwidth]{diagrams/system_architecture.pdf}
     \caption{System-Architektur des Rüsselsheim Chatbots}
     \label{fig:architecture}
   \end{figure}
   ```

5. **Kompilieren:**
   ```bash
   pdflatex main.tex
   bibtex main
   pdflatex main.tex
   pdflatex main.tex
   ```

### Option B: Microsoft Word (Springer/Elsevier Template)

1. **Template herunterladen:**
   - Springer: https://www.springer.com/gp/authors-editors/conference-proceedings/conference-proceedings-guidelines
   - Elsevier: https://www.elsevier.com/authors/policies-and-guidelines/latex-instructions

2. **Markdown-Text kopieren:**
   - Öffne `.md`-Dateien
   - Kopiere Text → Word
   - Formatiere mit Template-Styles

3. **Diagramme einfügen:**
   - Mermaid → PNG exportieren (1920x1080)
   - Einfügen → Bild → Größe anpassen

4. **Referenzen:**
   - Nutze Word's Zitat-Manager
   - Oder: Copy-Paste aus `Literatur_Zusammenfassung.md`

---

## 🎤 PowerPoint-Präsentation erstellen

### Schritt 1: Template wählen

- **Academic Templates:** https://slidesgo.com/themes/academic
- **IEEE Style:** Blau-Weiß, minimalistisch
- **Uni-Template:** Falls deine Uni eins hat

### Schritt 2: Folien übertragen

1. Öffne `PowerPoint_Praesentation.md`
2. Jede `# FOLIE X` = Eine neue Slide
3. Kopiere Content 1:1
4. Füge Diagramme ein (siehe unten)

### Schritt 3: Diagramme exportieren

**Online (einfach):**
1. Gehe zu https://mermaid.live
2. Kopiere Diagramm-Code aus `Architektur_Diagramme.md`
3. Klick "Export PNG" (1920x1080)
4. Einfügen in PowerPoint

**CLI (fortgeschritten):**
```bash
npm install -g @mermaid-js/mermaid-cli
mmdc -i diagram.mmd -o diagram.png -w 1920 -H 1080
```

### Schritt 4: Timing üben

- Gesamt: 20 Minuten
- Einleitung: 3 Min (Folien 1-3)
- Stand der Technik: 4 Min (Folien 4-6)
- Implementierung: 9 Min (Folien 7-12)
- Evaluation: 3 Min (Folien 13-14)
- Zusammenfassung: 1 Min (Folie 15)

**Probelauf mit Timer durchführen!**

---

## 📚 Literatur-Referenzen

### Alle Papers sind in `Literatur_Zusammenfassung.md` dokumentiert

**Top 5 Must-Cite Papers:**
1. Wang et al. (2024) - LLMs in Smart Government (ACM)
2. Gao et al. (2024) - Comprehensive RAG Survey (arXiv)
3. Karamanolakis et al. (2024) - E-Government RAG Architecture (MDPI)
4. Zhu et al. (2024) - RAG Evaluation Survey (arXiv)
5. Reimers & Gurevych (2019) - Sentence-BERT (EMNLP)

**Zitier-Format (IEEE):**
```
[1] X. Wang et al., "Applications and Challenges of Large Language Models in Smart Government,"
    in Proc. 2024 3rd Int. Conf. Frontiers of Artificial Intelligence and Machine Learning (FAIM),
    2024, pp. 1-10.
```

### BibTeX Export (für LaTeX)

```bibtex
@inproceedings{wang2024llm,
  title={Applications and Challenges of Large Language Models in Smart Government},
  author={Wang, X. and others},
  booktitle={Proceedings of the 2024 3rd International Conference on Frontiers of Artificial Intelligence and Machine Learning},
  year={2024},
  organization={ACM}
}
```

Alle BibTeX-Entries in `Literatur_Zusammenfassung.md` → einfach kopieren!

---

## ✅ Checkliste: Was ist fertig?

### ✅ Code & Implementation (100%)
- [x] RAG-System implementiert
- [x] 9 API-Integrationen
- [x] Multi-Provider LLM-Architektur
- [x] Web Scraper
- [x] Evaluation-Framework
- [x] 27 Tests (alle bestanden)
- [x] Docker-Deployment

### ✅ Paper-Materialien (70%)
- [x] Literatur-Recherche (25+ Papers)
- [x] Teil 3: Stand der Technik (fertig)
- [x] Teil 4: Lösung (fertig)
- [x] Teil 5: Evaluation (Template)
- [x] Architektur-Diagramme (6 Stück)
- [ ] Teil 1: Einleitung (DU)
- [ ] Teil 2: Motivation (DU)
- [ ] Teil 6: Diskussion (DU)
- [ ] Teil 7: Zusammenfassung (DU)

### ✅ Präsentation (80%)
- [x] PowerPoint-Struktur (16 Folien)
- [x] Technische Folien (7-12) mit Content
- [x] Stand der Technik Folien (4-6)
- [ ] Einleitungs-Folien (1-3) - DU
- [ ] Zusammenfassungs-Folie (15) - DU
- [ ] Evaluation-Folie (14) - Nach Test

---

## 🎯 Nächste Schritte (Priorität)

### 1. **JETZT: Evaluation durchführen** (30 Min)
```bash
# Gemini API Key hinzufügen
nano backend/.env

# Backend neu starten
docker-compose restart backend

# Evaluation laufen lassen
curl -X POST http://localhost:8000/api/evaluation/evaluate/batch \
  | python3 -m json.tool > evaluation_results.json

# Ergebnisse analysieren
cat evaluation_results.json
```

### 2. **Teil 5 ausfüllen** (1-2 Stunden)
- Zahlen aus `evaluation_results.json` einfügen
- Beispiel-Dialoge kopieren
- Grafiken erstellen (Python/Excel)
- Interpretation schreiben

### 3. **Deine Teile schreiben** (3-4 Stunden)
- Teil 1: Einleitung (0.5h)
- Teil 2: Motivation (0.5h)
- Teil 6: Diskussion (1-2h)
- Teil 7: Zusammenfassung (0.5h)

### 4. **Paper formatieren** (2-3 Stunden)
- Template auswählen (IEEE/ACM/Springer)
- Alle Teile zusammenfügen
- Diagramme einfügen
- Referenzen formatieren
- Korrektur lesen

### 5. **PowerPoint erstellen** (2-3 Stunden)
- Template wählen
- Folien übertragen
- Diagramme einfügen
- Probelauf mit Timer

### 6. **Probelauf** (1 Stunde)
- Präsentation durchsprechen (20 Min)
- Fragen vorbereiten (10 Min)
- Ggf. anpassen

---

## 💡 Tipps & Tricks

### Paper-Schreiben
- **Absätze:** Max 5-7 Sätze pro Absatz
- **Sätze:** Max 20 Wörter pro Satz (Ausnahmen OK)
- **Passiv vs. Aktiv:** "Wir implementieren" > "Es wurde implementiert"
- **Figures:** Immer im Text referenzieren ("Abbildung 1 zeigt...")
- **Code:** Syntax-Highlighting nutzen (Listings Package in LaTeX)

### Präsentation
- **Font Size:** Mindestens 18pt für Text, 24pt für Überschriften
- **Bilder:** Mindestens 1920x1080, keine verpixelten Screenshots
- **Animationen:** Sparsam! Nur bei sequentiellen Diagrammen (z.B. RAG-Flow)
- **Sprecher-Notizen:** Nutzen! Hilft gegen Blackout
- **Zeitplanung:** 1-2 Minuten pro Folie (außer Titel/Zusammenfassung)

### Evaluation
- **Reproduzierbarkeit:** JSON-Datei aufbewahren + Git committen
- **Screenshots:** Mach Screenshots von erfolgreichen Antworten
- **Fehleranalyse:** Wenn Evaluation fehlschlägt, Logs checken:
  ```bash
  docker-compose logs backend --tail=100
  ```

---

## 📞 Hilfe & Support

### Probleme mit der Evaluation?

**Problem:** "Network is unreachable" bei Evaluation
```bash
# Lösung: Gemini API Key prüfen
cat backend/.env | grep GEMINI_API_KEY

# Sollte NICHT leer sein!
# Falls leer: Key von https://ai.google.dev/ holen
```

**Problem:** "No documents found" bei RAG-Suche
```bash
# Lösung: Dokumente importieren
curl -X POST http://localhost:8000/api/documents/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Personalausweis beantragen",
    "content": "Um einen Personalausweis zu beantragen...",
    "category": "verwaltung"
  }'
```

**Problem:** Backend startet nicht
```bash
# Logs checken
docker-compose logs backend

# Häufigste Fehler:
# - PostgreSQL nicht bereit → Warten 30s
# - Port 8000 belegt → docker-compose down && docker-compose up
```

### Fragen zur Hausarbeit?

- **Struktur unklar?** → Schau dir IEEE-Beispiel-Papers an
- **Zu lang/kurz?** → Conference-Format = komprimiert, viele Infos auf wenig Platz
- **Zitier-Stil?** → IEEE: [1], [2], ... / Harvard: (Autor, Jahr)

---

## 🎓 Finale Checkliste

### Bevor du abgibst:

**Paper:**
- [ ] Alle Teile 1-7 geschrieben
- [ ] Referenzen vollständig und formatiert
- [ ] Alle Diagramme eingefügt mit Beschriftung
- [ ] Abstract geschrieben (150-200 Wörter)
- [ ] Seitenzahl stimmt (8-10 Seiten)
- [ ] Korrektur gelesen (Rechtschreibung, Grammatik)
- [ ] PDF exportiert und geprüft (keine Layout-Fehler)

**Präsentation:**
- [ ] Alle 16 Folien fertig
- [ ] Diagramme in hoher Auflösung
- [ ] Probelauf durchgeführt (20 Min Timer!)
- [ ] Sprecher-Notizen vorbereitet
- [ ] Backup auf USB-Stick (falls Laptop ausfällt)

**Code:**
- [ ] Alle Tests bestehen: `pytest backend/tests/`
- [ ] Evaluation-Ergebnisse dokumentiert
- [ ] README aktualisiert
- [ ] Git committed & pushed

---

**Viel Erfolg! 🚀**

*Bei Fragen: Check die Kommentare in den Dateien oder GitHub Issues.*
