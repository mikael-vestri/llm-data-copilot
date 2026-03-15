from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

# Load env vars
load_dotenv()
# Carrega a vectorstore
vectorstore = FAISS.load_local("vectorstore", OpenAIEmbeddings(), allow_dangerous_deserialization=True)

# Pega todos os documentos
docs = vectorstore.docstore._dict  # <- acesso direto ao conteúdo

print(f"\n📦 Total de documentos vetorizados: {len(docs)}\n")

for i, (key, doc) in enumerate(docs.items()):
    print(f"[{i+1}]")
    print(f"Key: {key}")
    print(f"Input: {doc.page_content}")
    print(f"Query:\n{doc.metadata.get('query', '???')}")
    print("----\n")
