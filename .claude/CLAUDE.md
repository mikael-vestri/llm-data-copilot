# LLM Data Copilot

## Project Summary

LLM Data Copilot is a RAG-based prototype that converts natural-language questions into SQL. Business users describe what they need in plain language and receive a SQL query grounded in example queries and schema context.

## Structure

- `agents/sql_agent.py` — RAG agent (retrieval + SQL generation). Loads FAISS from `vectorstore_enhanced/`.
- `queries/examples.json` — NL-to-SQL examples (input, query, metadata). Source for embeddings.
- `scripts/create_embeddings_hybrid.py` — Builds FAISS index from `queries/examples.json`. Run from repo root.
- `scripts/inspect_vectorstore.py` — Optional: inspect vector store contents.
- `scripts/legacy/` — Older/experimental scripts; not required to run the app.
- `main.py` — CLI entry point (`python main.py`).
- `ui.py` — Streamlit web UI (`streamlit run ui.py`).
- `docs/ARCHITECTURE.md` — Architecture overview.

## Run (from repo root, with venv active)

1. Build index (once): `python scripts/create_embeddings_hybrid.py`
2. CLI: `python main.py` | Web: `streamlit run ui.py`

## Conventions

- Python 3.10+. Env vars in `.env` (see `.env.example`). No secrets in repo.
- Demo data only in `queries/examples.json` (generic schema: properties, clients, property_values).
- For reviews: start with `README.md`, then `agents/sql_agent.py`, then `scripts/create_embeddings_hybrid.py`.
