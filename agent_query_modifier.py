import os
from dotenv import load_dotenv
from langchain.agents import Tool, initialize_agent
from langchain.agents.agent_types import AgentType
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

# Load environment variables
load_dotenv()

def retrieve_examples(user_question: str, k: int = 5):
    """Retrieve similar examples from vectorstore"""
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

def generate_sql_with_context(original_query: str, modification_request: str):
    """Generate SQL modification using agent with vectorstore context"""
    
    # Primeiro, buscar exemplos relacionados
    search_query = "office consultant nova_client nova_office nova_consultant"
    examples = retrieve_examples(search_query)
    
    # Filtrar exemplos relevantes
    relevant_examples = [
        ex for ex in examples 
        if ex['score'] < 2.0 and ('office' in ex['query'].lower() or 'consultant' in ex['query'].lower())
    ]
    
    examples_text = "\n\n".join([
        f"Question: {ex['question']}\nSQL Query:\n{ex['query']}"
        for ex in relevant_examples
    ]) if relevant_examples else "No specific examples found for office/consultant joins."
    
    # Criar prompt com contexto dos exemplos
    prompt = f"""
Você é um especialista em SQL PostgreSQL. Analise a query SQL fornecida e faça as modificações solicitadas.

EXEMPLOS DE QUERIES SIMILARES DA BASE DE DADOS:
{examples_text}

QUERY ORIGINAL:
{original_query}

SOLICITAÇÃO DE MODIFICAÇÃO:
{modification_request}

INSTRUÇÕES:
1. Use os exemplos acima como referência para os nomes corretos das tabelas e relacionamentos
2. Mantenha toda a estrutura e lógica da query original
3. Adicione as colunas 'office' e 'consultant' nos SELECTs apropriados
4. Certifique-se de que as novas colunas sejam incluídas nos GROUP BYs onde necessário
5. Mantenha todos os JOINs e condições WHERE existentes
6. Use os exemplos para determinar os JOINs corretos para office e consultant
7. Retorne apenas a query SQL modificada, sem explicações adicionais

QUERY MODIFICADA:"""
    
    llm = ChatOpenAI(model="gpt-4", temperature=0.1)
    response = llm.invoke(prompt)
    return response.content.strip()

def main():
    print("🔧 SQL Query Modifier com Agente")
    print("=" * 60)
    
    # Ler a query original
    with open("queries/tax_bill_tracker.sql", "r", encoding="utf-8") as f:
        original_query = f.read()
    
    print("📋 Query original carregada")
    print("🔍 Buscando exemplos relacionados na vectorstore...")
    
    # Fazer a modificação usando o agente
    modification_request = "Adicione as colunas 'office' e 'consultant' na query. Use os exemplos da vectorstore para determinar os JOINs corretos."
    
    modified_query = generate_sql_with_context(original_query, modification_request)
    
    print("✅ Query modificada com contexto da vectorstore:")
    print("=" * 60)
    print(modified_query)
    print("=" * 60)
    
    # Salvar a query modificada
    output_file = "queries/tax_bill_tracker_with_agent.sql"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(modified_query)
    
    print(f"\n💾 Query salva em: {output_file}")

if __name__ == "__main__":
    main() 