# Core Concepts: Memory

The `MemoryManager` gives your agent a memory, allowing it to hold coherent, multi-turn conversations. It's a key-value store scoped to a `user_id`, ensuring conversation histories are kept separate. See the **Storage & Persistence** guide for details on backends.

## Example Usage

This script demonstrates how to save, load, and summarize conversation history.

```python
from safeagent import MemoryManager, LLMClient, Config, gemini_embed

cfg = Config()
mem_mgr = MemoryManager(backend="inmemory")
llm = LLMClient(api_key=cfg.api_key)
user_id = "test_user"

mem_mgr.save(user_id, "turn_1", "User: Hi, what is SafeAgent?")
mem_mgr.save(user_id, "turn_2", "Agent: It is a production-ready agent framework.")
print("Saved conversation history.")

summary = mem_mgr.summarize(user_id=user_id, llm_client=llm, embed_fn=lambda t: [])
print(f"\nGenerated Summary: {summary}")
```