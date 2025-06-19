# Core Concepts: Governance

The `GovernanceManager` is the "conscience" of the SafeAgent framework. It provides a complete, transparent, and auditable record of your agent's actions in `audit.log`.

## Example: Seeing Governance in Action

This script runs a simple tool and shows the resulting `audit.log` entry.

```python
import os
import json
from safeagent import ToolRegistry, GovernanceManager

if os.path.exists("audit.log"): os.remove("audit.log")
gov = GovernanceManager()
tool_registry = ToolRegistry(governance_manager=gov)

@tool_registry.register(cost_per_call=0.001)
def get_service_status(service: str) -> str:
    return "OK"

gov.start_new_run()
tool = tool_registry.get_governed_tool("get_service_status", "test_user")
tool(service="billing_api")

print("--- Contents of audit.log ---")
with open("audit.log", "r") as f:
    for line in f: print(json.dumps(json.loads(line), indent=2))
```