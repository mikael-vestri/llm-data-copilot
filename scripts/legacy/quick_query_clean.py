import json

with open("queries/examples.json", "r", encoding="utf-8") as f:
    data = json.load(f)

for ex in data:
    if "query" in ex:
        ex["query"] = ex["query"].replace("\u00a0", " ")

with open("queries/examples.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)