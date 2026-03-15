# query_agent.py

from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_core.documents import Document
from dotenv import load_dotenv
import os


# Load OpenAI key
load_dotenv()
openai_key = os.getenv("OPENAI_API_KEY")
if not openai_key:
    raise ValueError("OPENAI_API_KEY not found in .env file")

# Load the saved vector store
vectorstore = FAISS.load_local("vectorstore", OpenAIEmbeddings(), allow_dangerous_deserialization=True)

# Ask the user for a question in natural language
user_question = input("What would you like to do with your data? Describe it in plain English:\n> ")

# Retrieve the most relevant document (top 1 match)
retrieved_docs = vectorstore.similarity_search(user_question, k=1)

# Handle the result
if retrieved_docs:
    doc: Document = retrieved_docs[0]
    print("\n✅ Closest SQL query found:")
    print("--------------------------------------------------")
    print(doc.page_content.strip())
    print("\n📄 Description:")
    print(doc.metadata.get("description", "No description available."))
    print("🔧 Source system:", doc.metadata.get("system", "Unknown"))
else:
    print("❌ Sorry, no relevant SQL query was found.")
