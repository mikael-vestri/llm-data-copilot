# LLM Data Copilot

A prototype **RAG-based** application that converts natural-language questions into SQL. It uses semantic search over example queries and an LLM to generate SQL aligned with the retrieved patterns—suitable for analytics and reporting use cases where non-SQL users need to query structured data.

## What it does

1. **You ask** a question in plain language (e.g. *"What are the total taxable values by client for 2025?"*).
2. **The system** finds similar example questions and their SQL in a vector store (FAISS).
3. **An LLM** produces a SQL query grounded in those examples and in the described schema.
4. **You get** a suggested SQL query (read-only; the app does not execute it).

## Repository structure

```text
llm-data-copilot/
├── agents/
│   └── sql_agent.py              # RAG agent (retrieval + SQL generation)
├── queries/
│   └── examples.json             # Example NL questions and SQL (used for embeddings)
├── scripts/
│   ├── create_embeddings_hybrid.py   # Build FAISS index from examples
│   ├── inspect_vectorstore.py       # Optional: inspect index contents
│   └── legacy/                        # Older/experimental scripts (not required)
├── docs/
│   └── ARCHITECTURE.md           # Architecture overview
├── main.py                       # CLI entry point (interactive agent)
├── ui.py                         # Streamlit web interface
├── requirements.txt
├── .env.example                  # Template for environment variables
└── README.md
```

## Prerequisites

- **Python 3.10+**
- **OpenAI API key** (for embeddings and the LLM)

## Setup

### 1. Clone and enter the repo

```bash
git clone https://github.com/mikael-vestri/llm-data-copilot.git
cd llm-data-copilot
```

### 2. Create and activate a virtual environment

**Windows (PowerShell):**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

*(If script execution is disabled, run once: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`.)*

**macOS / Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Copy the example file and add your OpenAI API key:

```bash
cp .env.example .env
```

Edit `.env` and set:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

**Do not commit `.env`**—it is listed in `.gitignore`.

### 5. Build the vector index

The app needs a FAISS index built from the example queries. From the repo root:

```bash
python scripts/create_embeddings_hybrid.py
```

This reads `queries/examples.json` and writes the index under `vectorstore_enhanced/`. Run once (or after changing the examples).

## How to run

### Option A: Command line

```bash
python main.py
```

Enter your question when prompted. Type `exit` or `quit` to stop.

### Option B: Web UI (Streamlit)

```bash
streamlit run ui.py
```

Open the URL shown in the terminal (e.g. http://localhost:8501) and type your question in the text box.

## Example questions (demo data)

The included `queries/examples.json` uses a generic schema (e.g. `properties`, `clients`, `property_values`). You can try:

- *"How many properties do we have per client for the current tax year?"*
- *"What are the total taxable values and tax amounts by client for 2025?"*
- *"Which properties have missing tax values for 2025?"*
- *"Show tax savings by client for 2025."*
- *"List the top 10 clients by total tax due in 2025."*

## Documentation

- [Architecture overview](docs/ARCHITECTURE.md) — flow, components, and design choices.

## Security and privacy

- **Secrets:** No API keys or secrets are stored in the repo. Use `.env` (from `.env.example`) and keep `.env` out of version control.
- **Data:** The repo only includes generic demo examples in `queries/examples.json`; no internal or production data is included.

## License and use

This project is a portfolio prototype. You are welcome to clone it, run it with your own API key, and adapt it for learning or evaluation.
