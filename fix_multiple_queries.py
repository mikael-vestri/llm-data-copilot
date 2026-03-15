import re
import json

# Caminho do arquivo problemático
file_path = "queries/examples.json"

# Abre o arquivo bruto e tenta limpar os caracteres de controle
with open(file_path, "r", encoding="utf-8") as f:
    raw_content = f.read()

# Substitui todos os caracteres de controle NÃO ESCAPADOS por espaços
cleaned_content = re.sub(r'(?<!\\)[\n\r\t]', ' ', raw_content)

# Agora tenta carregar como JSON normalmente
try:
    examples = json.loads(cleaned_content)
except json.JSONDecodeError as e:
    print("💥 Ainda deu pau no JSON:", e)
    exit()

# Salva limpo
with open(file_path, "w", encoding="utf-8") as f:
    json.dump(examples, f, indent=2)

print("✅ JSON limpo e salvo com sucesso!")
