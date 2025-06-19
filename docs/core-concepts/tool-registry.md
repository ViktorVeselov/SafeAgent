# Core Concepts: Tool Registry

The `ToolRegistry` is one of the most powerful and unique components of SafeAgent. It's not just a place to store functions; it's a complete, production-grade framework for managing how your agent interacts with the outside world.

## The `@register` Decorator

You add tools to the registry using the `@register` decorator. In its simplest form, you can just decorate a Python function.

```python
from minillm import ToolRegistry, GovernanceManager

gov = GovernanceManager()
tool_registry = ToolRegistry(governance_manager=gov)

@tool_registry.register()
def get_current_user():
    """Returns the name of the current user."""
    return "Alex"
```

## Built-in Superior Features

Even in this simple example, the `ToolRegistry` is already providing immense value that is superior to other frameworks:

1.  **Automatic Governance**: Every time `get_current_user` is called via the registry, its execution is logged by the `GovernanceManager` with details about the arguments, result, and latency.
2.  **Semantic Searchability**: The tool's name (`get_current_user`) and its docstring (`Returns the name...`) are automatically embedded and indexed in a vector store. This allows the framework to dynamically find the most relevant tools for a given task.
3.  **Automatic Schema Generation**: The registry can inspect the function's signature and docstring to generate a perfect, machine-readable schema to show to the LLM, ensuring it knows how to call the tool correctly.

## Production-Grade Policies

The true power of the `ToolRegistry` is revealed when you add **policies** to the decorator. These allow you to declaratively add reliability and security features to any tool.

```python
@tool_registry.register(
    required_role="analyst", # Security
    cache_ttl_seconds=60,    # Caching
    retry_attempts=3,        # Reliability
    cost_per_call=0.01,      # Cost Tracking
    output_sinks=[FileOutputSink()] # NEW: Output Handling
)
def get_financial_data(ticker: str):
    """Fetches financial data for a stock ticker."""
    # ...
```

These features are what elevate SafeAgent from a prototyping tool to a true production framework. To learn more, see the [Production Policies Advanced Guide](../advanced-guides/production-policies.md) and the guide on [Output Sinks](../advanced-guides/output-sinks.md).