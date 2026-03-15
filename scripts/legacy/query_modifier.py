import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# Load environment variables
load_dotenv()

def modify_sql_query(original_query: str, modification_request: str):
    """
    Modifica uma query SQL existente baseada em uma solicitação de modificação
    """
    
    prompt = PromptTemplate.from_template("""
Você é um especialista em SQL PostgreSQL. Analise a query SQL fornecida e faça as modificações solicitadas.

QUERY ORIGINAL:
{original_query}

SOLICITAÇÃO DE MODIFICAÇÃO:
{modification_request}

INSTRUÇÕES:
1. Mantenha toda a estrutura e lógica da query original
2. Adicione apenas as colunas solicitadas (office e consultant)
3. Certifique-se de que as novas colunas sejam incluídas nos SELECTs e GROUP BYs apropriados
4. Mantenha todos os JOINs e condições WHERE existentes
5. Retorne apenas a query SQL modificada, sem explicações adicionais
6. Utiliza seus conhecimentos da vectorstore para fazer os joins necessários para trazer as informações requeridas

QUERY MODIFICADA:""")
    
    chain = LLMChain(
        llm=ChatOpenAI(model="gpt-4", temperature=0.1),
        prompt=prompt
    )
    
    response = chain.invoke({
        "original_query": original_query,
        "modification_request": modification_request
    })
    
    return response["text"].strip()

def main():
    print("🔧 SQL Query Modifier")
    print("=" * 50)
    
    # Ler a query original do arquivo
    with open("queries/tax_bill_tracker.sql", "r", encoding="utf-8") as f:
        original_query = f.read()
    
    print("📋 Query original carregada do arquivo tax_bill_tracker.sql")
    print("🎯 Modificação solicitada: Adicionar colunas 'office' e 'consultant'")
    print("\n" + "="*50)
    
    # Fazer a modificação
    modified_query = modify_sql_query(
        original_query, 
        "Adicione as colunas 'office' e 'consultant' na query. Estas colunas devem ser incluídas nos SELECTs e GROUP BYs apropriados."
    )
    
    print("✅ Query modificada:")
    print("=" * 50)
    print(modified_query)
    print("=" * 50)
    
    # Salvar a query modificada
    output_file = "queries/tax_bill_tracker_modified.sql"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(modified_query)
    
    print(f"\n💾 Query salva em: {output_file}")

if __name__ == "__main__":
    main() 