# LLM Data Copilot

## Project Summary

LLM Data Copilot is a prototype AI agent that converts natural-language business questions into SQL queries.

The main goal of the project is to democratize access to structured data inside an organization. Instead of relying on the data team for every ad-hoc request, business users can describe what they need in plain language and receive a SQL query aligned with the underlying schema.

This project was built as a practical exploration of LLM applications in enterprise data environments, with a strong focus on retrieval, grounding, and SQL generation.

## Business Problem

In many organizations, consultants and business stakeholders need fast access to insights stored in data warehouses, but they do not know SQL. This creates a dependency on data professionals for relatively simple analytical questions and slows down decision-making.

This project addresses that gap by introducing a natural-language interface for structured data access.

## Solution Overview

The solution uses a Retrieval-Augmented Generation (RAG) approach:

1. A user submits a question in natural language.
2. The system retrieves semantically similar examples and schema-related context.
3. A language model receives the retrieved context.
4. The model generates a SQL query grounded in the retrieved material.

The objective is not just to generate SQL, but to generate SQL that is consistent with real database structures and existing business logic.

## Current Architecture

### 1. Query and Context Assets

The project stores context assets such as:

- example SQL queries
- natural-language examples mapped to SQL
- table and business-rule documentation

Relevant folders:

- `queries/`
- `data_dictionary/`
- `prompts/`

### 2. Embedding Pipeline

The embedding layer transforms SQL examples and related context into vector representations for semantic retrieval.

Relevant scripts:

- `create_embedding.py`
- `create_embedding_from_examples.py`

### 3. Retrieval Layer

The retrieval layer uses a FAISS vector store to find the most relevant examples based on the user's question.

Relevant assets:

- `vectorstore/`
- `query_agent.py`

### 4. SQL Generation Layer

The SQL generation layer uses an LLM to produce a new SQL query based on the retrieved examples.

Relevant script:

- `generate_sql.py`

### 5. Entry Point

The current project includes a simple entry point and modular scripts for experimentation.

Relevant file:

- `main.py`

## Design Decisions

### Grounding Before Generation

A major design decision in this project is to retrieve real examples before query generation.

This was done to reduce hallucinations and improve schema adherence. Instead of asking the model to generate SQL from scratch, the system first provides examples and context that reflect actual query patterns used in the project.

### Practical Enterprise Orientation

The project was designed around a realistic enterprise use case rather than a toy demo. The focus is on helping non-technical users interact with real structured data in a safer and more scalable way.

## Current Limitations

This repository represents an early functional prototype, so some areas can still be improved, such as:

- stronger SQL validation
- schema-aware guardrails
- support for more query examples
- better separation between orchestration and interface layers
- improved documentation and testing

## What a Reviewer Should Look At First

If you are reviewing this repository, the best files to start with are:

1. `README.md` for the high-level overview
2. `generate_sql.py` for the SQL generation flow
3. `query_agent.py` for retrieval behavior
4. `create_embedding_from_examples.py` for how semantic context is built

## Suggested Review Goal

Review this project as an early-stage AI data assistant focused on natural-language-to-SQL generation, retrieval grounding, and practical use in business analytics environments.
