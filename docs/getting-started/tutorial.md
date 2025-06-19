# Getting Started with SafeAgent

Welcome! This guide will walk you through the core value of **SafeAgent**: building powerful, production-ready tools with minimal effort. We'll show you how to take a simple Python function and instantly upgrade it with security, reliability, and governance.

## Installation

First, you'll need to install SafeAgent and its optional dependencies. It's recommended to do this in a virtual environment.

```bash
pip install -e .[test] faiss-cpu numpy rbac
```

Next, SafeAgent needs an LLM API key. Set your key as an environment variable, and the framework will automatically detect it.

```bash
export GEMINI_API_KEY="YOUR_API_KEY"
```

## The "One-Decorator" Advantage

The core philosophy of SafeAgent's `ToolRegistry` is to let you focus on your business logic. You write a plain Python function, and our `@register` decorator wraps it in a complete production-grade safety harness.

Let's build an example step-by-step.

### Step 1: Initialize SafeAgent Components

Every project starts by initializing the core components. For this guide, we only need the `GovernanceManager` and the `ToolRegistry`.

```python
from minillm import ToolRegistry, GovernanceManager

gov = GovernanceManager()
tool_registry = ToolRegistry(governance_manager=gov)
```

### Step 2: Define Your Core Logic

Imagine you have a function that calls a weather API which is sometimes unreliable.

```python
def get_weather_from_flaky_api(city: str) -> str:
    """Gets the current weather, but the API fails sometimes."""
    if not hasattr(get_weather_from_flaky_api, "call_count"):
        get_weather_from_flaky_api.call_count = 0
    get_weather_from_flaky_api.call_count += 1
    if get_weather_from_flaky_api.call_count == 1:
        raise ConnectionError("Network Error: Failed to connect.")
    return f"It is 75°F and sunny in {city}."
```

### Step 3: Apply Production Policies with `@register`

We take our simple, flaky function and make it robust by registering it as a governed tool.

```python
from minillm import RBACError

@tool_registry.register(
    required_role="weather_forecaster",
    retry_attempts=2,
    cache_ttl_seconds=60,
    cost_per_call=0.002
)
def get_weather(city: str) -> str:
    """A governed tool to fetch the weather for a specified city."""
    return get_weather_from_flaky_api(city)
```

### Step 4: Use the Governed Tool

Now, instead of calling your original function, you get the "governed" version from the registry.

```python
# Get the wrapped, robust version of your tool.
governed_weather_tool = tool_registry.get_governed_tool(
    name="get_weather",
    user_id="forecaster_alex" # This user has the required role.
)
```

### Full Script for Convenience

Here is the complete, runnable script from this tutorial.

```python
import os
import json
from minillm import ToolRegistry, GovernanceManager, RBACError

print("Initializing SafeAgent components...")
gov = GovernanceManager()
tool_registry = ToolRegistry(governance_manager=gov)

if os.path.exists("audit.log"): os.remove("audit.log")

def get_weather_from_flaky_api(city: str) -> str:
    if not hasattr(get_weather_from_flaky_api, "call_count"):
        get_weather_from_flaky_api.call_count = 0
    get_weather_from_flaky_api.call_count += 1
    if get_weather_from_flaky_api.call_count == 1:
        raise ConnectionError("Network Error: Failed to connect.")
    return f"It is 75°F and sunny in {city}."

@tool_registry.register(
    required_role="weather_forecaster",
    retry_attempts=2,
    retry_delay=0.1,
    cache_ttl_seconds=60,
    cost_per_call=0.002
)
def get_weather(city: str) -> str:
    return get_weather_from_flaky_api(city)

print("\n--- DEMONSTRATING GOVERNED EXECUTION ---")
governed_tool = tool_registry.get_governed_tool("get_weather", "forecaster_alex")

print("\n1. Calling the tool for the first time (will retry internally)...")
gov.start_new_run()
result1 = governed_tool(city="Miami")
print(f"   -> Success! Result: '{result1}'")

print("\n2. Calling the tool again (will hit cache)...")
gov.start_new_run()
result2 = governed_tool(city="Miami")
print(f"   -> Success! Result: '{result2}'")

print("\n3. Calling with an unauthorized user...")
unauthorized_tool = tool_registry.get_governed_tool("get_weather", "intern_bob")
try:
    unauthorized_tool(city="Miami")
except RBACError as e:
    print(f"   -> Success! Tool call failed as expected: {e}")

print("\n--- GOVERNANCE PROOF: INSPECTING audit.log ---")
with open("audit.log", "r") as f:
    for line in f:
        log = json.loads(line)
        action = log.get('action')
        if action == 'tool_call_error': print("[LOG] The underlying network error was automatically caught and logged.")
        if action == 'tool_call_start' and log.get('metadata', {}).get('attempt') == 2: print("[LOG] The retry policy automatically triggered a second attempt.")
        if action == 'tool_call_end': print(f"[LOG] The tool succeeded. Log includes latency and cost: {log.get('metadata')}")
        if action == 'tool_cache_hit': print("[LOG] The second call was a cache hit! The function did not run again.")
        if action == 'tool_access_denied': print(f"[LOG] The unauthorized user was correctly denied access.")
```