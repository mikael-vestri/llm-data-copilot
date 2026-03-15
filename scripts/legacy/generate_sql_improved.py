import os
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import LLMChain

# Load env vars
load_dotenv()

def expand_user_question(question):
    """Expand the user's question for better matching"""
    expanded = f"""
    Question: {question}
    
    Context: This is a question about database analysis, reporting, tax calculations, 
    property management, client data, or business intelligence.
    
    Related concepts: clients, properties, tax values, reports, calculations, jurisdictions
    """.strip()
    
    return expanded

def load_vectorstore(enhanced=True):
    """Load the vectorstore (standard or enhanced)"""
    store_name = "vectorstore_enhanced" if enhanced else "vectorstore"
    
    try:
        vectorstore = FAISS.load_local(
            store_name, 
            OpenAIEmbeddings(), 
            allow_dangerous_deserialization=True
        )
        print(f"✅ Loaded {store_name}")
        return vectorstore
    except Exception as e:
        print(f"❌ Error loading {store_name}: {e}")
        return None

def search_with_multiple_strategies(vectorstore, question, k=3):
    """Try multiple search strategies"""
    
    results = []
    
    # Strategy 1: Original question
    docs1 = vectorstore.similarity_search_with_score(question, k=k)
    results.extend([(doc, score, "original") for doc, score in docs1])
    
    # Strategy 2: Expanded question
    expanded_question = expand_user_question(question)
    docs2 = vectorstore.similarity_search_with_score(expanded_question, k=k)
    results.extend([(doc, score, "expanded") for doc, score in docs2])
    
    # Remove duplicates based on query_name
    seen = set()
    unique_results = []
    
    for doc, score, strategy in results:
        query_name = doc.metadata.get('query_name', 'unknown')
        if query_name not in seen:
            seen.add(query_name)
            unique_results.append((doc, score, strategy))
    
    # Sort by score (lower is better for L2)
    unique_results.sort(key=lambda x: x[1])
    
    return unique_results[:k]

def main():
    # Load enhanced vectorstore
    vectorstore = load_vectorstore(enhanced=True)
    if not vectorstore:
        print("⚠️ Trying standard vectorstore...")
        vectorstore = load_vectorstore(enhanced=False)
        if not vectorstore:
            print("❌ No vectorstore found. Run create_embedding_hybrid.py first")
            return

    # Get question
    user_question = input("\nWhat do you want to ask? (e.g., 'What are the tax savings for 2025?')\n>> ")

    # Search with multiple strategies
    results = search_with_multiple_strategies(vectorstore, user_question, k=3)
    
    print(f"\n🔍 Found {len(results)} relevant examples:\n")
    
    good_matches = []
    for i, (doc, score, strategy) in enumerate(results):
        print(f"[{i+1}] Score: {score:.4f} (Strategy: {strategy})")
        print(f"Original Question: {doc.metadata.get('original_input', 'N/A')}")
        print(f"Description: {doc.metadata.get('description', 'N/A')}")
        print(f"Query Name: {doc.metadata.get('query_name', 'N/A')}")
        print("-" * 50)
        
        # Consider good matches if score < 1.5 (adjust as needed)
        if score < 1.5:
            good_matches.append(doc)

    # Build examples for prompt
    if good_matches:
        print(f"\n✅ Using {len(good_matches)} similar examples...\n")
        examples = "\n\n".join([
            f"Question: {doc.metadata['original_input']}\n"
            f"Description: {doc.metadata['description']}\n"
            f"SQL Query:\n{doc.metadata['query']}"
            for doc in good_matches
        ])
    else:
        print("\n⚠️ No sufficiently similar examples found. Generating from scratch...\n")
        examples = "No specific examples available. Generate based on general SQL knowledge."

        # Improved prompt template
    prompt = PromptTemplate.from_template("""You are an expert SQL developer working with a PostgreSQL database containing business data about properties, clients, tax calculations, and reporting.

DATABASE CONTEXT:
- Main tables: nova_property, nova_client, tpt_assessoraccounts, nova_collector_account_number
- Common fields: tax_year, client_id, property_id, taxable_value, tax_rate
- Systems: Nova and TPT (two different property management systems)

EXAMPLES FROM SIMILAR QUERIES:
{examples}

---

USER QUESTION: {question}

INSTRUCTIONS:
1. Analyze the user's question carefully
2. Use the examples above as reference for table names, joins, and business logic
3. Generate a complete, runnable PostgreSQL query
4. Include appropriate filters (deleted_at IS NULL, tax_year conditions)
5. Use meaningful column aliases
6. Add comments for complex logic

YOUR SQL QUERY:""")

    # Define LLM
    llm = ChatOpenAI(model="gpt-4", temperature=0.1)

    # Execute the LLMChain
    chain = LLMChain(llm=llm, prompt=prompt)
    response = chain.invoke({"examples": examples, "question": user_question})

    # Display result
    print("\n" + "="*60)
    print("🚀 GENERATED SQL QUERY:")
    print("="*60)
    print(response['text'])
    print("="*60)

if __name__ == "__main__":
    main()