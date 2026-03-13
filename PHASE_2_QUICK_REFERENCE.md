# Phase 2 Quick Reference Guide

## One-Liner Summary

**Phase 2 = Transparent Component Wrapping + Distributed Tracing + Smart Load Balancing**

## The 3 Core Components

### 1️⃣ Component Wrapper Factory
**What:** Wrap any component to automatically cache, trace, and monitor it
**Where:** `src/component_wrapper_factory.py`
**When:** At component initialization

```python
# SETUP
from src.component_wrapper_factory import get_component_wrapper_factory
factory = get_component_wrapper_factory()

# WRAP
wrapped = factory.wrap_component(my_service, "service_id")

# USE (identical to original)
result = wrapped.method_name()

# METRICS
stats = factory.get_component_metrics("service_id")
print(f"Calls: {stats['call_count']}, Latency: {stats['avg_latency']}ms")
```

**Key Features:**
- ✅ Transparent wrapping (no code changes needed)
- ✅ Automatic caching with TTL
- ✅ Call-level metrics
- ✅ Error tracking
- ✅ Success rate monitoring

---

### 2️⃣ Distributed Tracing System
**What:** Trace requests end-to-end across all components
**Where:** `src/distributed_tracing.py`
**When:** At request entry/exit points

```python
# SETUP
from src.distributed_tracing import get_tracing_system
ts = get_tracing_system()

# START TRACE
trace = ts.start_trace()

# TRACE OPERATIONS
span = ts.start_span("ComponentA", "operation_name")
# ... do work ...
ts.end_span(span.span_id)

# END TRACE
ts.end_trace(trace.trace_id)

# ANALYZE
summary = ts.get_trace_summary(trace.trace_id)
print(f"Duration: {summary['total_duration_ms']}ms")
```

**Key Features:**
- ✅ Parent-child span relationships
- ✅ Critical path calculation
- ✅ Component dependency tracking
- ✅ Timing for all operations
- ✅ Tags and logs for metadata

---

### 3️⃣ Intelligent Load Balancer
**What:** Route requests to best-performing component
**Where:** `src/intelligent_load_balancer.py`
**When:** When selecting component for request

```python
# SETUP
from src.intelligent_load_balancer import get_load_balancer, LoadBalancingStrategy
lb = get_load_balancer(LoadBalancingStrategy.PERFORMANCE_BASED)

# REGISTER COMPONENTS
lb.register_component("comp_a", service_a)
lb.register_component("comp_b", service_b)

# SELECT BEST COMPONENT
selected = lb.get_component()

# DO WORK
latency_start = time.time()
result = selected.process(data)
latency = time.time() - latency_start

# REPORT METRICS
lb.record_request(selected, latency, success=True)

# CHECK STATUS
status = lb.get_component_status("comp_a")
print(f"Health: {status['health']}")
```

**Key Features:**
- ✅ 5 strategies (round-robin, least-connections, weighted, performance, random)
- ✅ Circuit breaker pattern
- ✅ Health monitoring
- ✅ Performance-based scoring
- ✅ Automatic failover

---

## Integration Pattern

```python
# TYPICAL USAGE PATTERN

# 1. INITIALIZE PHASE 2
factory = get_component_wrapper_factory()
ts = get_tracing_system()
lb = get_load_balancer(LoadBalancingStrategy.PERFORMANCE_BASED)

# 2. WRAP COMPONENTS
services = {"auth": auth_svc, "data": data_svc}
wrapped = factory.wrap_batch(services)

# 3. REGISTER WITH LB
lb.register_components_batch(wrapped)

# 4. START TRACE
trace = ts.start_trace()

# 5. SELECT COMPONENT
selected_id = lb.get_component()
selected = wrapped[selected_id]

# 6. TRACE OPERATION
span = ts.start_span(selected_id, "operation")

# 7. EXECUTE
result = selected.method()

# 8. RECORD METRICS (automatic for wrapper)
lb.record_request(selected, latency, success=True)

# 9. END SPAN
ts.end_span(span.span_id)

# 10. END TRACE
ts.end_trace(trace.trace_id)
```

---

## Common Tasks

### Task 1: Wrap a Component
```python
factory.wrap_component(component, "component_id", enable_caching=True)
```

### Task 2: Get Component Metrics
```python
metrics = factory.get_component_metrics("component_id")
# Keys: call_count, error_count, avg_latency, success_rate, cache_hits, etc.
```

### Task 3: Trace an Operation
```python
span = ts.start_span("ComponentName", "operation_name")
# ... do operation ...
ts.end_span(span.span_id)
```

### Task 4: Check Component Health
```python
status = lb.get_component_status("component_id")
print(status["health"])  # healthy/degraded/unhealthy/circuit_open
```

### Task 5: Change Load Balancing Strategy
```python
lb.strategy = LoadBalancingStrategy.WEIGHTED_ROUND_ROBIN
lb.weights["fast_component"] = 2.0
```

### Task 6: Clear Cache
```python
factory.clear_all_caches()
```

### Task 7: Print System Status
```python
factory.print_summary()
ts.print_trace(trace_id)
lb.print_status()
```

---

## Singleton Instances (Global)

All Phase 2 components are singletons accessible globally:

```python
# Component Wrapper Factory
from src.component_wrapper_factory import component_wrapper_factory

# Distributed Tracing System
from src.distributed_tracing import distributed_tracing_system

# Load Balancer
from src.intelligent_load_balancer import intelligent_load_balancer
```

Or via getter functions:

```python
from src.component_wrapper_factory import get_component_wrapper_factory
from src.distributed_tracing import get_tracing_system
from src.intelligent_load_balancer import get_load_balancer

factory = get_component_wrapper_factory()
ts = get_tracing_system()
lb = get_load_balancer()
```

---

## Key Metrics

### Component Metrics
```python
{
    "call_count": int,
    "error_count": int,
    "avg_latency": float,
    "min_latency": float,
    "max_latency": float,
    "success_rate": float,  # 0.0-1.0
    "cache_hits": int,
    "cache_misses": int,
    "cache_hit_rate": float,
}
```

### Trace Summary
```python
{
    "trace_id": str,
    "total_duration_ms": float,
    "critical_path_ms": float,
    "span_count": int,
    "components_involved": list,
}
```

### Load Balancer Stats
```python
{
    "total_requests": int,
    "successful_requests": int,
    "success_rate": float,
    "avg_latency": float,
    "p95_latency": float,
    "p99_latency": float,
}
```

---

## Error Handling

### Circuit Breaker Open
```python
# When too many failures occurred
# Solution: Wait for half_open state, or check logs
status = lb.get_component_status("comp_id")
if status["health"] == "circuit_open":
    print("Component failing, route to backup")
```

### Trace Growing Too Large
```python
# When too many spans
# Solution: Clean up old traces
ts.cleanup_old_traces(keep_count=100)
```

### High Cache Memory
```python
# When cache using too much memory
# Solution: Reduce TTL or disable caching
wrapped = factory.wrap_component(comp, "id", cache_ttl_seconds=60)
```

---

## Performance Tips

1. **Cache Wisely** - Only cache read-only operations
2. **Cleanup Traces** - Don't keep traces forever
3. **Span Efficiently** - Don't create trace per operation
4. **Choose Strategy** - PERFORMANCE_BASED works best
5. **Monitor Overhead** - <2ms wrapper overhead acceptable

---

## Testing Phase 2

### Run Full Demo
```bash
python src/run_phase2_demo.py
# Choose "all" to run all 4 demonstrations
```

### Run Specific Demo
```bash
python src/run_phase2_demo.py
# Enter: 1 (component wrapper)
# Or: 2 (distributed tracing)
# Or: 3 (load balancing)
# Or: 4 (integrated system)
```

---

## Load Balancing Strategies Comparison

| Strategy | Best For | Complexity |
|----------|----------|-----------|
| ROUND_ROBIN | Simple, fair distribution | Low |
| LEAST_CONNECTIONS | Connection-heavy services | Low |
| WEIGHTED_ROUND_ROBIN | Heterogeneous hardware | Low |
| PERFORMANCE_BASED | Optimal distribution | High |
| RANDOM | Testing, simple fallback | Low |

**Recommendation:** Start with PERFORMANCE_BASED

---

## Common Integration Patterns

### Pattern 1: Simple Wrapping
```python
factory.wrap_component(my_service, "my_service")
# That's it! Now it's cached and monitored
```

### Pattern 2: Full Tracing
```python
trace = ts.start_trace()
span = ts.start_span("ServiceA", "process")
# ... do work ...
ts.end_span(span.span_id)
ts.end_trace(trace.trace_id)
```

### Pattern 3: Load Balanced
```python
lb.register_components_batch(services)
component = lb.get_component()
result = component.process(data)
lb.record_request(component, latency, success=True)
```

### Pattern 4: All Together
```python
# Wrap, then load balance with tracing
trace = ts.start_trace()
span = ts.start_span("System", "request")
component = lb.get_component()
result = wrapped[component].process()
lb.record_request(component, latency, True)
ts.end_span(span.span_id)
ts.end_trace(trace.trace_id)
```

---

## Debugging

### Inspect Metrics
```python
metrics = factory.get_all_metrics()
for comp_id, data in metrics.items():
    print(f"{comp_id}: {data['success_rate']:.1%} success")
```

### View Trace Tree
```python
ts.print_trace(trace_id, max_depth=5)
```

### Check LB Status
```python
lb.print_status()
```

### Get Slowest Spans
```python
slowest = ts.get_slowest_spans(trace_id, count=10)
for s in slowest:
    print(f"{s['component']}.{s['operation']}: {s['duration_ms']}ms")
```

---

## Files Reference

| File | Purpose | Lines |
|------|---------|-------|
| component_wrapper_factory.py | Wrapping & caching | 400 |
| distributed_tracing.py | Request tracing | 500 |
| intelligent_load_balancer.py | Smart routing | 550 |
| run_phase2_demo.py | Demonstrations | 400 |

**Total Phase 2:** ~1,850 lines

---

## Quick Start (2 Minutes)

```python
# 1. Import
from src.component_wrapper_factory import get_component_wrapper_factory
from src.distributed_tracing import get_tracing_system
from src.intelligent_load_balancer import get_load_balancer

# 2. Initialize
factory = get_component_wrapper_factory()
ts = get_tracing_system()
lb = get_load_balancer()

# 3. Wrap
wrapped_svc = factory.wrap_component(my_service, "svc")

# 4. Register
lb.register_component("svc", wrapped_svc)

# 5. Trace
trace = ts.start_trace()
span = ts.start_span("svc", "work")

# 6. Route & Execute
result = wrapped_svc.do_work()

# 7. Finish
ts.end_span(span.span_id)
ts.end_trace(trace.trace_id)

# 8. Check metrics
print(factory.get_component_metrics("svc"))
```

That's it! You now have:
- ✅ Wrapped service with caching/metrics
- ✅ Load balancing
- ✅ Complete request tracing

---

## Next Steps

1. **Run Demo:** `python src/run_phase2_demo.py`
2. **Review Code:** Check PHASE_2_GUIDE.md for details
3. **Integrate:** Follow PHASE_2_INTEGRATION.md for Phase 1 integration
4. **Monitor:** Use metrics to optimize your system

---

## Support Index

- **Component Reference:** See PHASE_2_GUIDE.md
- **Integration Guide:** See PHASE_2_INTEGRATION.md
- **Implementation Roadmap:** See PHASE_2_ROADMAP.md
- **Working Examples:** See run_phase2_demo.py
- **Code Location:** See `src/` directory

---

✅ **Phase 2 Status: COMPLETE**

Ready to transform your system with middleware magic! 🚀
