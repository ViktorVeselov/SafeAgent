# Welcome to SafeAgent

**SafeAgent** is a minimal, flexible framework for orchestrating **production-ready LLM agents**. It provides pluggable components for retrieval, memory, and orchestration with enterprise-grade governance, reliability, and observability built-in from day one.

While many tools can help you build a prototype, SafeAgent is designed to build systems you can confidently run in production.

## The SafeAgent Advantage: Beyond the Prototype

-   **Unparalleled Governance & Observability**: Every action—from LLM calls to tool executions—is automatically audited with detailed logs for cost, latency, and data lineage. This isn't an add-on; it's part of the core framework.
-   **Production-Grade Reliability**: Build resilient agents with built-in policies for caching (with TTL), automatic retries with exponential backoff, and circuit breakers to prevent cascading failures.
-   **Secure by Design**: A declarative, role-based access control (RBAC) system for tools ensures that agents and users only have access to the functions they're authorized to use.
-   **Developer-First Experience**: With features like automatic tool-schema generation, optional state validation, and a visual run tracer (via the audit log), SafeAgent is designed to maximize developer velocity and minimize debugging headaches.

---

## Table of Contents

### Getting Started
-   **[Quickstart](./quickstart.md)**: A brief introduction to get you up and running.
-   **[Tutorial](./getting-started/tutorial.md)**: See the power of SafeAgent in a single, runnable script.
-   **[Configuration](./getting-started/configuration.md)**: Learn how to configure SafeAgent for your environment.

### Core Concepts
-   **[Overview](./concepts.md)**: A high-level look at the concepts in SafeAgent.
-   **[Orchestrators](./core-concepts/orchestrators.md)**: Learn about the components that drive the agent's logic.
-   **[Tool Registry](./core-concepts/tool-registry.md)**: Manage and secure your agent's tools.
-   **[Retrievers](./core-concepts/retrievers.md)**: Provide external knowledge to your agents.
-   **[Memory](./core-concepts/memory.md)**: Give your agents short-term and long-term memory.
-   **[Governance](./core-concepts/governance.md)**: Understand the built-in security and observability features.
-   **[Storage & Persistence](./core-concepts/storage-and-persistence.md)**: Learn how to save and load agent states.
-   **[LLM Client](./core-concepts/llm-client.md)**: Interact with Language Models.

### Advanced Guides
-   **[Stateful Agents (ReAct)](./advanced-guides/stateful-agents.md)**: Build complex, cyclical agents.
-   **[Production Policies](./advanced-guides/production-policies.md)**: Dive deep into reliability and cost-management.
-   **[Human-in-the-Loop](./advanced-guides/human-in-the-loop.md)**: Add human oversight to your agents.
-   **[Output Sinks](./advanced-guides/output-sinks.md)**: Automatically send tool outputs to other systems.

### Examples
-   **[Custom Tool Suite](./examples/custom-tool-suite.md)**: See how to create and use your own tools.
-   **[Database Integration](./examples/database-integration.md)**: Connect your agent to a database.
-   **[Multi-Tool ReAct Agent](./examples/multi-tool-agent.md)**: Build an agent that can use multiple tools.

### API Reference
-   **[Overview](./api/index.md)**: Start here for the API documentation.
-   **[Reference](./reference.md)**: Detailed API reference.
-   **[Core](./api/core.md)**: Core components of the framework.
-   **[Orchestrators](./api/orchestrators.md)**: API for orchestration.
-   **[Protocols](./api/protocols.md)**: Data protocols and models.
-   **[Sinks](./api/sinks.md)**: API for output sinks.
-   **[Tooling](./api/tooling.md)**: Utilities and helpers for tool creation.

### Other
-   **[Comparison](./comparison.md)**: How SafeAgent compares to other frameworks.