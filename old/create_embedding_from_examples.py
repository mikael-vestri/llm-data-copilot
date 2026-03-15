import json
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
from dotenv import load_dotenv

load_dotenv()

# Carrega os exemplos
with open("queries/examples.json", "r", encoding="utf-8") as f:
    examples = json.load(f)

# Cria os documentos com input como page_content e query na metadata
docs = [
    Document(
        page_content=ex["input"],
        metadata={
            "query": ex["query"],
            "description": ex.get("metadata", {}).get("description", "")
        }
    )
    for ex in examples
]

# Gera os embeddings
embedding_model = OpenAIEmbeddings()
db = FAISS.from_documents(docs, embedding_model)
db.save_local("vectorstore")

print("✅ Embeddings generated from inputs and saved to ./vectorstore")
