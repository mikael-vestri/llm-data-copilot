# Scripts

| Script | Purpose |
|--------|--------|
| `create_embeddings_hybrid.py` | Build the FAISS vector index from `queries/examples.json`. Run once after clone (or when examples change). |
| `inspect_vectorstore.py` | Optional: list documents stored in the vector index. |

Run from the **repository root**:

```bash
python scripts/create_embeddings_hybrid.py
python scripts/inspect_vectorstore.py
```

The `legacy/` folder contains older or experimental scripts not required to run the main application.
