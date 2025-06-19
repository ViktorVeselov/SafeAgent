# Core Concepts

MiniLLM consists of small, composable modules that can be swapped out as your application grows. The default configuration uses Gemini for text generation and embeddings.

## Memory Manager

`MemoryManager` stores a rolling summary of past conversations. It supports a Redis backend for persistence and an in-memory fallback for quick testing.

## Retrievers

Two retrievers help fetch relevant documents:

- `VectorRetriever` uses FAISS for similarity search. It calls the `gemini_embed` function to compute embeddings.
- `GraphRetriever` performs Neo4j graph search and also relies on the Gemini embedding API for text similarity.

## Orchestrator

`SimpleOrchestrator` connects each step of the workflow in a directed acyclic graph. You can add nodes and edges to customise the execution order.

Together these pieces let you build durable, stateful agents that remember past context and retrieve domain knowledge when answering new questions.
