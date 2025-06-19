# Example: Database Integration Agent

A common use case for an LLM agent is to provide a natural language interface to a database. This example shows how to build a tool that can query a SQLite database, and an agent that can use it.

## 1. Setup: Create a Dummy Database
This script creates a simple `company.db` file with some sample data.

```python
import sqlite3
import os

print("Creating dummy database 'company.db'...")
conn = sqlite3.connect("company.db")
cursor = conn.cursor()
cursor.execute("DROP TABLE IF EXISTS employees")
cursor.execute("CREATE TABLE employees (id INT, name TEXT, role TEXT, department TEXT)")
cursor.execute("INSERT INTO employees VALUES (1, 'Alice', 'Engineer', 'Technology')")
cursor.execute("INSERT INTO employees VALUES (2, 'Bob', 'Sales Manager', 'Sales')")
conn.commit()
conn.close()
print("Database created successfully.")
```

## 2. Full Agent Script
This is the complete, runnable script for the database agent.

```python
from safeagent import *
import sqlite3
import json
import os

# --- Tool Definition ---
gov = GovernanceManager()
tool_registry = ToolRegistry(governance_manager=gov)

@tool_registry.register(required_role="analyst", cost_per_call=0.005)
def execute_sql_query(query: str) -> str:
    """Executes a read-only SQL query on the company database. Only SELECT statements are allowed."""
    if not query.strip().upper().startswith("SELECT"):
        return "Error: Only SELECT queries are permitted."
    try:
        conn = sqlite3.connect("company.db")
        cursor = conn.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        column_names = [d[0] for d in cursor.description]
        conn.close()
        if not results: return "Query returned no results."
        return json.dumps({"columns": column_names, "data": results})
    except Exception as e:
        return f"Query failed. Error: {e}"

# --- Agent Setup ---
cfg = Config()
llm = LLMClient(api_key=cfg.api_key)
agent = StatefulOrchestrator(entry_node="formulate_query")

# --- Node Definitions ---
def formulate_query(state: dict) -> dict:
    prompt = f"Given the user question, write a single, valid SQLite query to answer it. Table: 'employees' (id, name, role, department).\nQuestion: {state['question']}\nSQL Query:"
    response = llm.generate(prompt)
    sql_query = response['text'].strip().replace('`', '').replace('sql', '')
    return {"sql_query": sql_query}

def run_query(state: dict) -> dict:
    tool = tool_registry.get_governed_tool("execute_sql_query", "analyst_user")
    results = tool(query=state['sql_query'])
    return {"db_results": results}
    
def synthesize_answer(state: dict) -> dict:
    prompt = f"Based on these DB results, answer the user's question.\nQuestion: {state['question']}\nDB Results: {state['db_results']}\nAnswer:"
    response = llm.generate(prompt)
    return {"final_answer": response['text']}

# --- Build and Run ---
agent.add_node("formulate_query", formulate_query)
agent.add_node("run_query", run_query)
agent.add_node("synthesize_answer", synthesize_answer)
agent.add_edge("formulate_query", "run_query")
agent.add_edge("run_query", "synthesize_answer")
agent.add_edge("synthesize_answer", "__end__")

gov.start_new_run()
initial_state = {"question": "Who is the sales manager?"}
status, final_state = agent.run(initial_state)

print(f"\n--- FINAL ANSWER ---\n{final_state.get('final_answer')}")

if os.path.exists("company.db"): os.remove("company.db")
```