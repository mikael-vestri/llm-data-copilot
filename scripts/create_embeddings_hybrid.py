"""Build FAISS vector index from queries/examples.json for semantic retrieval.

Run from repository root: python scripts/create_embeddings_hybrid.py
"""
import json
import os
import re
from pathlib import Path

from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings

# Ensure we run from repo root (so paths like queries/examples.json resolve)
ROOT_DIR = Path(__file__).resolve().parent.parent
os.chdir(ROOT_DIR)
load_dotenv(ROOT_DIR / ".env")


def extract_tables_from_query(query):
    """Extract table names from SQL query."""
    table_pattern = r"(?:FROM|JOIN)\s+(?:main\.public\.)?(\w+)"
    tables = re.findall(table_pattern, query, re.IGNORECASE)
    return list(set(tables))


def extract_key_fields(query):
    """Extract main fields from SELECT clause."""
    select_pattern = r"SELECT\s+(.+?)\s+FROM"
    select_match = re.search(select_pattern, query, re.IGNORECASE | re.DOTALL)
    fields = []
    if select_match:
        select_clause = select_match.group(1)
        field_pattern = r"(\w+\.\w+|\w+)(?:\s+AS\s+\w+)?"
        fields = re.findall(field_pattern, select_clause)
    return fields[:10]


def get_query_type(query):
    """Classify query type for richer context."""
    query_lower = query.lower()
    if "group by" in query_lower and "count" in query_lower:
        return "Aggregation/Count Query"
    if "union" in query_lower:
        return "Union Query"
    if "with" in query_lower:
        return "CTE Query"
    if "join" in query_lower:
        return "Join Query"
    return "Select Query"


def create_enhanced_text_representation(example):
    """Build text representation for embedding (question + description + tables + type)."""
    query = example["query"]
    input_question = example["input"]
    description = example.get("metadata", {}).get("description", "")
    tables = extract_tables_from_query(query)
    fields = extract_key_fields(query)
    return f"""
Question: {input_question}

Description: {description}

Related Tables: {', '.join(tables)}

Key Fields: {', '.join(fields[:5])}

Query Type: {get_query_type(query)}
""".strip()


def vectorize_enhanced():
    examples_path = ROOT_DIR / "queries" / "examples.json"
    with open(examples_path, "r", encoding="utf-8") as f:
        examples = json.load(f)

    docs = []
    for ex in examples:
        content = create_enhanced_text_representation(ex)
        doc = Document(
            page_content=content,
            metadata={
                "original_input": ex["input"],
                "query": ex["query"],
                "description": ex.get("metadata", {}).get("description", ""),
                "query_name": ex.get("metadata", {}).get("query_name", ""),
            },
        )
        docs.append(doc)

    embedding_model = OpenAIEmbeddings()
    db = FAISS.from_documents(docs, embedding_model)
    out_dir = ROOT_DIR / "vectorstore_enhanced"
    db.save_local(str(out_dir))

    print(f"✅ Created embeddings for {len(docs)} examples")
    print(f"✅ Saved to {out_dir}")


if __name__ == "__main__":
    vectorize_enhanced()
