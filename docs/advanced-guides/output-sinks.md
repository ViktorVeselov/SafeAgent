# Advanced Guide: Tool Output Sinks

In a production environment, a tool's output often needs to be sent to other systems. SafeAgent handles this declaratively with **Output Sinks**.

## The Core Idea
Instead of writing publishing logic inside every tool, you can attach "sinks" to a tool when you register it. After the tool runs successfully, the framework automatically sends its result to each attached sink.

## Example: Saving and Publishing Tool Results

This runnable example defines a tool to generate an invoice and attaches two sinks:
1.  A `FileOutputSink` to save a JSON record locally.
2.  A conceptual `PubSubSink` to send the data to a cloud messaging queue.

```python
from safeagent import *
import datetime
import os
import json
import shutil

# --- Setup ---
gov = GovernanceManager()
tool_registry = ToolRegistry(governance_manager=gov)

# 1. Define and register the tool with multiple output sinks
@tool_registry.register(
    required_role="billing",
    output_sinks=[
        FileOutputSink(base_path="invoices"), # Sink 1
        PubSubSink(project_id="my-gcp-project", topic_id="invoice-queue") # Sink 2
    ]
)
def generate_invoice(customer_id: int, amount: float) -> dict:
    """Generates a new invoice for a customer."""
    return {
        "invoice_id": f"INV-{datetime.datetime.now().timestamp()}",
        "customer_id": customer_id, "amount": amount,
        "due_date": (datetime.date.today() + datetime.timedelta(days=30)).isoformat()
    }

# --- Execution ---
gov.start_new_run() 
invoice_tool = tool_registry.get_governed_tool(name="generate_invoice", user_id="billing_clerk")
result = invoice_tool(customer_id=123, amount=99.99)
print(f"Tool Result: {result}")

# --- Verification ---
run_id = gov.get_current_run_id()
expected_path = os.path.join("invoices", f"generate_invoice_{run_id}.json")
print(f"\nVerifying file sink result at: {expected_path}")

with open(expected_path, "r") as f:
    saved_data = json.load(f)

print(f"\n--- Contents of Saved File ---\n{json.dumps(saved_data, indent=2)}")

shutil.rmtree("invoices")
```