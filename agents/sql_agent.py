import os
from dotenv import load_dotenv
from langchain.agents import Tool, initialize_agent
from langchain.agents.agent_types import AgentType
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

# Load environment variables
load_dotenv()

# ----------------------------
# Function: Retrieve similar examples from vectorstore
# ----------------------------
def retrieve_examples(user_question: str, k: int = 3):
    vectorstore = FAISS.load_local("vectorstore_enhanced", OpenAIEmbeddings(), allow_dangerous_deserialization=True)
    docs = vectorstore.similarity_search_with_score(user_question, k=k)

    examples = [
        {
            "question": doc.metadata.get("original_input", doc.page_content),
            "query": doc.metadata.get("query", ""),
            "score": score
        }
        for doc, score in docs
    ]
    return examples

# ----------------------------
# Function: Generate SQL query based on similar examples
# ----------------------------
def generate_sql_query(user_question: str):
    examples = retrieve_examples(user_question)

    examples_text = "\n\n".join([
        f"Question: {ex['question']}\nSQL Query:\n{ex['query']}"
        for ex in examples
        if ex['score'] < 1.5
    ]) or "No specific examples available. Generate based on general SQL knowledge."

    prompt = PromptTemplate.from_template("""
You are an expert SQL developer working with a PostgreSQL database containing business data about properties, clients, tax calculations, and reporting.

DATABASE CONTEXT:
- Main tables: properties, clients, property_values (schema for property tax / business analytics)
- Common fields: tax_year, client_id, property_id, taxable_value, tax_rate, tax_due
- Use soft-delete filters (e.g. deleted_at IS NULL) when the schema supports it

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
    
    chain = LLMChain(
        llm=ChatOpenAI(model="gpt-4", temperature=0.2),
        prompt=prompt
    )

    response = chain.invoke({"examples": examples_text, "question": user_question})
    return response["text"]


# Function to validate if the query is safe using LLM
def is_safe_query_llm(query: str) -> bool:
    prompt = f"""
    Analyze the following SQL query and determine if it is safe for execution.
    
    A query is considered SAFE if:
    - It is for READ-ONLY operations (SELECT, WITH, etc.)
    - It does NOT modify data (INSERT, UPDATE, DELETE, DROP, CREATE, etc.)
    - It does NOT alter database structure
    - It can have comments, CTEs, subqueries, UNIONs, etc.
    
    Query to analyze:
    {query}
    
    Respond only with "SAFE" or "DANGEROUS".
    """
    
    llm = ChatOpenAI(model="gpt-4", temperature=0)
    response = llm.invoke(prompt)
    return "SAFE" in str(response.content).upper()


# ----------------------------
# Tool definitions for agent
# ----------------------------
tools = [
    Tool(
        name="RetrieveQueryTool",
        func=retrieve_examples,
        description="Use this to retrieve example SQL queries similar to the user's input from the vectorstore."
    ),
    Tool(
        name="GenerateSQLTool",
        func=generate_sql_query,
        description="Use this to generate a new SQL query based on the user's question using the retrieved examples."
    )
]

# ----------------------------
# Initialize the agent
# ----------------------------
llm = ChatOpenAI(model="gpt-4", temperature=0.2)

agent_executor = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# ----------------------------
# CLI interaction mode
# ----------------------------
if __name__ == "__main__":
    print("🧠 LLM Data Copilot Agent is ready.")
    while True:
        question = input("\n📌 Enter your data question (e.g., 'What are the tax savings for 2025?')\n>> ").strip()
        if question.lower() in ["exit", "quit"]:
            break
        result = agent_executor.invoke({"input": question})
        print("\n🎯 Final Answer:\n", result)
        
        # Security validation of the generated query
        print("\n🔍 Debug - Result structure:")
        print(f"Result type: {type(result)}")
        print(f"Available keys: {list(result.keys()) if isinstance(result, dict) else 'N/A'}")
        
        if "output" in result and result["output"]:
            query_output = result["output"]
            print(f"Output content: {query_output[:200]}...")  # First 200 characters
            print(f"Query starts with SELECT? {query_output.strip().lower().startswith('select')}")
            
            if is_safe_query_llm(query_output):
                print("\n✅ Query validated as safe for database execution.")
            else:
                print("\n⚠️  Query blocked for security! Only read queries are allowed.")
        else:
            print("❌ Could not find query in the result.")
