# Example: Multi-Tool ReAct Agent

This advanced example builds an agent with access to **multiple tools**. The agent uses semantic search to choose the best tool for the job.

## Full Agent Script

```python
from safeagent import *
import json

# --- Setup ---
gov = GovernanceManager()
cfg = Config()
llm = LLMClient(api_key=cfg.api_key)
tool_registry = ToolRegistry(
    governance_manager=gov,
    embedding_config={"api_key": cfg.api_key},
    similarity_metric=SimilarityMetric.COSINE
)

# --- Tool 1: Weather ---
@tool_registry.register(cache_ttl_seconds=60)
def get_weather(city: str) -> str:
    """Gets the current weather conditions for a specified city."""
    if "boston" in city.lower(): return "68°F and cloudy."
    return "Weather unavailable."

# --- Tool 2: User Profile ---
@tool_registry.register(required_role="support")
def get_user_email(username: str) -> str:
    """Retrieves the contact email address for a given system username."""
    if "alex" in username.lower(): return "alex@example.com"
    return "User not found."

# --- Agent Nodes ---
def reason_node(state: dict) -> dict:
    question = state['question']
    relevant_tools = tool_registry.get_relevant_tools(question, top_k=2)
    tool_schemas = tool_registry.generate_tool_schema(relevant_tools)
    
    prompt = f"Question: {question}\nHistory: {state.get('history', [])}\nChoose the best tool from this list to answer. If no tool is relevant or you have enough info, respond with the final answer. Tools: {json.dumps(tool_schemas)}"
    response = llm.generate(prompt)
    
    try:
        decision = json.loads(response['text'])
        return {"decision": decision}
    except json.JSONDecodeError:
        return {"decision": {"tool_name": "__end__", "final_answer": response['text']}}

def act_node(state: dict) -> dict:
    tool_name = state['decision']['tool_name']
    tool_args = state['decision']['tool_args']
    governed_tool = tool_registry.get_governed_tool(tool_name, user_id="support")
    observation = governed_tool(**tool_args)
    new_history = state.get('history', []) + [f"Tool '{tool_name}' said: '{observation}'"]
    return {"history": new_history}

def should_continue(state: dict) -> str:
    return "__end__" if state['decision'].get('tool_name') == "__end__" else "reason_node"

# --- Build and Run ---
agent = StatefulOrchestrator(entry_node="reason_node")
agent.add_node("reason_node", reason_node)
agent.add_node("act_node", act_node)
agent.add_conditional_edge("reason_node", should_continue)
agent.add_edge("act_node", "reason_node")

# --- Test Cases ---
print("\n--- Test Case 1: Weather ---")
gov.start_new_run()
initial_state_1 = {"question": "What's the weather like in Boston?"}
status, final_state = agent.run(initial_state_1)
print(f"\nFinal Answer: {final_state.get('decision', {}).get('final_answer')}")

print("\n--- Test Case 2: User Email ---")
gov.start_new_run()
initial_state_2 = {"question": "I need the email for user alex."}
status, final_state = agent.run(initial_state_2)
print(f"\nFinal Answer: {final_state.get('decision', {}).get('final_answer')}")
```