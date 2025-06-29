import time
import json
import logging
from .utils import get_request_id

_redis = None

class MemoryManager:
    """
    Minimal key-value memory store.
    Supports 'inmemory' or 'redis' backends and logs each read/write.
    Optionally, can summarize entire memory via an LLM.
    """

    def __init__(self, backend: str = "inmemory", redis_url: str = None):
        """
        backend: "inmemory" (default) or "redis".
        redis_url: e.g., "redis://localhost:6379" if backend="redis".
        """
        global _redis
        self.backend = backend

        if self.backend == "redis":
            if _redis is None:
                try:
                    import redis
                    _redis = redis
                except ModuleNotFoundError:
                    logging.error("Redis backend selected, but 'redis' package not found. Falling back to in-memory.")
                    self.backend = "inmemory" 
                    self.store = {}
                    return

            if _redis: 
                self.client = _redis.from_url(redis_url)
                try:
                    self.client.ping()
                    logging.info("Successfully connected to Redis.")
                except Exception as e:
                    logging.error(f"Failed to connect to Redis at {redis_url}: {e}. Falling back to in-memory.")
                    self.backend = "inmemory"
                    self.store = {}
            else:
                logging.error("Redis package not available. Falling back to in-memory.")
                self.backend = "inmemory"
                self.store = {}

        if self.backend == "inmemory":
            self.store = {} 

    def save(self, user_id: str, key: str, value: str) -> None:
        """Saves value under (user_id, key)."""
        if self.backend == "redis":
            self.client.hset(user_id, key, value)
        else:
            self.store.setdefault(user_id, {})[key] = value

        logging.info(json.dumps({
            "event": "memory_save",
            "user_id": user_id,
            "key": key,
            "request_id": get_request_id(),
            "timestamp": time.time(),
        }))

    def load(self, user_id: str, key: str) -> str:
        """Loads value for (user_id, key). Returns empty string if missing."""
        if self.backend == "redis":
            raw = self.client.hget(user_id, key)
            if isinstance(raw, bytes):
                value = raw.decode("utf-8")
            elif raw is None:
                value = ""
            else:
                value = str(raw)
        else:
            value = self.store.get(user_id, {}).get(key, "")

        logging.info(json.dumps({
            "event": "memory_load",
            "user_id": user_id,
            "key": key,
            "request_id": get_request_id(),
            "timestamp": time.time(),
        }))
        return value

    def summarize(self, user_id: str, embed_fn, llm_client, max_tokens: int = 256) -> str:
        """
        Reads all entries for user_id, concatenates them, and calls LLM to generate a summary.
        Stores the summary under key="summary" and returns it.
        """
        if self.backend == "redis":
            # Ensure proper handling if client failed to initialize or connection dropped
            try:
                all_vals = [v.decode("utf-8") for v in self.client.hvals(user_id)]
            except Exception as e:
                logging.warning(f"Could not retrieve from Redis during summarize: {e}. Using empty history.")
                all_vals = []
        else:
            all_vals = list(self.store.get(user_id, {}).values())

        full_text = "\n".join(all_vals)
        if not full_text:
            return ""

        summary_prompt = f"Summarize the following conversation history:\n\n{full_text}"
        resp = llm_client.generate(summary_prompt, max_tokens=max_tokens)
        summary = resp["text"]

        # Save summary back to memory
        self.save(user_id, "summary", summary)
        return summary