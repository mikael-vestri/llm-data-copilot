# Architecture Overview

This document describes the current architecture of the LLM Data Copilot project.

## High-Level Flow

```text
User Question
     ↓
Semantic Retrieval
     ↓
Relevant Context (examples + schema hints)
     ↓
LLM Prompt Construction
     ↓
SQL Generation
     ↓
Suggested SQL Output
```

## Architecture Components

### 1. User Input Layer

The flow starts when a user submits an analytical question in natural language.

Example:

> "What are the tax savings for Texas in 2025?"

At this stage, the problem is expressed in business language rather than SQL.

### 2. Retrieval Layer

The retrieval layer searches for semantically similar examples stored in a FAISS vector store.

Purpose:

- identify similar prior requests
- recover real SQL patterns
- provide grounding context to the LLM

Relevant components:

- `vectorstore/`
- `create_embedding.py`
- `create_embedding_from_examples.py`
- `query_agent.py`

### 3. Context Layer

The retrieved material acts as working context for the model.

This context may include:

- natural-language example requests
- corresponding SQL queries
- metadata about business meaning
- schema-related hints

Relevant source folders:

- `queries/`
- `data_dictionary/`
- `prompts/`

### 4. Prompt Construction Layer

After retrieval, the system builds a prompt that combines:

- the user's question
- retrieved examples
- guidance for SQL generation

This prompt is then sent to the language model.

Relevant component:

- `generate_sql.py`

### 5. SQL Generation Layer

The LLM generates a candidate SQL query intended to answer the user's request.

The generated query is expected to follow the structure and style of the retrieved examples rather than relying only on the model's general prior knowledge.

### 6. Output Layer

The current output of the system is a suggested SQL query shown to the user.

At this prototype stage, the system focuses on generation rather than direct execution.

## Why This Architecture Was Chosen

The project was designed around a Retrieval-Augmented Generation approach because pure prompt-based SQL generation is more vulnerable to hallucinations.

By retrieving real examples before generation, the system increases the likelihood that the generated SQL:

- follows known schema conventions
- reflects actual business logic
- uses realistic analytical query patterns

## Current Strengths

- practical business use case
- simple and understandable architecture
- grounding through semantic retrieval
- clear separation between embedding and generation steps

## Current Gaps

The current prototype can be improved with:

- stronger modularization
- richer schema documentation
- automated SQL validation
- logging and observability
- unit tests and integration tests
- safer handling of environment configuration

## Suggested Next Architecture Evolution

A stronger next version of this project could evolve into the following flow:

```text
User Question
     ↓
Intent Detection
     ↓
Semantic Retrieval
     ↓
Prompt Builder
     ↓
LLM SQL Generation
     ↓
SQL Validation
     ↓
Optional Query Explanation
     ↓
Final Output
```

This would make the system more robust and more suitable for production-style review.
