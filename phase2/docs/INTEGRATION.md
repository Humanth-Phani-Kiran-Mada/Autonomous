# 🔗 Phase 2 Integration Guide

> **How to integrate Phase 2 with Phase 1 and your existing services**

**Version:** 1.0 | **Last Updated:** March 13, 2026 | **Status:** ✅ Complete

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [Architecture Integration](#architecture-integration)
3. [Step-by-Step Integration](#step-by-step-integration)
4. [Code Examples](#code-examples)
5. [Troubleshooting Integration](#troubleshooting-integration)
6. [Best Practices](#best-practices)

---

## 🎯 Overview

Phase 2 components are designed to enhance Phase 1 with minimal changes:

```
PHASE 1 (Existing)           PHASE 2 (New)
├─ Services                  ├─ Load Balancer  (routes to services)
├─ Components                ├─ Wrapper        (caches components)
├─ Logging                   ├─ Tracing        (tracks requests)
└─ Monitoring                └─ Metrics        (enhanced monitoring)
```

### Integration Complexity

- **Component Wrapper:** ✅ Easy (5-10 minutes)
- **Distributed Tracing:** ✅ Easy (10-15 minutes)
- **Load Balancer:** ✅ Moderate (15-30 minutes)
- **All Components:** ✅ Moderate (30-45 minutes)

---

## 🏗️ Architecture Integration

### Before Integration

```
Client
  ↓
[Phase 1 Service]
  ├─ Direct component access
  ├─ Manual tracing (if any)
  ├─ No intelligent routing
  └─ Potential performance issues
```

### After Integration

```
Client
  ↓
[Load Balancer - Phase 2]
  ├─ Intelligent routing
  ├─ Service selection
  └─ Load distribution
  ↓
[Phase 1 Service + Phase 2 Enhancements]
  ├─ Component Wrapper (cached access)
  ├─ Distributed Tracing (visibility)
  ├─ Performance optimization
  └─ Enhanced monitoring
```

---

## 📝 Step-by-Step Integration

### Step 1: Install Phase 2 (5 minutes)

```bash
# Copy Phase 2 to your project
cp -r phase2/ /path/to/your/project/

# Install dependencies (if needed)
pip install -r phase2/requirements.txt
```

---

### Step 2: Integrate Component Wrapper (10 minutes)

#### 2a. Import the wrapper

```python
# In your service code
from phase2.src.component_wrapper_factory import ComponentWrapperFactory

# Create global wrapper instance
wrapper = ComponentWrapperFactory()
```

#### 2b. Replace component access

**Before:**
```python
# Direct component import (slow)
from my_components import get_processor
processor = get_processor()
result = processor.process(data)
```

**After:**
```python
# Use wrapper (fast + cached)
processor = wrapper.get_component('processor')
result = processor.process(data)
```

#### 2c. That's it!

The wrapper handles caching automatically. No other changes needed.

---

### Step 3: Integrate Distributed Tracing (15 minutes)

#### 3a. Import tracing system

```python
from phase2.src.distributed_tracing import DistributedTracingSystem

# Create global tracing instance
tracing = DistributedTracingSystem()
```

#### 3b. Add tracing to request handler

**Before:**
```python
def handle_request(request):
    # No tracing
    result = process(request)
    return result
```

**After:**
```python
def handle_request(request):
    # Add tracing
    trace = tracing.start_trace(
        request.id,
        'my_service',
        metadata={'user_id': request.user_id}
    )
    
    try:
        span = trace.create_span('process_request')
        result = process(request)
        span.end(status='success')
    except Exception as e:
        span = trace.create_span('process_request')
        span.end(status='failure', error=str(e))
        raise
    finally:
        trace.complete()
    
    return result
```

#### 3c. Propagate trace context

For external calls, propagate the trace ID:

```python
def call_other_service(service_url, data, trace_id):
    headers = {
        'X-Trace-ID': trace_id,
        'X-Service-Name': 'my_service'
    }
    response = requests.post(service_url, json=data, headers=headers)
    return response
```

---

### Step 4: Integrate Load Balancer (30 minutes)

#### 4a. Create load balancer

```python
from phase2.src.intelligent_load_balancer import IntelligentLoadBalancer

# Create load balancer
lb = IntelligentLoadBalancer(strategy='least_loaded')

# Register your service instances
lb.register_service('service_1', '127.0.0.1', 8001)
lb.register_service('service_2', '127.0.0.1', 8002)
lb.register_service('service_3', '127.0.0.1', 8003)
```

#### 4b. Add load balancer to request flow

```python
def route_request(request):
    # Select service using load balancer
    service = lb.select_service(request)
    
    # Forward request to selected service
    response = service.handle(request)
    
    # Update metrics
    lb.update_service_metrics(
        service.id,
        load=get_service_load(service.id),
        healthy=True,
        response_time=response.elapsed_ms
    )
    
    return response
```

#### 4c. Implement health checks

```python
def health_check():
    # Called periodically by load balancer
    services = lb.get_services()
    
    for service in services:
        try:
            # Simple health check
            response = requests.get(f'http://{service.address}:{service.port}/health')
            healthy = response.status_code == 200
        except:
            healthy = False
        
        # Update status
        lb.update_service_metrics(service.id, healthy=healthy)
```

---

## 💻 Code Examples

### Example 1: Basic Integration

```python
"""
Minimal integration example
- Component Wrapper for performance
- No tracing or load balancing
- Best for: Single service, not concerned with tracing
"""

from phase2.src.component_wrapper_factory import ComponentWrapperFactory

# Setup
wrapper = ComponentWrapperFactory()

# In your request handler
def handle_request(data):
    # Get cached component
    processor = wrapper.get_component('ml_model')
    
    # Process
    result = processor.predict(data)
    
    return result

# Get metrics (optional)
metrics = wrapper.get_metrics('ml_model')
print(f"Cache hit ratio: {metrics['cache_hit_ratio']:.1%}")
```

---

### Example 2: Integration with Tracing

```python
"""
Integration with tracing
- Component Wrapper for performance
- Distributed Tracing for visibility
- Best for: Multi-service setup, debugging needed
"""

from phase2.src.component_wrapper_factory import ComponentWrapperFactory
from phase2.src.distributed_tracing import DistributedTracingSystem

# Setup
wrapper = ComponentWrapperFactory()
tracing = DistributedTracingSystem()

# In your request handler
def handle_request(request):
    # Start tracing
    trace = tracing.start_trace(request.id, 'api_service')
    
    try:
        # Get cached component
        span1 = trace.create_span('get_component')
        processor = wrapper.get_component('ml_model')
        span1.end(status='success')
        
        # Process data
        span2 = trace.create_span('process_data')
        result = processor.predict(request.data)
        span2.end(status='success')
        
        # Return result
        return result
    
    except Exception as e:
        # Record error
        trace.create_span('error').end(
            status='failure',
            error=str(e)
        )
        raise
    
    finally:
        trace.complete()

# Query trace (for debugging)
trace_data = tracing.get_trace('req_123')
print(f"Total latency: {trace_data.latency_ms}ms")
```

---

### Example 3: Full Integration

```python
"""
Full integration example
- Component Wrapper for performance
- Distributed Tracing for visibility
- Load Balancer for distribution
- Best for: Multi-service production setup
"""

from phase2.src.component_wrapper_factory import ComponentWrapperFactory
from phase2.src.distributed_tracing import DistributedTracingSystem
from phase2.src.intelligent_load_balancer import IntelligentLoadBalancer

# Setup all components
wrapper = ComponentWrapperFactory()
tracing = DistributedTracingSystem()
lb = IntelligentLoadBalancer(strategy='least_loaded')

# Register services
lb.register_service('compute_1', '127.0.0.1', 8001)
lb.register_service('compute_2', '127.0.0.1', 8002)

# Main request handler
def handle_request(request):
    # Load balancer selects service
    span_route = trace.create_span('select_service')
    service = lb.select_service(request)
    span_route.add_attribute('selected_service', service.id)
    span_route.end(status='success')
    
    # Get cached component
    span_component = trace.create_span('get_component')
    processor = wrapper.get_component('ml_model')
    span_component.end(status='success')
    
    # Process request
    span_process = trace.create_span('process_request')
    result = processor.predict(request.data)
    span_process.end(status='success')
    
    return result

# Start tracing for each request
def api_endpoint(request):
    trace = tracing.start_trace(request.id, 'api_service')
    try:
        return handle_request(request)
    finally:
        trace.complete()
```

---

## 🔧 Troubleshooting Integration

### Issue: "ComponentNotFoundError"

**Cause:** Component not discovered

**Solution:**
```python
# Check discovered components
components = wrapper.discover_components()
print(components)

# Manually specify path
wrapper = ComponentWrapperFactory(
    discovery_path='/path/to/components'
)
```

---

### Issue: "NoHealthyServiceError"

**Cause:** No healthy services available

**Solution:**
```python
# Check service status
services = lb.get_services()
for service in services:
    print(f"{service.id}: {service.healthy}")

# Manually update health
lb.update_service_metrics('service_1', healthy=True)
```

---

### Issue: "Traces not appearing"

**Cause:** Trace not completed

**Solution:**
```python
# Ensure complete() is called
trace = tracing.start_trace(request.id, 'service')

try:
    # ... do work ...
finally:
    trace.complete()  # Must call this!
```

---

### Issue:"High memory usage"

**Cause:** Cache too large

**Solution:**
```python
# Reduce cache size
wrapper = ComponentWrapperFactory(
    max_cache_size=500,  # Reduce from default 1000
    cache_ttl=180        # Reduce from default 300
)

# Or manually clear
wrapper.clear_cache()
```

---

## ✅ Best Practices

### 1. Always Complete Traces

```python
# ✅ Good - trace always completed
trace = tracing.start_trace(request.id, 'service')
try:
    # ... do work ...
finally:
    trace.complete()

# ❌ Bad - missing complete() call
trace = tracing.start_trace(request.id, 'service')
# ... do work ...
```

---

### 2. Use Meaningful Span Names

```python
# ✅ Good - descriptive names
span = trace.create_span('database_query_user_profile')
span = trace.create_span('cache_lookup_session')

# ❌ Bad - vague names
span = trace.create_span('operation')
span = trace.create_span('work')
```

---

### 3. Add Relevant Attributes

```python
# ✅ Good - detailed context
span.add_attribute('user_id', user.id)
span.add_attribute('query_time_ms', 42)
span.add_attribute('cacheHit', True)

# ❌ Bad - missing context
span.end(status='success')
```

---

### 4. Handle Errors Properly

```python
# ✅ Good - error recorded
try:
    result = process(data)
    span.end(status='success')
except Exception as e:
    span.end(status='failure', error=str(e))
    raise

# ❌ Bad - error lost
result = process(data)
span.end(status='success')  # Hides failure!
```

---

### 5. Monitor Wrapper Metrics

```python
# ✅ Good - check periodically
metrics = wrapper.get_metrics()
if metrics['cache_hit_ratio'] < 0.8:
    print("Low cache hit ratio - investigate")

# ❌ Bad - ignore metrics
# Never check if caching is working
```

---

### 6. Keep Cache TTL Reasonable

```python
# ✅ Good - appropriate TTL
wrapper = ComponentWrapperFactory(
    cache_ttl=300,  # 5 minutes for typical use
)

# ❌ Bad - too long/short cache
wrapper = ComponentWrapperFactory(
    cache_ttl=3600,  # Too long - stale data
    # or
    cache_ttl=5,     # Too short - no caching benefit
)
```

---

## 📈 Integration Checklist

- [ ] Phase 2 directory copied to project
- [ ] Dependencies installed (if needed)
- [ ] Component Wrapper imported and configured
- [ ] Component access updated to use wrapper
- [ ] Distributed Tracing imported and configured
- [ ] Request handlers updated with trace spans
- [ ] Trace context propagated between services
- [ ] Load Balancer imported and configured
- [ ] Services registered with load balancer
- [ ] Health checks implemented
- [ ] Metrics collection verified
- [ ] Cache hit ratio monitored
- [ ] Error handling verified
- [ ] Performance benchmark run
- [ ] Production deployment tested

---

<div align="center">

## ✅ Integration Complete

**Next Steps:**
1. Run the [integration example](../examples/04_full_integration.py)
2. Check [docs/PERFORMANCE.md](PERFORMANCE.md) for benchmarks
3. Read [docs/TROUBLESHOOTING.md](TROUBLESHOOTING.md) for help
4. Monitor with [docs/FAQ.md](FAQ.md) guidance

</div>
