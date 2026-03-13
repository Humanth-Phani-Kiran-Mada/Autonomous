# 📊 Distributed Tracing System Guide

> **Deep dive into the Distributed Tracing System component**

**Version:** 1.0 | **Time to Read**: 30 minutes | **Status:** ✅ Complete

---

## 📌 Quick Summary

**What It Does:** Tracks requests end-to-end across services

**Result:** Complete visibility from request entry to response

**Use When:** Multi-service architecture needing end-to-end visibility

---

## 🎯 Core Concepts

### The Basic Idea

In monolithic systems, requests are simple:
```
Request → Process → Response
        (all in one place)
```

In microservices, requests are complex:
```
Request → Service A → Service B → Service C → Response
         (hard to track!)
```

**Problem:** How do you track where time is spent? Where did it fail? What was the sequence?

**Solution:** Distributed Tracing

```
Trace ID: abc123
├─ Start at Service A (0-50ms)
│  ├─ Call Service B (2-15ms)
│  │  └─ Call DB (5-13ms)
│  ├─ Call Service C (15-20ms)
│  └─ Aggregate results (20-50ms)
└─ Complete (50ms total)
```

---

## 💻 Basic Usage

### Setup Tracing

```python
from distributed_tracing import DistributedTracingSystem

# Create tracing system
tracing = DistributedTracingSystem()
```

### Start Tracing a Request

```python
# Start trace (once per request)
trace = tracing.start_trace(
    'req_abc123',           # Unique request ID
    'api_service',          # Service name
    metadata={'user_id': '42'}  # Optional metadata
)
```

### Create Spans for Operations

```python
# Create span for operation
span = trace.create_span('database_query')

# Do the work
try:
    result = db.query("SELECT * FROM users")
    span.add_attribute('rows', len(result))
    span.end(status='success')
except Exception as e:
    span.end(status='failure', error=str(e))
```

### Complete Trace

```python
# Always complete the trace
try:
    # ... operations ...
finally:
    trace.complete()  # IMPORTANT!
```

---

## 🔍 Advanced Features

### Nested Spans (Multi-Service Calls)

```python
# Service A's span
span_a = trace.create_span('call_service_b')

# Inside Service B, create child span
span_b = trace.create_span('database_query')

# Spans can nest to show dependencies
# Service A → Service B → Database
```

### Attributes & Events

```python
span = trace.create_span('operation')

# Add attributes (structured data)
span.add_attribute('user_id', 123)
span.add_attribute('query_time', 45.2)
span.add_attribute('cache_hit', True)

# Add events (significant occurrences)
span.add_event('cache_miss', {'key': 'user_123'})
span.add_event('retry_attempt', {'count': 1})

span.end(status='success')
```

### Error Tracking

```python
span = trace.create_span('risky_operation')

try:
    result = risky_operation()
    span.end(status='success')  # ✓ Success
except TimeoutError as e:
    span.end(status='timeout', error=str(e))  # ⏱️ Timeout
except Exception as e:
    span.end(status='failure', error=str(e))  # ✗ Failure
```

---

## 📚 Real-World Examples

### Example 1: API Request Tracing

```python
def handle_api_request(request_id, user_id):
    # Start trace
    trace = tracing.start_trace(request_id, 'api_service')
    
    try:
        # Validate input
        span1 = trace.create_span('validate_input')
        if not is_valid(request):
            span1.end(status='failure', error='Invalid input')
            return {'error': 'Invalid'}
        span1.end(status='success')
        
        # Query database
        span2 = trace.create_span('database_query')
        user_data = db.query_user(user_id)
        span2.add_attribute('user_found', user_data is not None)
        span2.end(status='success')
        
        # Process data
        span3 = trace.create_span('processing')
        result = process_data(user_data)
        span3.end(status='success')
        
        # Return result
        return {'data': result}
    
    finally:
        trace.complete()
```

### Example 2: Multi-Service Request Chain

```python
# Service A receives request
def service_a_handler(request):
    trace = tracing.start_trace(request.id, 'service_a')
    
    span = trace.create_span('call_service_b')
    
    # Call Service B (pass trace ID!)
    headers = {'X-Trace-ID': request.id}
    response = requests.post(SERVICE_B_URL, headers=headers, json=request.data)
    
    span.end(status='success')
    trace.complete()
    
    return response.json()

# Service B receives request with trace ID
def service_b_handler(request):
    trace_id = request.headers.get('X-Trace-ID')
    # Continue same trace!
    trace = tracing.continue_trace(trace_id)
    
    span = trace.create_span('business_logic')
    result = process(request.data)
    span.end(status='success')
    
    trace.complete()
    return result
```

### Example 3: Querying Traces

```python
# Find specific trace
trace = tracing.get_trace('req_abc123')

# Get details
print(f"Total latency: {trace.duration_ms}ms")
print(f"Spans: {len(trace.spans)}")

# Find slow requests
slow_traces = tracing.search_traces(
    min_latency_ms=1000  # > 1 second
)

# Find errors
error_traces = tracing.search_traces(error_only=True)

# Analyze patterns
traces = tracing.get_recent_traces(n=100)
latencies = [t.duration_ms for t in traces]
print(f"Avg latency: {sum(latencies)/len(latencies)}")
```

---

## 🔧 Troubleshooting

### Issue: Spans Not Recording

**Cause:** Trace not completed or span not ended

**Solution:**
```python
trace = tracing.start_trace(req_id, 'service')

# MUST do this:
try:
    span = trace.create_span('operation')
    # ... do work ...
    span.end(status='success')  # DON'T FORGET!
finally:
    trace.complete()  # DON'T FORGET!
```

---

### Issue: High Tracing Overhead

**Cause:** Too many spans or expensive operations

**Solution:**
```python
# DON'T: Create span for each item
for item in items:
    span = trace.create_span('process_item')
    # ... process ...
    span.end()  # Creates 1000 spans!

# DO: Use single span for batch
span = trace.create_span('process_items')
for item in items:
    # Process without per-item spans
    pass
span.end()
```

---

## ✅ Best Practices

###1. Always Complete Traces

```python
# ✅ Good
trace = tracing.start_trace(req_id, 'service')
try:
    # ... do work ...
finally:
    trace.complete()

# ❌ Bad - trace lost
trace = tracing.start_trace(req_id, 'service')
# ... do work ...
# Missing: trace.complete()!
```

### 2. Use Meaningful Span Names

```python
# ✅ Good - descriptive
span = trace.create_span('database_query_users_by_id')
span = trace.create_span('authenticate_request')

# ❌ Bad - vague
span = trace.create_span('query')
span = trace.create_span('work')
```

### 3. Add Context to Spans

```python
# ✅ Good - full context
span.add_attribute('user_id', user_id)
span.add_attribute('query_time_ms', 42)
span.add_attribute('cache_hit', True)

# ❌ Bad - no context
span.end(status='success')
```

### 4. Propagate Trace Context

```python
# ✅ Good - propagate trace ID between services
headers = {
    'X-Trace-ID': trace.id,
    'X-Service': 'service_a'
}
response = requests.post(url, headers=headers)

# ❌ Bad - lose trace context
response = requests.post(url)  # No trace ID passed!
```

### 5. Use Sampling for High Traffic

```python
# Only trace sample of requests in production
import random

if random.random() < 0.01:  # 1% sampling
    trace = tracing.start_trace(req_id, 'service')
else:
    trace = NoOpTrace()  # No overhead

# ... rest of code ...
```

---

## 📊 Performance Tuning

### Storage Configuration

```python
# Adjust retention based on needs
tracing = DistributedTracingSystem(
    retention_hours=24,  # Keep 24 hours
    max_traces=10000     # Max 10k traces
)
```

### Sampling Strategies

```python
# 1. Random sampling
if random.random() < probability:
    trace = tracing.start_trace(req_id, 'service')

# 2. Probability-based on error rate
if request.has_errors() or random.random() < 0.01:
    trace = tracing.start_trace(req_id, 'service')

# 3. Deterministic (consistent for same request)
hash_value = hash(user_id) % 100
if hash_value < 1:  # 1% of users always traced
    trace = tracing.start_trace(req_id, 'service')
```

---

## 🎯 Monitoring Traces

### Key Metrics

```python
traces = tracing.get_recent_traces(n=1000)

# Latency analysis
latencies = [t.duration_ms for t in traces]
print(f"P50: {sorted(latencies)[len(latencies)//2]}")
print(f"P95: {sorted(latencies)[int(len(latencies)*0.95)]}")
print(f"P99: {sorted(latencies)[int(len(latencies)*0.99)]}")

# Error rate
errors = [t for t in traces if t.has_errors]
error_rate = len(errors) / len(traces)

# Service dependency analysis
services_per_trace = [len(t.services()) for t in traces]
print(f"Avg services per request: {sum(services_per_trace)/len(services_per_trace)}")
```

---

<div align="center">

## ✅ Distributed Tracing Guide Complete

**Next:** 
- Try [examples/02_distributed_tracing.py](../examples/02_distributed_tracing.py)
- Or read [LOAD_BALANCER.md](LOAD_BALANCER.md)
- Or check [guides/COMPLETE_GUIDE.md](COMPLETE_GUIDE.md)

</div>
