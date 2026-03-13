# 🐛 Phase 2 Troubleshooting Guide

> **Solutions to common Phase 2 problems**

**Version:** 1.0 | **Last Updated:** March 13, 2026 | **Status:** ✅ Complete

---

## 📋 Quick Reference

| Problem | Solution | Time |
|---------|----------|------|
| Cache not working | Check hit ratio metrics | 2 min |
| High memory usage | Reduce cache size | 3 min |
| Traces missing | Complete trace.complete() | 2 min |
| No healthy services | Update health status | 3 min |
| Slow performance | Check wrapper metrics | 5 min |

---

## 🔍 Component Wrapper Issues

### Issue: "ComponentNotFoundError: Component 'X' not found"

**Symptoms:**
- Error when calling `wrapper.get_component('X')`
- Component should exist but can't be found
- Works sometimes, fails other times

**Causes:**
- Component not in discovery path
- Component file not properly named
- Discovery path misconfigured

**Solutions:**

```python
# 1. Check discovered components
components = wrapper.discover_components()
print("Available components:", components)

# If empty, check path
# 2. Verify discovery path
print("Discovery path:", wrapper.discovery_path)

# 3. Try manual path
wrapper = ComponentWrapperFactory(
    discovery_path='/absolute/path/to/components'
)

# 4. Check component file naming
# Files should be: name.component.py or match pattern
# Example: ml_model.component.py
```

**Prevention:**
- Use consistent naming: `component_name.component.py`
- Ensure path is absolute, not relative
- Run `discover_components()` before production

---

### Issue: "Cache hit ratio is very low (< 0.5)"

**Symptoms:**
- Cache hit ratio shows < 50%
- Performance not improved
- Cache seems ineffective

**Causes:**
- Cache TTL too short
- Cache size too small
- Components constantly changing
- Not accessing same components repeatedly

**Solutions:**

```python
# 1. Check current settings
metrics = wrapper.get_metrics()
print(f"Cache hit ratio: {metrics['cache_hit_ratio']:.1%}")
print(f"Cache hits: {metrics['cache_hits']}")
print(f"Cache misses: {metrics['cache_misses']}")

# 2. Increase TTL
wrapper = ComponentWrapperFactory(
    cache_ttl=600,  # 10 minutes instead of 5
)

# 3. Increase cache size
wrapper = ComponentWrapperFactory(
    max_cache_size=2000,  # More components
)

# 4. Analyze access patterns
def analyze_access():
    # Track which components are accessed most
    # Prioritize caching high-use components
    pass
```

**Prevention:**
- Monitor cache hit ratio regularly
- Adjust TTL based on component lifecycle
- Size cache appropriately for your use case

---

### Issue: "OutOfMemory error with wrapper"

**Symptoms:**
- Memory usage grows rapidly
- OutOfMemory exceptions
- Process crashes

**Causes:**
- Cache size too large
- Component objects too large
- Memory not releasing

**Solutions:**

```python
# 1. Monitor memory usage
metrics = wrapper.get_metrics()
print(f"Cache size: {metrics.get('cache_size_mb', 'unknown')} MB")

# 2. Reduce cache size
wrapper = ComponentWrapperFactory(
    max_cache_size=500,  # Reduce size
    cache_ttl=120        # Reduce TTL
)

# 3. Manual cleanup
wrapper.clear_cache()

# 4. Monitor component sizes
component = wrapper.get_component('large_model')
print(f"Component size: {get_size(component)} MB")

# 5. Use memory profiler
if memory_usage > THRESHOLD:
    wrapper.clear_cache('large_model')
```

**Prevention:**
- Set reasonable `max_cache_size` initially
- Monitor memory usage regularly
- Clear cache periodically if needed

---

### Issue: "Wrapper adds too much latency"

**Symptoms:**
- Expected: < 1ms cache hit latency
- Actual: 5ms+ latency
- Performance not improved as expected

**Causes:**
- Cache design inefficient
- Large components causing overhead
- Other bottlenecks masking wrapper benefits

**Solutions:**

```python
# 1. Profile wrapper performance
span = trace.create_span('wrapper_get')
component = wrapper.get_component('X')
span.add_attribute('duration_ms', span.duration_ms)

# 2. Check cache lookup speed
if latency > 5:  # Expected < 1ms
    # Problem might be elsewhere
    # Check component discovery time
    
# 3. Optimize component size
# Smaller components = faster caching
# Consider lazy loading

# 4. Use different cache backend
# Current: in-memory
# Consider: shared cache across instances
```

**Prevention:**
- Measure baseline latency without wrapper
- Profile cache operations specifically
- Keep components reasonably sized

---

## 📊 Distributed Tracing Issues

### Issue: "TraceNotFoundError: Trace 'X' not found"

**Symptoms:**
- Can'tretrieve trace by ID
- `tracing.get_trace(trace_id)` returns None
- Trace should exist but can't find it

**Causes:**
- Trace not completed
- Trace TTL expired
- Trace ID misspelled/wrong
- Storage backend issue

**Solutions:**

```python
# 1. Ensure trace.complete() called
trace = tracing.start_trace(req_id, 'service')
try:
    # ... do work ...
finally:
    trace.complete()  # MUST call this

# 2. Check if trace still in retention window
# Traces older than retention_hours are deleted
retention_hours = 24

# 3. Store trace ID correctly
trace_id = trace.id
print(f"Trace ID: {trace_id}")  # Verify format

# 4. Check storage backend
backend = tracing.storage_backend
print(f"Backend: {backend}")

# 5. Check if maximum traces exceeded
if tracing.get_total_traces() > max_traces:
    print("Trace storage full - old traces deleted")
```

**Prevention:**
- Always call `trace.complete()` in finally block
- Store trace IDs for lookup
- Monitor retention period for your needs

---

### Issue: "Spans not recording in trace"

**Symptoms:**
- Trace exists but spans are empty
- `trace.create_span()` doesn't record
- Span data lost

**Causes:**
- Span not ended properly
- Exception preventing flush
- Trace completed before spansended

**Solutions:**

```python
# 1. Ensure spans are ended
span = trace.create_span('operation')
try:
    # ... do work ...
finally:
    span.end(status='success')  # Don't forget!

# 2. Complete trace after spans
trace = tracing.start_trace(req_id, 'service')
spans = []
for item in items:
    span = trace.create_span('process_item')
    # ... do work ...
    span.end(status='success')

trace.complete()  # After all spans done

# 3. Check span status
span.end(
    status='success',  # 'success', 'failure', 'timeout'
    error=str(exception) if failed else None
)
```

**Prevention:**
- Use try/finally to ensure span.end() called
- Always complete trace after all spans
- Test tracing with simple examples first

---

### Issue: "High overhead from tracing (> 5% latency)"

**Symptoms:**
- Tracing adds > 5% latency
- Performance worse than expected
- Trace operations slow

**Symptoms:**
- Trace creation expensive
- Too many span operations
- Storage backend slow

**Solutions:**

```python
# 1. Reduce span granularity
# DON'T do this (too many spans)
for item in items:
    span = trace.create_span('process_item')
    span.end()

# DO this instead
span = trace.create_span('process_items')
for item in items:
    # Process without span
    pass
span.end()

# 2. Use sampling for high-traffic services
if needs_tracing():  # e.g., 1% sampling
    trace = tracing.start_trace(req_id, 'service')
else:
    trace = NULL_TRACE  # No-op trace

# 3. Async trace storage
# Use background thread/queue for writing
# Reduces blocking latency

# 4. Measure actual overhead
with timer() as t:
    trace = tracing.start_trace(req_id, 'service')
    trace.complete()
    overhead = t.elapsed_ms
```

**Prevention:**
- Use reasonable span granularity
- Measure actual overhead not assumptions
- Consider sampling for high-traffic services

---

## ⚖️ Load Balancer Issues

### Issue: "NoHealthyServiceError: No healthy services"

**Symptoms:**
- Error when selecting service
- All services marked unhealthy
- Can't route requests

**Causes:**
- All services down
- Health checks failing
- Services not registered

**Solutions:**

```python
# 1. Check registered services
services = lb.get_services()
print(f"Registered services: {len(services)}")
for service in services:
    print(f"  {service.id}: {service.healthy}")

# 2. Manually mark as healthy
lb.update_service_metrics(
    'service_1',
    healthy=True,
    load=0.5
)

# 3. Check health check logic
# Ensure health check is working
response = check_service_health('service_1')
if response.ok:
    lb.update_service_metrics('service_1', healthy=True)

# 4. Register more services
# If all are down, may need to start backups
lb.register_service('backup_service', '127.0.0.1', 8010)
```

**Prevention:**
- Have health checks working before deploying
- Register multiple service instances
- Monitor service health continuously

---

### Issue: "Always routes to same service"

**Symptoms:**
- Load not distributed
- Always selects same service
- Other services ignored

**Causes:**
- Other services marked unhealthy
- Routing strategy misconfigured
- Load metrics not updated

**Solutions:**

```python
# 1. Check service health status
services = lb.get_services()
for service in services:
    print(f"{service.id}: health={service.healthy}")

# 2. Mark services healthy
for service in services:
    lb.update_service_metrics(
        service.id,
        healthy=True,
        load=0.5
    )

# 3. Check routing strategy
print(f"Strategy: {lb.strategy}")
if lb.strategy != 'least_loaded':
    lb.strategy = 'least_loaded'

# 4. Update load metrics regularly
load_1 = get_service_load('service_1')
load_2 = get_service_load('service_2')
lb.update_service_metrics('service_1', load=load_1, healthy=True)
lb.update_service_metrics('service_2', load=load_2, healthy=True)
```

**Prevention:**
- Update service metrics on each request
- Use health checks to detect failures
- Monitor routing distribution

---

### Issue: "Load balancer adds latency"

**Symptoms:**
- Expected: < 5ms selection time
- Actual: 10ms+ added latency
- Performance worse than expected

**Causes:**
- Health check latency
- Metric calculation expensive
- Database queries in routing

**Solutions:**

```python
# 1. Profile routing decision
with timer() as t:
    service = lb.select_service(request)
    latency = t.elapsed_ms
    if latency > 10:
        print("Routing too slow")

# 2. Simplify routing logic
# Use simple scoring, not complex logic
score = (1 - load) * health_factor

# 3. Cache routing decisions
# For same request type, use same service
if prev_service and prev_service.healthy:
    use_prev_service()

# 4. Use minimal health checks
# Health check should be very fast
# Just check TCP connection, not full request
```

**Prevention:**
- Keep routing logic simple
- Use fast health checks (TCP ping)
- Cache routing decisions when possible

---

## 🔧 General Troubleshooting

### Debugging Approach

1. **Identify the symptom** - What's not working?
2. **Check logs** - What errors are reported?
3. **Monitor metrics** - What data shows?
4. **Isolate component** - Which component has the issue?
5. **Reproduce** - Can you make it fail consistently?
6. **Fix** - Apply solution
7. **Verify** - Confirm it's fixed

---

### Enable Detailed Logging

```python
import logging

# Enable trace logging
logging.basicConfig(level=logging.DEBUG)

# Specific component logging
wrapper_logger = logging.getLogger('component_wrapper')
wrapper_logger.setLevel(logging.DEBUG)

trace_logger = logging.getLogger('distributed_tracing')
trace_logger.setLevel(logging.DEBUG)

lb_logger = logging.getLogger('load_balancer')
lb_logger.setLevel(logging.DEBUG)
```

---

### Collect Diagnostic Information

```python
def collect_diagnostics():
    """Gather diagnostic data"""
    diagnostics = {
        'wrapper_metrics': wrapper.get_metrics(),
        'services': lb.get_services(),
        'recent_traces': tracing.get_recent_traces(n=10),
        'errors': collect_error_log(),
    }
    return diagnostics

# Use for debugging
diag = collect_diagnostics()
print(json.dumps(diag, indent=2))
```

---

<div align="center">

## ✅ Troubleshooting Guide Complete

**Still having issues?** Check [FAQ.md](FAQ.md) for more help

</div>
