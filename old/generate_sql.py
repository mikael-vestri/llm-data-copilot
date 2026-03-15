import os
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import LLMChain

# Load env vars
load_dotenv()

# Load vectorstore
vectorstore = FAISS.load_local("vectorstore", OpenAIEmbeddings(), allow_dangerous_deserialization=True)

# Get question
user_question = input("What do you want to ask? (e.g., 'What are the tax savings for Texas in 2025?')\n>> ")

# Search similar examples
docs_with_scores = vectorstore.similarity_search_with_score(user_question, k=3)
score_threshold = 0.75

print("\n🔍 Similarity scores for retrieved examples:\n")
for i, (doc, score) in enumerate(docs_with_scores):
    print(f"[{i+1}] Score: {score:.4f}")
    print(f"Description: {doc.metadata.get('description', '(no description)')}")
    print(f"Question: {doc.page_content[:150]}...\n")

# Filtra os melhores matches
good_matches = [doc for doc, score in docs_with_scores if score >= score_threshold]

# Monta os exemplos
if good_matches:
    print("\n✅ Using similar examples found in the vectorstore...\n")
    examples = "\n\n".join([
        f"Question: {doc.page_content}\nQuery:\n{doc.metadata['query']}"
        for doc in good_matches
    ])
else:
    print("\n⚠️ No sufficiently similar examples found. Generating SQL from scratch...\n")
    examples = "No examples available."

# Template do prompt
prompt = PromptTemplate.from_template("""You are an AI SQL assistant working with a PostgreSQL database. Based on the examples below, generate a new SQL query that best answers the user's question.

Examples:
{examples}

---

User Question: {question}

Your SQL Query:""")

# Define LLM
llm = ChatOpenAI(model="gpt-4", temperature=0.2)

# Executa o LLMChain
chain = LLMChain(llm=llm, prompt=prompt)
response = chain.invoke({"examples": examples, "question": user_question})

# Exibe resultado
print("\n✅ Suggested SQL Query:\n")
print(response['text'])
