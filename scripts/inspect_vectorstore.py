"""Inspect contents of the FAISS vector store (vectorstore_enhanced).

Run from repository root: python scripts/inspect_vectorstore.py
"""
import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

ROOT_DIR = Path(__file__).resolve().parent.parent
os.chdir(ROOT_DIR)
load_dotenv(ROOT_DIR / ".env")

vectorstore = FAISS.load_local(
    str(ROOT_DIR / "vectorstore_enhanced"),
    OpenAIEmbeddings(),
    allow_dangerous_deserialization=True,
)
docs = vectorstore.docstore._dict

print(f"\n📦 Total documents in index: {len(docs)}\n")
for i, (key, doc) in enumerate(docs.items()):
    print(f"[{i + 1}] Key: {key}")
    print(f"Input: {doc.page_content[:200]}...")
    print(f"Query: {doc.metadata.get('query', '???')[:150]}...")
    print("----\n")
