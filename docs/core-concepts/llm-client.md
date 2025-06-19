# Core Concepts: LLM Client

The `LLMClient` is a standardized interface for interacting with different Large Language Model providers.

## Example Usage
```python
from safeagent import LLMClient, Config

llm = LLMClient(api_key=Config().api_key)
response = llm.generate("Explain 'prompt engineering' in one sentence.")
print(f"Response: {response.get('text')}")
```