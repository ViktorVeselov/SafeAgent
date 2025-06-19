# Core Concepts: Orchestrators

Orchestrators are the engines that execute your agent's logic. SafeAgent provides two distinct orchestrators, each designed for a different type of task.

## 1. `SimpleOrchestrator`

The `SimpleOrchestrator` is a straightforward **Directed Acyclic Graph (DAG)** runner. It's perfect for linear, predictable workflows where one step follows another without complex branching or loops.

-   **Best For**: Data processing pipelines, question-answering with a fixed set of steps (e.g., retrieve -> prompt -> answer), and the pre-built MCP protocol.
-   **How it Works**: You define nodes (Python functions) and edges (dependencies between nodes). The orchestrator automatically injects the output of a dependency as an input to the next node.

## 2. `StatefulOrchestrator`

The `StatefulOrchestrator` is a powerful engine for building complex, **cyclical agents** that can make decisions and repeat tasks. It manages a central state object that is passed to every node.

-   **Best For**: Building ReAct (Reason-Act) style agents, workflows with conditional branching, and human-in-the-loop processes.
-   **How it Works**: Nodes receive the entire state and return a dictionary of updates. Edges can be conditional, using a function to decide which node to run next based on the current state.

See the [Stateful Agents Advanced Guide](../advanced-guides/stateful-agents.md) for a complete example.