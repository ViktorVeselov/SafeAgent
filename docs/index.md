# Welcome to SafeAgent

**SafeAgent** is a minimal, flexible framework for orchestrating **production-ready LLM agents**. It provides pluggable components for retrieval, memory, and orchestration with enterprise-grade governance, reliability, and observability built-in from day one.

While many tools can help you build a prototype, SafeAgent is designed to build systems you can confidently run in production.

## The SafeAgent Advantage: Beyond the Prototype

-   **Unparalleled Governance & Observability**: Every action—from LLM calls to tool executions—is automatically audited with detailed logs for cost, latency, and data lineage. This isn't an add-on; it's part of the core framework.
-   **Production-Grade Reliability**: Build resilient agents with built-in policies for caching (with TTL), automatic retries with exponential backoff, and circuit breakers to prevent cascading failures.
-   **Secure by Design**: A declarative, role-based access control (RBAC) system for tools ensures that agents and users only have access to the functions they're authorized to use.
-   **Developer-First Experience**: With features like automatic tool-schema generation, optional state validation, and a visual run tracer (via the audit log), SafeAgent is designed to maximize developer velocity and minimize debugging headaches.

## Getting Started

-   **[Tutorial](./getting-started/tutorial.md)**: See the power of SafeAgent in a single, runnable script.
-   **[Configuration](./getting-started/configuration.md)**: Learn how to configure SafeAgent for your environment.

## Ready for Advanced Use Cases?

-   **[Stateful Agents](./advanced-guides/stateful-agents.md)**: See how to build complex, cyclical agents using the `StatefulOrchestrator`.
-   **[Production Policies](./advanced-guides/production-policies.md)**: Dive deep into the reliability and cost-management features of the `ToolRegistry`.
-   **[Output Sinks](./advanced-guides/output-sinks.md)**: Learn how to automatically send tool outputs to other systems like files or message queues.