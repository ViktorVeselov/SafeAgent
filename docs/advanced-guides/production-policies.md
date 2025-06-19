# Advanced Guide: Production Policies

A key advantage of SafeAgent is the ability to declaratively add production-grade policies to your tools via the `@tool_registry.register` decorator.

## 1. Caching (`cache_ttl_seconds`)
Prevents redundant tool calls by caching results.
```python
@tool_registry.register(cache_ttl_seconds=300)
def get_user_profile(user_id: int) -> dict: #...
```

## 2. Retries (`retry_attempts`, `retry_delay`)
Automatically retries a tool if it fails due to transient issues.
```python
@tool_registry.register(retry_attempts=2, retry_delay=2.0)
def call_flaky_api(): #...
```

## 3. Circuit Breaker (`circuit_breaker_threshold`)
Prevents an agent from repeatedly calling a service that is clearly down.
```python
@tool_registry.register(circuit_breaker_threshold=5)
def call_critical_service(): #...
```

## 4. Cost Tracking (`cost_per_call`, `cost_calculator`)
Adds cost information to the audit log for every tool call.
```python
# Fixed cost
@tool_registry.register(cost_per_call=0.01)
def get_map_data(): #...
```

## 5. Security (`required_role`)
Restricts tool execution to users with a specific role.
```python
@tool_registry.register(required_role="billing_admin")
def process_refund(transaction_id: str): #...
```