# Comparison to LangGraph

LangGraph is a powerful library for building stateful, multi-actor applications. SafeAgent shares this goal but takes a different, more opinionated approach focused on **production-readiness from day one**.

## Philosophy

-   **LangGraph**: A flexible, low-level toolkit that requires you to build your own surrounding architecture for governance, reliability, and operational monitoring.
-   **SafeAgent**: A "batteries-included" framework providing a complete architecture with pre-integrated, production-grade components for these critical functions.

## Key Differences

| Feature | LangGraph | SafeAgent |
| :--- | :--- | :--- |
| **Governance** | Not a built-in feature. | **A core, defining feature.** Automatic, detailed audit logs for every action. |
| **Reliability** | Requires custom implementation. | **Built-in via declarative policies.** Caching, retries, and circuit breakers. |
| **Security** | Requires a custom solution. | **Built-in via declarative policies.** RBAC to restrict tool access. |
| **Tool Management** | Manual schema creation. | Automatic schema generation and **semantic search** to find relevant tools. |

## When to Choose Which?

-   **Choose LangGraph when** you need highly customized or unconventional graph structures, or prefer to build your own architecture from low-level primitives.
-   **Choose SafeAgent when** your priority is building **robust, observable, and secure** agents for production, and you want to accelerate development with pre-built solutions.