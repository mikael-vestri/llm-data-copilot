# LLM Data Copilot

LLM Data Copilot is a prototype AI agent that translates natural-language business questions into SQL queries.

The project was built to explore how large language models can improve access to structured data in business environments, especially for users who need insights from a database but do not know SQL.

## Problem Statement

In many organizations, non-technical users depend on data professionals to write SQL for ad-hoc analytical requests. This creates bottlenecks, slows down decision-making, and limits access to data.

This project addresses that problem by using a retrieval-grounded LLM workflow capable of converting business questions into SQL queries aligned with real query examples and schema context.

## Solution Approach

The current prototype follows a Retrieval-Augmented Generation approach:

1. The user asks a question in natural language.
2. The system retrieves semantically similar examples from a vector store.
3. The LLM receives the retrieved context.
4. The model generates a SQL query grounded in the retrieved examples.

A key design decision in this project is grounding before generation. Instead of relying only on the language model's prior knowledge, the system first retrieves relevant examples to reduce hallucinations and improve schema adherence.

## Current Repository Structure

```text
llm-data-copilot/
├── app/                               # Reserved interface layer
├── data_dictionary/                   # Schema and business-context assets
├── prompts/                           # Prompt-related assets
├── queries/                           # SQL examples and NL-to-SQL examples
├── vectorstore/                       # Local FAISS index generated from examples
├── create_embedding.py                # Creates embeddings from a SQL asset
├── create_embedding_from_examples.py  # Creates embeddings from NL-to-SQL examples
├── fix_multiple_queries.py            # Utility script for query cleanup/experiments
├── generate_sql.py                    # Main SQL generation flow
├── inspect_vectorstore.py             # Vector store inspection utility
├── main.py                            # Minimal entry point
├── query_agent.py                     # Retrieval-based query lookup flow
├── requirements.txt                   # Project dependencies
└── README.md                          # Project documentation
```

## Main Components

### 1. Embedding Layer

The project converts examples into embeddings and stores them in a FAISS vector index for semantic retrieval.

Relevant scripts:

- `create_embedding.py`
- `create_embedding_from_examples.py`

### 2. Retrieval Layer

The retrieval layer searches the vector store for similar examples based on the user's question.

Relevant component:

- `query_agent.py`

### 3. SQL Generation Layer

The SQL generation flow uses retrieved examples as context for an LLM to generate a new SQL query.

Relevant component:

- `generate_sql.py`

## Example Use Case

User question:

> "What are the tax savings for Texas in 2025?"

Expected behavior:

- retrieve similar examples
- pass grounded context to the model
- return a candidate SQL query consistent with known patterns

## Setup

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd llm-data-copilot
```

### 2. Create and activate a virtual environment

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create a `.env` file

```env
OPENAI_API_KEY=your_api_key_here
```

## How to Run

### Build embeddings from example inputs

```bash
python create_embedding_from_examples.py
```

### Retrieve the closest matching example

```bash
python query_agent.py
```

### Generate SQL from a natural-language question

```bash
python generate_sql.py
```

## Notes for Reviewers

This repository should be reviewed as an early functional prototype, not as a fully productionized system.

What it already demonstrates well:

- practical LLM application for analytics
- retrieval-grounded SQL generation
- business-oriented AI use case
- awareness of hallucination risk in structured-data tasks

## Current Limitations

This version can be improved in several ways:

- richer schema documentation in `data_dictionary/`
- stronger SQL validation
- better modularization of orchestration logic
- automated tests
- more examples in the vector store
- a clearer interface layer in `app/`

## Recommended Next Improvements

Possible next steps include:

1. Add SQL validation and schema checks
2. Expand the example library used for retrieval
3. Separate retrieval, prompt building, and generation into clearer modules
4. Add tests and logging
5. Add a lightweight interface for user interaction

## Related Documentation

For additional context, see:

- `cloud.md`
- `skills.md`
- `ARCHITECTURE.md`
