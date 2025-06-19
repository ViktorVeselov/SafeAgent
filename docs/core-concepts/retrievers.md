# Core Concepts: Retrievers

Retrievers are components responsible for fetching external information to augment an agent's knowledge (Retrieval-Augmented Generation, or RAG).

## `VectorRetriever`

This retriever uses a `faiss` vector index to find documents that are semantically similar to a query.

### Example Usage

```python
import numpy as np
import os
import json
from safeagent import VectorRetriever, gemini_embed, Config

cfg = Config()
index_path = "my_test_index.idx"
if os.path.exists(index_path): os.remove(index_path)

embed_func = lambda text: gemini_embed(text, api_key=cfg.api_key)
retriever = VectorRetriever(index_path=index_path, embed_model_fn=embed_func)

print("Indexing documents...")
docs = ["The sky is blue.", "The capital of France is Paris."]
embeddings = [embed_func(doc) for doc in docs]
metadata = [{"id": i} for i in range(len(docs))]
retriever.index(np.array(embeddings, dtype=np.float32), metadata)

results = retriever.query("What color is the sky?", top_k=1)
print(f"\nQuery Results: {json.dumps(results, indent=2)}")

if os.path.exists(index_path): os.remove(index_path)
```