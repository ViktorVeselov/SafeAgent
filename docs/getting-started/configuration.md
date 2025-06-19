# Configuration

SafeAgent is configured primarily through environment variables, allowing you to easily switch settings without changing code. All configuration is managed by the `minillm.config.Config` dataclass.

## Core Configuration Variables

| Environment Variable | `Config` Attribute | Default Value | Description |
| -------------------- | ------------------ | ------------- | ----------- |
| `LLM_PROVIDER` | `llm_provider` | `"gemini"` | The LLM provider to use (e.g., 'openai'). |
| `GEMINI_API_KEY` | `api_key` | `""` | The API key for your chosen provider. |
| `LLM_MODEL` | `llm_model` | `"gemini-pro"` | The specific model to use for generation. |
| `TEMPLATE_DIR` | `template_dir` | `"templates"` | Directory for prompt templates. |
| `MEMORY_BACKEND` | `memory_backend` | `"redis"` | Backend for the MemoryManager (`redis` or `inmemory`). |
| `REDIS_URL` | `redis_url` | `"redis://localhost:6379"`| URL for your Redis server. |

## Tool Registry & Embedding Configuration

These variables allow you to customize the behavior of the semantic tool search.

| Environment Variable | `Config` Attribute | Default Value | Description |
| -------------------- | ------------------ | ------------- | ----------- |
| `EMBEDDING_DIMENSION` | `embedding_dimension` | `768` | The vector dimension of your embedding model (e.g., Gemini's is 768, OpenAI's is 1536). |
| `TOOL_SIMILARITY_METRIC` | `tool_similarity_metric` | `"cosine"` | The metric for vector search. Can be `cosine`, `l2`, or `dot_product`. |