# tentando consertar o create embeddings "Normal"
import json
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
from dotenv import load_dotenv
import re

load_dotenv()

def extract_tables_from_query(query):
    """Extrai nomes de tabelas da query SQL"""
    # Regex para encontrar FROM e JOIN
    table_pattern = r'(?:FROM|JOIN)\s+(?:main\.public\.)?(\w+)'
    tables = re.findall(table_pattern, query, re.IGNORECASE)
    return list(set(tables))  # Remove duplicatas

def extract_key_fields(query):
    """Extrai campos principais da query (SELECT, WHERE, GROUP BY)"""
    # Campos no SELECT (simplificado)
    select_pattern = r'SELECT\s+(.+?)\s+FROM'
    select_match = re.search(select_pattern, query, re.IGNORECASE | re.DOTALL)
    
    fields = []
    if select_match:
        select_clause = select_match.group(1)
        # Remove funções e pega só nomes de campos
        field_pattern = r'(\w+\.\w+|\w+)(?:\s+AS\s+\w+)?'
        fields = re.findall(field_pattern, select_clause)
    
    return fields[:10]  # Limita a 10 campos principais

def create_enhanced_text_representation(example):
    """Cria representação mais rica combinando pergunta + contexto da query"""
    
    query = example["query"]
    input_question = example["input"]
    description = example.get("metadata", {}).get("description", "")
    
    # Extrai contexto da query
    tables = extract_tables_from_query(query)
    fields = extract_key_fields(query)
    
    # Monta texto combinado
    enhanced_text = f"""
    Question: {input_question}
    
    Description: {description}
    
    Related Tables: {', '.join(tables)}
    
    Key Fields: {', '.join(fields[:5])}
    
    Query Type: {get_query_type(query)}
    """.strip()
    
    return enhanced_text

def get_query_type(query):
    """Identifica tipo da query"""
    query_lower = query.lower()
    
    if 'group by' in query_lower and 'count' in query_lower:
        return "Aggregation/Count Query"
    elif 'union' in query_lower:
        return "Union Query"
    elif 'with' in query_lower:
        return "CTE Query"
    elif 'join' in query_lower:
        return "Join Query"
    else:
        return "Select Query"

def vectorize_enhanced():
    # Carrega os exemplos
    with open("queries/examples.json", "r", encoding="utf-8") as f:
        examples = json.load(f)

    # Cria documentos com representação melhorada
    docs = []
    for ex in examples:
        enhanced_content = create_enhanced_text_representation(ex)
        
        doc = Document(
            page_content=enhanced_content,  # Texto rico
            metadata={
                "original_input": ex["input"],
                "query": ex["query"],
                "description": ex.get("metadata", {}).get("description", ""),
                "query_name": ex.get("metadata", {}).get("query_name", "")
            }
        )
        docs.append(doc)

    # Gera embeddings
    embedding_model = OpenAIEmbeddings()
    db = FAISS.from_documents(docs, embedding_model)
    db.save_local("vectorstore_enhanced")

    print(f"✅ Enhanced embeddings created for {len(docs)} examples")
    print("✅ Saved to ./vectorstore_enhanced")

if __name__ == "__main__":
    vectorize_enhanced()