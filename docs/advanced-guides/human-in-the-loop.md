# Advanced Guide: Human-in-the-Loop

For many critical tasks, you need to pause an agent's execution and ask for human approval. The `StatefulOrchestrator` supports this with a special `__interrupt__` node.

## Example: Agent Seeking Approval
This is a complete, runnable script demonstrating a human-in-the-loop workflow.

```python
from safeagent import *

# --- Setup ---
gov = GovernanceManager()
llm = LLMClient(api_key=Config().api_key)
def send_email(body: str): 
    print("--- EMAIL SENT ---")
    print(body)

# --- Agent Nodes ---
def draft_email(state: dict) -> dict:
    prompt = f"Draft a polite email about: {state['topic']}"
    response = llm.generate(prompt, max_tokens=100)
    return {"draft": response['text']}

def get_human_approval(state: dict) -> str:
    return "__interrupt__"

# --- Build and Run ---
agent = StatefulOrchestrator(entry_node="draft_email")
agent.add_node("draft_email", draft_email)
agent.add_node("send_final_email", lambda state: send_email(state['final_draft']))
agent.add_conditional_edge("draft_email", get_human_approval)
agent.add_edge("send_final_email", "__end__")

gov.start_new_run() 
initial_state = {"topic": "team meeting moved to 3 PM"}
status, paused_state = agent.run(initial_state)

print(f"\n--- AGENT PAUSED --- DRAFT FOR APPROVAL:\n{paused_state['draft']}")

if status == "paused":
    feedback = input("\nType 'approve' or provide edits: ")
    human_input = {"final_draft": paused_state['draft'] if "approve" in feedback.lower() else feedback}
    paused_state['__next_node__'] = 'send_final_email'
    
    status, final_state = agent.resume(paused_state, human_input)
    print(f"\n--- AGENT COMPLETED --- Final Status: {status}")
```