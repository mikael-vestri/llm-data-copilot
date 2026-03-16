---
name: llm-data-copilot-agent
description: Use when working on or reviewing the LLM Data Copilot project—agent capabilities, RAG/SQL generation, grounding, schema awareness, and portfolio readiness. Covers expected behavior of the NL-to-SQL agent and improvement goals for the codebase.
---

# Agent Skills

This document describes the expected capabilities of the LLM Data Copilot agent.

The purpose of the agent is to translate business questions written in natural language into SQL queries that are relevant, syntactically valid, and grounded in available schema context.

## Primary Skill Set

### 1. Natural Language Understanding

The agent should understand analytical requests expressed in plain language.

Examples:

- "Show tax savings for Texas in 2025"
- "List potential revenue by project"
- "Return properties with revised value changes"

The agent must infer:

- analytical intent
- likely entities involved
- filters, dimensions, and metrics
- whether aggregation is needed

### 2. Retrieval-Grounded Reasoning

The agent should not generate SQL blindly.

Before generating a query, it should retrieve the most relevant examples and context from the vector store. The retrieved context should help the model stay aligned with real query patterns and business logic.

The agent must use retrieved context as grounding material, not as optional decoration.

### 3. Schema Awareness

The agent should remain consistent with the data structures described in the repository.

It must rely on available assets such as:

- `queries/`
- `data_dictionary/`
- retrieved SQL examples
- metadata stored in the vector index

The agent should avoid inventing tables, columns, joins, or filters that are not supported by the known context.

### 4. SQL Generation

The agent should generate SQL that:

- reflects the user's analytical request
- follows the schema patterns observed in examples
- uses valid SQL structure
- is readable and logically organized
- is as close as possible to production-style analytical SQL

### 5. Hallucination Mitigation

The agent must actively minimize hallucinations.

Expected behavior:

- retrieve context before generation
- prefer grounded examples over unsupported assumptions
- avoid fabricating schema elements
- stay conservative when context is insufficient

### 6. Analytical Pattern Recognition

The agent should recognize common analytical needs, such as:

- filtering by year, state, or system
- grouping by project, property, or client
- calculating savings, revenue, or revised values
- using joins to connect operational and client-level data

### 7. Explainability Support

When useful, the agent should be able to explain why a certain SQL pattern was chosen based on retrieved examples and business context.

This is especially valuable in enterprise environments, where transparency matters as much as correctness.

## Reviewer Guidance

When reviewing or improving this project, the AI assistant should focus on the following goals:

1. Improve grounding quality
2. Improve SQL reliability
3. Improve documentation clarity
4. Improve architecture modularity
5. Improve readiness for external review on GitHub

## Recommended Improvement Areas

Potential next skills or extensions for this project include:

- SQL syntax validation
- schema validation against trusted metadata
- execution checks against a safe sandbox
- better prompt templates
- richer example coverage
- user-facing interface improvements
- test coverage for retrieval and generation flows
