# Advanced Guide: Stateful Agents (ReAct)

The `StatefulOrchestrator` is designed to build complex agents that can reason, act, and loop until a task is complete. A classic example is the **ReAct (Reason + Act)** pattern.

This is a complete, runnable script for a ReAct agent.

```python
from safeagent import *
import json

# --- Setup ---
gov = GovernanceManager()
cfg = Config()
llm = LLMClient(api_key=cfg.api_key)
tool_registry = ToolRegistry(governance_manager=gov, embedding_config={"api_key": cfg.api_key})

@tool_registry.register()
def search_wikipedia(query: str) -> str:
    """Searches for a term on Wikipedia. Use this for general knowledge questions."""
    print(f"TOOL: Searching Wikipedia for '{query}'")
    if "zephyrhills" in query.lower():
        return "Zephyrhills is a city in Pasco County, Florida, known for its bottled water."
    return "No information found for that query."

# --- Agent Nodes ---
def reason_node(state: dict) -> dict:
    """Decides which tool to use or if the task is complete."""
    print("--- STEP: REASONING ---")
    
    prompt = f"Question: {state['question']}\n"
    prompt += f"Conversation History: {state.get('history', [])}\n\n"
    prompt += "Decide the next action. Should you use a tool, or do you have the final answer? "
    prompt += "If using a tool, respond with JSON: {\"tool_name\": \"tool_to_use\", \"tool_args\": {\"arg\": \"value\"}}. "
    prompt += "Otherwise, respond with the final answer as a plain string."
    
    response = llm.generate(prompt)
    
    try:
        decision = json.loads(response['text'])
        print(f"Decision: Call tool '{decision.get('tool_name')}'")
        return {"decision": decision}
    except json.JSONDecodeError:
        print(f"Decision: Final Answer Found")
        return {"decision": {"tool_name": "__end__", "final_answer": response['text']}}

def act_node(state: dict) -> dict:
    """Executes the chosen tool."""
    print("--- STEP: ACTING ---")
    tool_name = state['decision']['tool_name']
    tool_args = state['decision']['tool_args']
    
    governed_tool = tool_registry.get_governed_tool(tool_name, user_id="agent_123")
    observation = governed_tool(**tool_args)
    
    print(f"Observation: {observation}")
    new_history = state.get('history', []) + [f"Called tool '{tool_name}' and got this result: '{observation}'"]
    return {"history": new_history}

# --- Define Conditional Edge ---
def should_continue(state: dict) -> str:
    """The routing logic for the graph. It checks the reasoning decision."""
    if state['decision']['tool_name'] == "__end__":
        return "__end__"
    return "act_node"

# --- Build and Run the Graph ---
agent = StatefulOrchestrator(entry_node="reason_node")
agent.add_node("reason_node", reason_node)
agent.add_node("act_node", act_node)
agent.add_edge("act_node", "reason_node") 
agent.add_conditional_edge("reason_node", should_continue)

initial_state = {"question": "What is Zephyrhills known for?"}
gov.start_new_run()
status, final_state = agent.run(initial_state)

print("\n--- AGENT FINISHED ---")
print(f"Status: {status}")
print(f"Final Answer: {final_state.get('decision', {}).get('final_answer')}")

```