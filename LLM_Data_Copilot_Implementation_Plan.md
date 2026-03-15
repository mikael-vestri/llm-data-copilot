# Python Implementation Plan - LLM Data Copilot

## Overview

Implementation plan for the **LLM Data Copilot** application, following a modular architecture focused on Python. This tool enables users to connect to their PostgreSQL databases, automatically extract the database schema, and interact with the data using natural language queries via LLM agents. The system will leverage existing scripts for query preprocessing, embedding generation, and vector store management.

## Steps

### Step 1: Project Setup & Structure

- [x] 1.1 Set up Python virtual environment (venv)
- [x] 1.2 Organize project folders:
  - `/agents` - LLM agents (LangChain-based)
  - `/app` - Core app logic
  - `/vectorstore` - FAISS vector store management
  - `/queries` - Example SQL queries (for training/embedding)
  - `/data_dictionary` - Extracted schemas
  - `/ui` - Streamlit interface
- [x] 1.3 Install core dependencies:
  - `openai`
  - `langchain`
  - `faiss-cpu`
  - `psycopg2` (PostgreSQL client)
  - `streamlit`
  - `tiktoken`, `dotenv`, etc.
- [x] 1.4 Initialize Git repository

### Step 2: Database Connection & Schema Extraction

- [ ] 2.1 Build connection input UI in Streamlit (user inputs PostgreSQL connection string)
- [ ] 2.2 Create database connection module
- [ ] 2.3 Implement schema extraction logic:
  - Connect to DB
  - Retrieve tables, columns, data types
  - Save schema as JSON or text
- [ ] 2.4 Display extracted schema in Streamlit

### Step 3: Query Embedding & Vector Store Setup

- [x] 3.1 Reuse existing preprocessing scripts:
  - Clean & normalize queries
  - Generate embeddings using OpenAI
- [x] 3.2 Initialize FAISS vector store
- [ ] 3.3 Ingest preprocessed queries into vector store
- [ ] 3.4 Save vector store locally
- [ ] 3.5 Load vector store for retrieval during app runtime

### Step 4: Agent Design & Use Cases

- [x] 4.1 Reuse existing agent tools:
  - RetrieveQueryTool
  - GenerateSQLTool
  - (Optional) ValidateSQLTool, ExplainSQLTool, LogTool
- [ ] 4.2 Implement agent for answering natural language questions:
  - Input: user question + extracted schema
  - Process: Use vector store & LLM to generate SQL
  - Output: SQL query
- [ ] 4.3 Implement agent to execute SQL queries on connected DB
- [ ] 4.4 Implement error handling for query generation & execution

### Step 5: Streamlit Interface Integration

- [x] 5.1 Basic interface (Streamlit) already set up
- [ ] 5.2 Integrate database connection flow
- [ ] 5.3 Integrate schema display
- [ ] 5.4 Integrate query generation & execution agents
- [ ] 5.5 Display query results in table format
- [ ] 5.6 Add loading states, error messages, and success indicators

### Step 6: Data Visualization (Future Feature)

- [ ] 6.1 Add option to visualize query results as charts (e.g., bar, line, pie)
- [ ] 6.2 Integrate with Streamlit's built-in chart components

### Step 7: Testing & Validation

- [ ] 7.1 Create unit tests for core modules (using pytest)
- [ ] 7.2 Test schema extraction module with multiple DBs
- [ ] 7.3 Test query generation agent with various prompts
- [ ] 7.4 End-to-end tests for entire workflow

### Step 8: Documentation & Finalization

- [ ] 8.1 Document project structure and architecture
- [ ] 8.2 Create a detailed README with usage instructions
- [ ] 8.3 Write developer guidelines for extending or customizing the tool
- [ ] 8.4 Final code cleanup and optimization

## Architecture Principles

- Modular design with clear separation of concerns:
  - **Agents Layer:** LLM-powered agents (LangChain)
  - **Application Layer:** DB connection, schema extraction, query execution
  - **Vector Store Layer:** Embedding generation, FAISS vector storage
  - **Interface Layer:** Streamlit UI
- Use dependency injection and environment variables (dotenv)
- Reuse existing scripts and modules wherever possible
- Keep core components loosely coupled for easier testing and maintenance

## Technology Stack

- **Python** (>=3.10)
- **OpenAI API** for LLM tasks
- **FAISS** for vector store
- **PostgreSQL** for database
- **Streamlit** for web interface
- **LangChain** for agent framework
- **pytest** for testing

---

This plan is designed to allow gradual, step-by-step progress with easy tracking and task completion marking.
