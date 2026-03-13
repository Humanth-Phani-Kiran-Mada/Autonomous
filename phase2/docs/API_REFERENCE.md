# 📖 Phase 2 API Reference

> **Complete API documentation for all Phase 2 components**

**Version:** 1.0 | **Last Updated:** March 13, 2026 | **Status:** ✅ Complete

---

## 📋 Table of Contents

1. [Quick Reference](#quick-reference)
2. [Component Wrapper API](#component-wrapper-api)
3. [Distributed Tracing API](#distributed-tracing-api)
4. [Load Balancer API](#load-balancer-api)
5. [Common Patterns](#common-patterns)
6. [Error Handling](#error-handling)

---

## 🚀 Quick Reference

### Component Wrapper
```python
from component_wrapper_factory import ComponentWrapperFactory

# Create factory
wrapper = ComponentWrapperFactory()

# Get wrapped component
component = wrapper.get_component('component_type')

# Use component
result = component.execute(data)

# Get metrics
metrics = wrapper.get_metrics('component_type')
```

### Distributed Tracing
```python
from distributed_tracing import DistributedTracingSystem

# Create tracing system
tracing = DistributedTracingSystem()

# Start tracing request
trace = tracing.start_trace('request_id', 'service_name')

# Create spans
span = trace.create_span('operation_name')

# End span
span.end()

# Complete trace
trace.complete()

# Get trace data
trace_data = tracing.get_trace('request_id')
```

### Load Balancer
```python
from intelligent_load_balancer import IntelligentLoadBalancer

# Create load balancer
lb = IntelligentLoadBalancer(strategy='least_loaded')

# Register services
lb.register_service('service_a', '127.0.0.1:8001')
lb.register_service('service_b', '127.0.0.1:8002')

# Route request
service = lb.select_service(request_data)

# Update metrics
lb.update_service_metrics('service_a', load=0.75, healthy=True)

# Get routing decision
decision = lb.get_routing_decision(request_data)
```

---

## 🏭 Component Wrapper API

### Class: `ComponentWrapperFactory`

#### Constructor
```python
class ComponentWrapperFactory:
    def __init__(self, 
                 cache_enabled: bool = True,
                 cache_ttl: int = 300,
                 max_cache_size: int = 1000,
                 discovery_path: str = './components',
                 monitor_enabled: bool = True):
```

**Parameters:**
- `cache_enabled` (bool): Enable component caching (default: True)
- `cache_ttl` (int): Cache TTL in seconds (default: 300)
- `max_cache_size` (int): Maximum cached components (default: 1000)
- `discovery_path` (str): Path to discover components (default: './components')
- `monitor_enabled` (bool): Enable performance monitoring (default: True)

**Example:**
```python
wrapper = ComponentWrapperFactory(
    cache_ttl=600,  # 10 minutes
    max_cache_size=2000
)
```

---

#### Method: `get_component()`
```python
def get_component(self, 
                  component_type: str,
                  **kwargs) -> WrappedComponent:
```

**Description:** Get a wrapped component, using cache if available

**Parameters:**
- `component_type` (str): Type of component to get
- `**kwargs`: Additional parameters passed to component

**Returns:** Wrapped component ready to use

**Raises:**
- `ComponentNotFoundError`: If component type not found
- `ComponentWrapperError`: If wrapping fails

**Example:**
```python
# Get component (cache hit on subsequent calls)
component = wrapper.get_component('ml_model')

# With parameters
component = wrapper.get_component('service', config='prod')

# Use component
result = component.execute(data)
```

---

#### Method: `get_metrics()`
```python
def get_metrics(self, 
                component_type: str = None) -> dict:
```

**Description:** Get performance metrics for component(s)

**Parameters:**
- `component_type` (str, optional): Specific component, or all if None

**Returns:** Dictionary of metrics

**Example:**
```python
# Get specific component metrics
metrics = wrapper.get_metrics('ml_model')
# Returns: {
#     'cache_hits': 1523,
#     'cache_misses': 47,
#     'avg_cache_hit_time': 0.8,
#     'cache_hit_ratio': 0.97,
#     'total_calls': 1570
# }

# Get all metrics
all_metrics = wrapper.get_metrics()
```

---

#### Method: `clear_cache()`
```python
def clear_cache(self, 
                component_type: str = None) -> None:
```

**Description:** Clear cache for component(s)

**Parameters:**
- `component_type` (str, optional): Specific component, or all if None

**Example:**
```python
# Clear specific component
wrapper.clear_cache('ml_model')

# Clear all cache
wrapper.clear_cache()
```

---

#### Method: `discover_components()`
```python
def discover_components(self) -> List[str]:
```

**Description:** Discover available components

**Returns:** List of component types found

**Example:**
```python
components = wrapper.discover_components()
# Returns: ['ml_model', 'nlp_service', 'cache_service']
```

---

### Class: `WrappedComponent`

Returned by `get_component()` method

#### Method: `execute()`
```python
def execute(self, 
            data: Any,
            **kwargs) -> Any:
```

**Description:** Execute the wrapped component

**Parameters:**
- `data`: Input data for component
- `**kwargs`: Additional parameters

**Returns:** Component execution result

**Example:**
```python
component = wrapper.get_component('ml_model')
result = component.execute(input_data)
```

---

#### Property: `metadata`
```python
@property
def metadata(self) -> dict:
```

**Description:** Get component metadata

**Example:**
```python
component = wrapper.get_component('ml_model')
print(component.metadata)
# Returns: {
#     'name': 'ml_model',
#     'version': '1.0.0',
#     'capabilities': ['predict', 'train'],
#     'resource_limits': {'mem': '512MB', 'cpu': '1'}
# }
```

---

## 📊 Distributed Tracing API

### Class: `DistributedTracingSystem`

#### Constructor
```python
class DistributedTracingSystem:
    def __init__(self,
                 storage_backend: str = 'memory',
                 max_traces: int = 10000,
                 retention_hours: int = 24):
```

**Parameters:**
- `storage_backend` (str): Storage type ('memory', 'file', 'db')
- `max_traces` (int): Maximum stored traces
- `retention_hours` (int): How long to keep traces

---

#### Method: `start_trace()`
```python
def start_trace(self,
                request_id: str,
                service_name: str,
                metadata: dict = None) -> Trace:
```

**Description:** Start a new trace for a request

**Parameters:**
- `request_id` (str): Unique request identifier
- `service_name` (str): Name of the service
- `metadata` (dict, optional): Additional metadata

**Returns:** Trace object

**Example:**
```python
trace = tracing.start_trace(
    'req_abc123',
    'user_service',
    metadata={'user_id': '42', 'priority': 'high'}
)
```

---

#### Method: `create_span()`
```python
def create_span(self,
                trace_id: str,
                operation: str,
                parent_span_id: str = None) -> Span:
```

**Description:** Create a span within a trace

**Parameters:**
- `trace_id` (str): ID of the trace
- `operation` (str): Operation name
- `parent_span_id` (str, optional): Parent span if child span

**Returns:** Span object

**Example:**
```python
span = tracing.create_span(
    'trace_abc123',
    'database_query',
    parent_span_id='parent_span_id'
)
```

---

### Class: `Trace`

#### Method: `create_span()`
```python
def create_span(self,
                operation: str) -> Span:
```

**Description:** Create a span in this trace

**Example:**
```python
trace = tracing.start_trace('req_123', 'service')
span = trace.create_span('db_query')
```

---

#### Method: `end_span()`
```python
def end_span(self, 
             span_id: str) -> None:
```

**Description:** End a span

**Example:**
```python
span.end()  # End current span
```

---

#### Method: `add_event()`
```python
def add_event(self,
              event_name: str,
              attributes: dict = None) -> None:
```

**Description:** Add an event to the trace

**Example:**
```python
trace.add_event('cache_miss', {'cache_key': 'user_42'})
```

---

#### Method: `complete()`
```python
def complete(self) -> None:
```

**Description:** Mark trace as complete

**Example:**
```python
trace.complete()
```

---

### Class: `Span`

#### Method: `end()`
```python
def end(self,
        status: str = 'success',
        error: str = None) -> None:
```

**Description:** End the span

**Parameters:**
- `status` (str): 'success', 'failure', or 'timeout'
- `error` (str, optional): Error message if failed

**Example:**
```python
try:
    # Do work
    span.end(status='success')
except Exception as e:
    span.end(status='failure', error=str(e))
```

---

#### Method: `add_attribute()`
```python
def add_attribute(self,
                  key: str,
                  value: Any) -> None:
```

**Description:** Add attribute to span

**Example:**
```python
span.add_attribute('db_rows', 100)
span.add_attribute('cache_hit', True)
```

---

#### Method: `add_event()`
```python
def add_event(self,
              name: str,
              attributes: dict = None) -> None:
```

**Description:** Add event to span

**Example:**
```python
span.add_event('cache_miss', {'key': 'user_42'})
```

---

## ⚖️ Load Balancer API

### Class: `IntelligentLoadBalancer`

#### Constructor
```python
class IntelligentLoadBalancer:
    def __init__(self,
                 strategy: str = 'least_loaded',
                 health_check_interval: int = 5,
                 max_retries: int = 3):
```

**Parameters:**
- `strategy` (str): Routing strategy ('round_robin', 'least_loaded', 'random', 'custom')
- `health_check_interval` (int): Health check interval in seconds
- `max_retries` (int): Max retries on failure

---

#### Method: `register_service()`
```python
def register_service(self,
                     service_id: str,
                     address: str,
                     port: int,
                     metadata: dict = None) -> None:
```

**Description:** Register a service instance

**Parameters:**
- `service_id` (str): Unique service ID
- `address` (str): Service address
- `port` (int): Service port
- `metadata` (dict, optional): Additional metadata

**Example:**
```python
lb.register_service('api_1', '127.0.0.1', 8001)
lb.register_service('api_2', '127.0.0.1', 8002)
```

---

#### Method: `select_service()`
```python
def select_service(self,
                   request_data: dict = None) -> Service:
```

**Description:** Select a service for routing

**Parameters:**
- `request_data` (dict, optional): Request data for custom routing

**Returns:** Selected service

**Raises:**
- `NoHealthyServiceError`: If no healthy services available

**Example:**
```python
service = lb.select_service({'priority': 'high'})
```

---

#### Method: `update_service_metrics()`
```python
def update_service_metrics(self,
                          service_id: str,
                          load: float,
                          healthy: bool,
                          response_time: float = None) -> None:
```

**Description:** Update service metrics

**Parameters:**
- `service_id` (str): Service ID
- `load` (float): Current load (0-1)
- `healthy` (bool): Health status
- `response_time` (float, optional): Response time in ms

**Example:**
```python
lb.update_service_metrics('api_1', load=0.75, healthy=True, response_time=45)
```

---

#### Method: `get_routing_decision()`
```python
def get_routing_decision(self,
                        request_data: dict = None) -> dict:
```

**Description:** Get detailed routing decision info

**Returns:** Decision details including selected service and reasoning

**Example:**
```python
decision = lb.get_routing_decision({'priority': 'high'})
# Returns: {
#     'selected_service': 'api_2',
#     'score': 95,
#     'load': 0.4,
#     'health': 'healthy',
#     'reasoning': 'Lowest load among healthy services'
# }
```

---

#### Method: `deregister_service()`
```python
def deregister_service(self,
                       service_id: str) -> None:
```

**Description:** Deregister a service

**Example:**
```python
lb.deregister_service('api_1')
```

---

#### Method: `get_services()`
```python
def get_services(self) -> List[Service]:
```

**Description:** Get all registered services

**Returns:** List of service objects

**Example:**
```python
services = lb.get_services()
for service in services:
    print(f"{service.id}: {service.load}%")
```

---

## 🔄 Common Patterns

### Pattern 1: Use Wrapper with Tracing

```python
from component_wrapper_factory import ComponentWrapperFactory
from distributed_tracing import DistributedTracingSystem

# Setup
wrapper = ComponentWrapperFactory()
tracing = DistributedTracingSystem()

# Start tracing
trace = tracing.start_trace('req_001', 'api_service')

# Get component (wrapped and cached)
component = wrapper.get_component('processor')

# Create span  for operation
span = trace.create_span('process_data')

try:
    # Execute
    result = component.execute(data)
    span.end(status='success')
except Exception as e:
    span.end(status='failure', error=str(e))
    raise

# Complete trace
trace.complete()

# Get metrics (optional)
metrics = wrapper.get_metrics('processor')
```

---

### Pattern 2: Use Load Balancer with Tracing

```python
from intelligent_load_balancer import IntelligentLoadBalancer
from distributed_tracing import DistributedTracingSystem

# Setup
lb = IntelligentLoadBalancer(strategy='least_loaded')
tracing = DistributedTracingSystem()

# Register services
lb.register_service('api_1', '127.0.0.1', 8001)
lb.register_service('api_2', '127.0.0.1', 8002)

# Start tracing
trace = tracing.start_trace('req_001', 'router')

# Select service
service = lb.select_service()

# Create span for routing
span = trace.create_span('route_request')

# Route request
response = service.handle(request)

# Record metrics
span.add_attribute('selected_service', service.id)
span.add_attribute('response_time', response.time_ms)
span.end(status='success')

# Complete trace
trace.complete()
```

---

### Pattern 3: All Three Components

```python
from component_wrapper_factory import ComponentWrapperFactory
from distributed_tracing import DistributedTracingSystem
from intelligent_load_balancer import IntelligentLoadBalancer

# Setup
wrapper = ComponentWrapperFactory()
tracing = DistributedTracingSystem()
lb = IntelligentLoadBalancer()

# Register services
lb.register_service('compute_1', '127.0.0.1', 8001)
lb.register_service('compute_2', '127.0.0.1', 8002)

# Request arrives
def handle_request(request):
    # Start tracing
    trace = tracing.start_trace(
        request.id,
        'api_service',
        metadata={'user_id': request.user_id}
    )
    
    # Load balancer selects service
    service = lb.select_service(request)
    span1 = trace.create_span('select_service')
    span1.add_attribute('selected', service.id)
    span1.end(status='success')
    
    # Get component (cached)
    component = wrapper.get_component('processor')
    span2 = trace.create_span('get_component')
    span2.add_attribute('cache_hit', True)
    span2.end(status='success')
    
    # Execute
    span3 = trace.create_span('execute')
    result = component.execute(request.data)
    span3.end(status='success')
    
    # Complete trace
    trace.complete()
    
    return result
```

---

## ⚠️ Error Handling

### Common Exceptions

```python
# Component Wrapper
ComponentNotFoundError      # Component type not found
ComponentWrapperError       # Wrapping failed
CacheSizeExceededError      # Cache full
ResourceLimitError          # Resource limits exceeded

# Distributed Tracing
TraceNotFoundError          # Trace ID not found
SpanNotFoundError           # Span not found
TracingError                # Generic tracing error

# Load Balancer
NoHealthyServiceError       # No healthy services available
ServiceNotFoundError        # Service ID not found
RoutingError                # Routing decision failed
```

---

### Error Handling Example

```python
from component_wrapper_factory import (
    ComponentWrapperFactory,
    ComponentNotFoundError,
    ComponentWrapperError
)

wrapper = ComponentWrapperFactory()

try:
    component = wrapper.get_component('unknown_type')
except ComponentNotFoundError:
    print("Component type not found, using fallback")
    component = wrapper.get_component('default_type')
except ComponentWrapperError as e:
    print(f"Error wrapping component: {e}")
    raise
```

---

<div align="center">

## ✅ API Reference Complete

**Next:** Integrate with [INTEGRATION.md](INTEGRATION.md)  
**Or:** Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for common issues

</div>
