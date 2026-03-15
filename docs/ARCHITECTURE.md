# Architecture Overview

This document describes the architecture of the LLM Data Copilot project.

## High-Level Flow

```text
User Question
     ↓
Semantic Retrieval (FAISS)
     ↓
Relevant Context (examples + schema hints)
     ↓
LLM Prompt Construction
     ↓
SQL Generation
     ↓
Suggested SQL Output
```

## Repository structure

```text
llm-data-copilot/
├── agents/
│   └── sql_agent.py              # RAG agent: retrieval + SQL generation
├── queries/
│   └── examples.json             # NL-to-SQL examples (input + query + metadata)
├── scripts/
│   ├── create_embeddings_hybrid.py  # Builds FAISS index from examples.json
│   ├── inspect_vectorstore.py      # Optional: inspect vector store contents
│   └── legacy/                      # Older/experimental scripts
├── docs/
│   └── ARCHITECTURE.md
├── main.py                         # CLI entry point
├── ui.py                           # Streamlit web UI
├── requirements.txt
├── .env.example
└── README.md
```

## Components

### 1. User Input

The user submits an analytical question in natural language (e.g. *"What are the tax savings by client for 2025?"*).

### 2. Retrieval Layer

- **Vector store:** FAISS index built from `queries/examples.json` (run `create_embeddings_hybrid.py`).
- **Agent:** `agents/sql_agent.py` loads the index and retrieves the top-k similar examples by semantic similarity.

### 3. Context & Prompt

The agent builds a prompt with the user question, retrieved NL-to-SQL examples, and database context (tables, common fields). This prompt is sent to the LLM.

### 4. SQL Generation

The LLM returns a candidate SQL query. The agent optionally validates that the query is read-only (no INSERT/UPDATE/DELETE).

### 5. Output

The generated SQL is shown in the CLI or in the Streamlit UI (`ui.py`).

## Design Choices

- **RAG (Retrieval-Augmented Generation):** Reduces hallucinations by grounding the LLM in real example queries and schema context.
- **No execution:** The prototype only suggests SQL; it does not run it against a database.

## Possible Next Steps

- SQL validation against a schema
- Logging and observability
- Unit and integration tests
- Optional query explanation (natural language summary of the SQL)
