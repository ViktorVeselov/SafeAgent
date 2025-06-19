# Example: Building a Custom Tool Suite

This example demonstrates how to create and register multiple custom tools, including one that interacts with the local filesystem, each with its own set of production-grade policies.

## 1. The Goal

We want to create an agent that can both look up user information and save notes to a file. These tools have very different requirements: one is a read-only operation that can be cached, while the other is a write operation that should never be cached.

## 2. Defining the Tools

This is a complete, runnable script that defines and then tests the tools.

```python
from safeagent import ToolRegistry, GovernanceManager
import datetime
import os
import shutil

# --- Setup ---
gov = GovernanceManager()
tool_registry = ToolRegistry(governance_manager=gov)

# --- Tool 1: A read-only data lookup tool ---
@tool_registry.register(
    cache_ttl_seconds=3600,
    required_role="support_agent"
)
def get_user_details(username: str) -> dict:
    """Retrieves profile information for a given username, such as signup date and account tier."""
    print(f"DATABASE: Querying for user '{username}'...")
    if username == "alice":
        return {"username": "alice", "signup_date": "2023-01-15", "tier": "premium"}
    return {"error": "User not found"}

# --- Tool 2: A tool that interacts with the filesystem ---
@tool_registry.register(
    retry_attempts=1,
    required_role="support_agent"
)
def save_note_to_file(filename: str, content: str) -> str:
    """Saves a string of text to a local file, appending a timestamp."""
    try:
        os.makedirs("notes", exist_ok=True)
        filepath = os.path.join("notes", filename)
        with open(filepath, 'a') as f:
            f.write(f"[{datetime.datetime.now().isoformat()}] {content}\n")
        return f"Successfully saved note to {filepath}."
    except Exception as e:
        raise e

# --- Using the Tools ---
print("--- Testing the Tool Suite ---")
gov.start_new_run()
user_details_tool = tool_registry.get_governed_tool("get_user_details", "support_agent")

print("\nCalling 'get_user_details' for the first time...")
result1 = user_details_tool(username="alice")
print(f"Result 1: {result1}")

print("\nCalling 'get_user_details' again to test cache...")
result2 = user_details_tool(username="alice")
print(f"Result 2: {result2}")
print("Note: The 'DATABASE: Querying...' message should only appear once.")

gov.start_new_run()
save_note_tool = tool_registry.get_governed_tool("save_note_to_file", "support_agent")
print("\nCalling 'save_note_to_file'...")
save_result = save_note_tool(filename="support_log.txt", content="Customer issue #555 resolved.")
print(f"Result: {save_result}")

if os.path.exists("notes"): shutil.rmtree("notes")

```