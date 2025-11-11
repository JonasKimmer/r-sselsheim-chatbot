# Architektur-Diagramme für die Hausarbeit

## Diagramm 1: System-Architektur Übersicht

```mermaid
graph TB
    subgraph "Client Layer"
        User[👤 Bürger]
        Frontend[Next.js Frontend<br/>React + TypeScript]
    end

    subgraph "API Gateway"
        FastAPI[FastAPI Backend<br/>Python]
    end

    subgraph "Services Layer"
        ChatService[Chat Service<br/>Orchestration]
        RAGService[RAG Service<br/>Retrieval-Augmented<br/>Generation]
        LLMService[LLM Service<br/>Multi-Provider]
        APIServices[External APIs<br/>9 Integrationen]
        ScraperService[Web Scraper<br/>ruesselsheim.de]
    end

    subgraph "LLM Providers"
        Ollama[Ollama<br/>Llama 3.1<br/>🔒 On-Premise]
        Gemini[Google Gemini<br/>1.5 Flash<br/>☁️ Free Tier]
        Claude[Anthropic Claude<br/>3.5 Sonnet<br/>💎 Premium]
    end

    subgraph "Data Layer"
        PostgreSQL[(PostgreSQL<br/>+ pgvector)]
        Redis[(Redis Cache)]
    end

    subgraph "External APIs"
        Weather[☀️ Weather API]
        Transit[🚆 RMV Transit]
        Traffic[🚗 Traffic API]
        Waste[🗑️ Waste API]
        Fuel[⛽ Fuel Prices]
        Others[📍 Maps, 🎉 Events,<br/>📰 News, 🏖️ Holidays]
    end

    User --> Frontend
    Frontend -->|REST API| FastAPI
    FastAPI --> ChatService
    ChatService --> RAGService
    ChatService --> LLMService
    ChatService --> APIServices
    FastAPI --> ScraperService

    RAGService --> PostgreSQL
    RAGService -->|Embeddings<br/>384-dim| PostgreSQL
    LLMService -->|Response| ChatService

    LLMService -.->|Provider<br/>Selection| Ollama
    LLMService -.->|Provider<br/>Selection| Gemini
    LLMService -.->|Provider<br/>Selection| Claude

    APIServices --> Weather
    APIServices --> Transit
    APIServices --> Traffic
    APIServices --> Waste
    APIServices --> Fuel
    APIServices --> Others

    ScraperService -->|BeautifulSoup| PostgreSQL

    ChatService --> Redis

    style Ollama fill:#90EE90
    style Gemini fill:#87CEEB
    style Claude fill:#FFB6C1
    style PostgreSQL fill:#336791,color:#fff
    style Frontend fill:#61DAFB,color:#000
```

---

## Diagramm 2: RAG-Flow (Retrieval-Augmented Generation)

```mermaid
sequenceDiagram
    participant User as 👤 Bürger
    participant Frontend as Frontend
    participant API as FastAPI
    participant Chat as Chat Service
    participant RAG as RAG Service
    participant LLM as LLM Service
    participant DB as PostgreSQL<br/>+ pgvector
    participant Provider as LLM Provider<br/>(Ollama/Gemini/Claude)

    User->>Frontend: "Wie beantrage ich<br/>einen Personalausweis?"
    Frontend->>API: POST /api/chat/
    API->>Chat: get_response(message)

    %% RAG Search
    Chat->>RAG: search(query, limit=3)
    RAG->>RAG: Generate Query Embedding<br/>(384-dim Vektor)
    RAG->>DB: Cosine Similarity Search<br/>SELECT ... ORDER BY embedding <=> query
    DB-->>RAG: Top 3 relevante Dokumente<br/>[Doc1: score=0.87, Doc2: score=0.81, Doc3: score=0.73]
    RAG-->>Chat: Retrieved Context

    %% LLM Generation
    Chat->>Chat: Build Prompt with Context:<br/>"Du bist Assistent für Rüsselsheim.<br/>Basierend auf:<br/>[Dokumente...]<br/>Frage: ..."
    Chat->>LLM: generate(prompt, tools)
    LLM->>Provider: API Call mit Prompt
    Provider-->>LLM: Generated Response
    LLM-->>Chat: "Um einen Personalausweis zu beantragen,<br/>benötigen Sie: 1. Biometrisches Foto..."

    Chat-->>API: Response + Metadata
    API-->>Frontend: JSON Response
    Frontend-->>User: Chat-Nachricht mit Antwort

    Note over RAG,DB: Retrieval Time: ~50-150ms
    Note over LLM,Provider: Generation Time: ~1-3s
    Note over User,Frontend: Total Time: ~2-4s
```

---

## Diagramm 3: Multi-Provider LLM-Architektur

```mermaid
graph TB
    subgraph "LLM Service (Abstraction Layer)"
        Config[Config File<br/>.env]
        Factory[Provider Factory<br/>Strategy Pattern]

        subgraph "Provider Implementations"
            OllamaClient[Ollama Client]
            GeminiClient[Gemini Client]
            ClaudeClient[Claude Client]
        end
    end

    subgraph "External Providers"
        OllamaServer[Ollama Server<br/>http://localhost:11434<br/>🔒 On-Premise]
        GeminiAPI[Google Gemini API<br/>ai.google.dev<br/>☁️ Cloud]
        ClaudeAPI[Anthropic API<br/>api.anthropic.com<br/>☁️ Cloud]
    end

    Config -->|LLM_PROVIDER=ollama| Factory
    Factory -->|Instantiate| OllamaClient
    Factory -->|Instantiate| GeminiClient
    Factory -->|Instantiate| ClaudeClient

    OllamaClient -->|REST API| OllamaServer
    GeminiClient -->|REST API| GeminiAPI
    ClaudeClient -->|REST API| ClaudeAPI

    subgraph "Comparison"
        Table["Provider | Kosten | Datenschutz | Qualität<br/>━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━<br/>Ollama | €0 API | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐<br/>Gemini | €0 Free | ⭐⭐⭐ | ⭐⭐⭐⭐<br/>Claude | ~€0.003/req | ⭐⭐⭐ | ⭐⭐⭐⭐⭐"]
    end

    style OllamaServer fill:#90EE90
    style GeminiAPI fill:#87CEEB
    style ClaudeAPI fill:#FFB6C1
    style Config fill:#FFE4B5
```

---

## Diagramm 4: Deployment-Architektur (Docker Compose)

```mermaid
graph TB
    subgraph "Docker Host Machine"
        subgraph "Docker Network: ruesselsheim_network"

            subgraph "Frontend Container"
                NextJS[Next.js App<br/>Port: 3000]
            end

            subgraph "Backend Container"
                FastAPIApp[FastAPI App<br/>Port: 8000]
                SentenceTransformers[Sentence Transformers<br/>paraphrase-multilingual-MiniLM]
            end

            subgraph "Database Container"
                PG[PostgreSQL 15<br/>+ pgvector]
                PGData[(Persistent Volume<br/>postgres_data)]
            end

            subgraph "Nginx Container (Production)"
                Nginx[Nginx Reverse Proxy<br/>Port: 80, 443]
                SSL[SSL/TLS<br/>Let's Encrypt]
            end

        end

        subgraph "Host Machine (Optional)"
            OllamaHost[Ollama Service<br/>Port: 11434<br/>host.docker.internal]
        end
    end

    subgraph "External Services"
        GeminiExt[☁️ Google Gemini]
        ClaudeExt[☁️ Anthropic Claude]
        APIs[☁️ 9 External APIs<br/>Weather, Transit, etc.]
    end

    Internet[🌐 Internet<br/>Bürger] --> Nginx
    Nginx --> NextJS
    Nginx --> FastAPIApp

    NextJS -.->|API Calls| FastAPIApp
    FastAPIApp --> PG
    PG --> PGData
    FastAPIApp -.->|Embeddings| SentenceTransformers

    FastAPIApp -.->|LLM Calls| OllamaHost
    FastAPIApp -.->|LLM Calls| GeminiExt
    FastAPIApp -.->|LLM Calls| ClaudeExt
    FastAPIApp -.->|API Calls| APIs

    style PG fill:#336791,color:#fff
    style FastAPIApp fill:#009688,color:#fff
    style NextJS fill:#61DAFB,color:#000
    style Nginx fill:#269539,color:#fff
    style OllamaHost fill:#90EE90
```

---

## Diagramm 5: RAG Document Lifecycle

```mermaid
stateDiagram-v2
    [*] --> WebScraping: ruesselsheim.de
    [*] --> ManualImport: Admin Portal
    [*] --> APIImport: External Data

    WebScraping --> TextExtraction
    ManualImport --> TextExtraction
    APIImport --> TextExtraction

    TextExtraction --> EmbeddingGeneration: BeautifulSoup<br/>HTML → Plain Text

    EmbeddingGeneration --> VectorStorage: Sentence Transformers<br/>Text → 384-dim Vector

    VectorStorage --> IndexCreation: pgvector<br/>IVFFlat Index

    IndexCreation --> SearchReady: Ready for Queries

    SearchReady --> Retrieval: User Query

    Retrieval --> ContextAugmentation: Top-K Documents<br/>(k=3)

    ContextAugmentation --> LLMGeneration: Prompt + Context

    LLMGeneration --> Response: Answer to User

    Response --> [*]

    SearchReady --> Update: Document Update
    Update --> EmbeddingGeneration: Re-Embed

    SearchReady --> Delete: Document Removal
    Delete --> [*]
```

---

## Diagramm 6: Evaluation Framework

```mermaid
graph LR
    subgraph "Test Dataset"
        Q1[Verwaltung<br/>5 Fragen]
        Q2[Wetter<br/>3 Fragen]
        Q3[Verkehr<br/>3 Fragen]
        Q4[Abfall<br/>3 Fragen]
        Q5[Weitere<br/>7 Fragen]
    end

    subgraph "Evaluation Service"
        BatchEval[Batch Evaluator]
        Metrics[Metrics Collector]
    end

    subgraph "Measurements"
        Time[⏱️ Response Time<br/>Search + Generation]
        Retrieval[🎯 Retrieval Score<br/>Cosine Similarity]
        Accuracy[✅ Category Match<br/>Expected vs. Retrieved]
        Success[✔️ Success Rate<br/>Answered vs. Failed]
    end

    subgraph "Results"
        Summary[📊 Summary Statistics<br/>Avg, Min, Max, P95]
        Details[📋 Detailed Results<br/>Per-Question Metrics]
        Export[💾 Export<br/>JSON, CSV, LaTeX]
    end

    Q1 --> BatchEval
    Q2 --> BatchEval
    Q3 --> BatchEval
    Q4 --> BatchEval
    Q5 --> BatchEval

    BatchEval --> Metrics

    Metrics --> Time
    Metrics --> Retrieval
    Metrics --> Accuracy
    Metrics --> Success

    Time --> Summary
    Retrieval --> Summary
    Accuracy --> Summary
    Success --> Summary

    Summary --> Details
    Details --> Export

    style Summary fill:#90EE90
    style Export fill:#FFB6C1
```

---

## Verwendung der Diagramme

**Für die Hausarbeit (LaTeX/Word):**
1. Mermaid → PNG/SVG konvertieren via mermaid.live oder CLI
2. Diagramme in Paper einbinden mit Bildunterschriften
3. Referenzieren im Text: "Abbildung 1 zeigt die System-Architektur..."

**Für die PowerPoint:**
1. PNG Export in hoher Auflösung (300 DPI)
2. Pro Folie ein Diagramm mit Erklärung
3. Animationen für sequentielle Darstellung (z.B. RAG-Flow)

**Mermaid Live Editor:**
https://mermaid.live - Diagramme dort einfügen und als PNG/SVG exportieren

**CLI Export (falls mermaid-cli installiert):**
```bash
mmdc -i diagram.mmd -o diagram.png -w 1920 -H 1080
```
