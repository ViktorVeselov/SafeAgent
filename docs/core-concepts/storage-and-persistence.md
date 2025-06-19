# Core Concepts: Storage & Persistence

A production-ready framework needs to manage state. SafeAgent provides clear, configurable options for storing two key types of data: **Tool Cache** and **Conversation Memory**.

## Tool Cache (`ToolRegistry`)

The `ToolRegistry` uses caching to improve performance and reduce costs for tools.

-   **Where is it stored?** By default, the cache is stored **in-memory** in a Python dictionary (`self._cache`).
-   **Why?** This provides a significant speed-up for repeated calls to the same tool with the same arguments *within a single, continuous process run*. It's designed to be simple and fast.
-   **Is it persistent?** No. The in-memory cache is ephemeral and will be cleared when your application restarts.
-   **Production Note:** For a cache that persists across restarts and can be shared by multiple agent processes, you would implement a custom `ToolRegistry` that uses a shared backend like Redis. The default implementation prioritizes simplicity and single-process performance.

## Conversation Memory (`MemoryManager`)

The `MemoryManager` is designed for long-term storage of conversation histories and requires a more robust solution.

-   **Where is it stored?** The `MemoryManager` supports two backends, configurable via the `MEMORY_BACKEND` environment variable:
    1.  `inmemory`: A simple Python dictionary.
    2.  `redis`: A persistent, external Redis database.
-   **Why use Redis in production?**
    * **Persistence**: Redis stores data on disk. If your agent application restarts, it won't lose its memory of past conversations.
    * **Scalability**: You can run multiple instances of your agent (e.g., in different containers or on different machines) that all connect to the *same* Redis instance. This allows them to share conversation state, which is impossible with an in-memory dictionary.
-   **How to configure it:** Set the `MEMORY_BACKEND` and `REDIS_URL` environment variables as described in the [Configuration Guide](../getting-started/configuration.md).

By providing these distinct, configurable storage options, SafeAgent allows you to choose the right trade-off between simplicity for local development (`inmemory`) and the persistence and scalability required for production (`redis`).