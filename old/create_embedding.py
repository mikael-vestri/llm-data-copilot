from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.schema import Document
from dotenv import load_dotenv
import os


# Load OpenAI key
load_dotenv()
openai_key = os.getenv("OPENAI_API_KEY")
if not openai_key:
    raise ValueError("OPENAI_API_KEY not found in .env file")

# Read query from .sql file
with open("queries/nova_tax_savings_2025.sql", "r", encoding="utf-8") as f:
    sql_query = f.read()

# Metadata for this embedding
metadata = {
    "id": "nova_tax_savings_2025",
    "description": "Calculates tax and savings values for properties from the Nova system for tax year 2025, including revised values, tax entity rates, and joins with CDP data. Applies filters to exclude deleted records.",
    "system": "nova",
    "tables_used": [
        "nova_property", "nova_client", "nova_client_property", "nova_property_value",
        "nova_collector_account_number", "nova_property_jurisdiction", "nova_tax_entity_rate",
        "cdp.clients", "cdp.client_channel_associations"
    ],
    "key_filters": [
        "WHERE deleted_at IS NULL (on multiple tables)",
        "tax_year = 2025 OR IS NULL"
    ],
    "fields_calculated": [
        "TaxSavings", "taxdue", "initialTax", "revisedTax"
    ],
    "tags": ["tax savings", "property", "nova", "CTE", "complex join"]
}

# Create and store embedding
doc = Document(page_content=sql_query, metadata=metadata)
embedding_model = OpenAIEmbeddings()
db = FAISS.from_documents([doc], embedding_model)
db.save_local("vectorstore")

print("✅ Embedding created and saved to ./vectorstore")
