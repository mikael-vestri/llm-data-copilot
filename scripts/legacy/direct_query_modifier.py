import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# Load environment variables
load_dotenv()

def modify_tax_bill_tracker_query():
    """
    Modifica a query tax_bill_tracker.sql para adicionar as colunas office e consultant
    """
    
    # Ler a query original
    with open("queries/tax_bill_tracker.sql", "r", encoding="utf-8") as f:
        original_query = f.read()
    
    prompt = PromptTemplate.from_template("""
Você é um especialista em SQL PostgreSQL. Analise a query SQL fornecida e adicione as colunas 'office' e 'consultant'.

QUERY ORIGINAL:
{original_query}

INSTRUÇÕES:
1. Mantenha toda a estrutura e lógica da query original
2. Adicione as colunas 'office' e 'consultant' nos SELECTs apropriados
3. Certifique-se de que as novas colunas sejam incluídas nos GROUP BYs onde necessário
4. Mantenha todos os JOINs e condições WHERE existentes
5. Use seus conhecimentos da vectorstore para fazer os JOINs necessários para trazer as informações de office e consultant
6. Retorne apenas a query SQL modificada, sem explicações adicionais

QUERY MODIFICADA:""")
    
    chain = LLMChain(
        llm=ChatOpenAI(model="gpt-4", temperature=0.1),
        prompt=prompt
    )
    
    response = chain.invoke({"original_query": original_query})
    return response["text"].strip()

def main():
    print("🔧 Modificando query tax_bill_tracker.sql")
    print("=" * 60)
    
    try:
        # Fazer a modificação
        modified_query = modify_tax_bill_tracker_query()
        
        print("✅ Query modificada com sucesso!")
        print("=" * 60)
        print(modified_query)
        print("=" * 60)
        
        # Salvar a query modificada
        output_file = "queries/tax_bill_tracker_with_office_consultant.sql"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(modified_query)
        
        print(f"\n💾 Query salva em: {output_file}")
        
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    main() 