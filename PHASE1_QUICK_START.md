# Phase 1 Quick Start Guide

## What's New?

Phase 1 implements a complete infrastructure foundation with 7 critical systems enabling:
- ✅ Real-time health monitoring
- ✅ Centralized metrics collection
- ✅ Resource management and quotas
- ✅ Priority-based task scheduling
- ✅ Intelligent caching
- ✅ Automatic error recovery
- ✅ Unified orchestration

## 5-Minute Setup

### Step 1: Import and Initialize

```python
from system_orchestrator import startup_system, shutdown_system
from task_queue import TaskPriority

# Start system with default config
orchestrator = startup_system()
```

### Step 2: Register Components

```python
# Register your components
orchestrator.register_component(
    "knowledge_base",
    kb_instance,
    component_type="core",
    resource_config={
        "max_memory_mb": 500,
        "max_connections": 10
    }
)
```

### Step 3: Use Built-in Features

```python
# Record metrics
orchestrator.record_metric(
    "knowledge_base",
    "operation_time",
    245.5,  # milliseconds
    tags={"operation": "search"}
)

# Execute task asynchronously
task_id = orchestrator.execute_task(
    expensive_function,
    name="Process batch",
    priority=TaskPriority.HIGH
)

# Get system status
status = orchestrator.get_system_status()
print(status)
```

### Step 4: Shutdown Gracefully

```python
shutdown_system()
```

---

## Common Patterns

### Pattern 1: Health Check Custom Logic

```python
from health_checker import get_health_checker

hc = get_health_checker()

# Define custom health check
def check_kb_health():
    stats = kb.get_statistics()
    return stats['document_count'] > 100

# Register with custom check
hc.register_component(
    "knowledge_base",
    kb_instance,
    check_function=check_kb_health
)

hc.start()
```

### Pattern 2: Fallback Chain for Resilience

```python
from error_recovery import get_error_recovery_manager

erm = get_error_recovery_manager()

# Register fallback chain
erm.register_fallback_chain(
    "search_operation",
    primary=kb.semantic_search,
    fallbacks=[
        (kb.keyword_search, "Keyword Search"),
        (kb.cached_search, "Cached Results")
    ],
    default_value=[]
)

# Execute with automatic recovery
result = erm.execute_with_recovery(
    "knowledge_base",
    "search_operation",
    kb.semantic_search,
    query
)
```

### Pattern 3: Caching with TTL

```python
from advanced_cache import get_cache

cache = get_cache()

# Cache with 1-hour TTL
cache.set(
    "user_preferences_123",
    user_prefs_data,
    ttl_seconds=3600,
    namespace="users"
)

# Retrieve from cache
cached_prefs = cache.get("user_preferences_123", namespace="users")
if cached_prefs:
    print(f"Cache hit! Stats: {cache.get_stats()}")
```

### Pattern 4: Task Queue with Priority

```python
from task_queue import get_task_queue, TaskPriority

tq = get_task_queue(max_workers=4)

# High-priority task
high_task_id = tq.enqueue(
    urgent_computation,
    name="Urgent Analysis",
    priority=TaskPriority.HIGH,
    timeout_seconds=30,
    max_retries=3
)

# Background task
bg_task_id = tq.enqueue(
    cleanup_operation,
    name="Cleanup",
    priority=TaskPriority.BACKGROUND
)

# Monitor progress
print(tq.get_queue_stats())
```

### Pattern 5: Resource Quota Management

```python
from resource_manager import get_resource_manager

rm = get_resource_manager()

# Register memory quota
rm.register_component(
    "ml_model",
    max_memory_mb=1000,
    max_connections=5
)

# Allocate memory
if rm.allocate_memory("ml_model", 500):
    # Load model with 500MB
    model = load_large_model()
    # ... use model ...
    rm.release_memory("ml_model", 500)
else:
    print("Memory quota exceeded!")
```

### Pattern 6: Metrics Collection and Analysis

```python
from metrics_collector import get_metrics_collector

mc = get_metrics_collector()

# Record various metrics
for i in range(100):
    operation_time = run_operation()
    mc.record("model_inference", "operation_time", operation_time)

# Get statistics
stats = mc.get_stats("model_inference", "operation_time")
print(f"Average: {stats.mean}ms")
print(f"p95: {stats.p95}ms")
print(f"p99: {stats.p99}ms")

# Get trends for visualization
trend = mc.get_trend("model_inference", "operation_time")
```

---

## Monitoring Dashboard

Get a complete system snapshot:

```python
status = orchestrator.get_system_status()

# Available information:
print(f"Running: {status['running']}")
print(f"Uptime: {status['uptime_seconds']}s")

# Component health
health = status['components']['health']
print(f"Overall state: {health['overall_state']}")
print(f"Healthy components: {health['healthy_count']}")
print(f"Alerts: {health['active_alerts']}")

# Resource usage
resources = status['components']['resources']
quotas = resources['quotas']
print(f"Memory utilization: {quotas['knowledge_base']['memory_mb']}")

# Queue status
queue = status['queue']
print(f"Pending tasks: {queue['pending']}")
print(f"Completed: {queue['completed']}")

# Cache performance
cache = status['cache']
print(f"Hit rate: {cache['hit_rate_percent']}%")
```

---

## Troubleshooting

### Issue: Component marked as unhealthy

**Cause**: Health check failed 3+ consecutive times

**Solution**:
```python
# Check health details
health = hc.get_component_health("component_name")
print(f"State: {health.state}")
print(f"Last error: {health.last_error}")

# Check alerts
alerts = hc.get_alerts()
for alert in alerts:
    if alert['component'] == 'component_name':
        print(f"Alert: {alert['message']}")
```

### Issue: Tasks not executing

**Cause**: Task queue at max workers or priority queue blocked

**Solution**:
```python
stats = tq.get_queue_stats()
print(f"Pending: {stats['pending']}")
print(f"Workers active: {stats['workers_active']}")
print(f"Max workers: {stats['max_workers']}")

# Increase workers if needed
tq.max_workers = 8
```

### Issue: Memory quota exceeded

**Cause**: Component using more memory than allocated

**Solution**:
```python
# Check quota violations
violations = rm.check_quotas()
for component, issues in violations.items():
    for issue in issues:
        print(f"{component}: {issue}")

# Increase quota
rm.register_component(
    "memory_intensive_component",
    max_memory_mb=2000  # Increased from 500
)
```

### Issue: Cache hit rate low

**Cause**: TTL too short or cache key misses

**Solution**:
```python
stats = cache.get_stats()
print(f"Hit rate: {stats['hit_rate_percent']}%")

# Check which keys are accessed
entry = cache.get_entry_info("key_name")
print(f"Hit count: {entry['hit_count']}")

# Adjust TTL for frequently accessed items
cache.set("key_name", value, ttl_seconds=7200)  # 2 hours instead of 1
```

---

## Performance Tips

### 1. Use Namespaces for Cache Organization

```python
cache.set("config_1", data1, namespace="config")
cache.set("user_123", data2, namespace="users")
cache.set("result_456", data3, namespace="results")

# Clear only specific namespace
cache.clear(namespace="results")
```

### 2. Set Appropriate TTLs

```python
# Static data: longer TTL
cache.set("system_config", config, ttl_seconds=86400)  # 24 hours

# Dynamic data: shorter TTL
cache.set("user_session", session, ttl_seconds=3600)  # 1 hour

# Temporary data: very short TTL
cache.set("request_cache", data, ttl_seconds=60)  # 1 minute
```

### 3. Batch Task Submission

```python
# Instead of submitting one task at a time
for item in items:
    task_id = tq.enqueue(process_item, item)

# Submit as single batch task
task_id = tq.enqueue(
    process_batch,
    items,
    name="Batch processing"
)
```

### 4. Use Priority for SLA Compliance

```python
# Critical user request: HIGH priority
response = tq.enqueue(
    handle_request,
    user_request,
    priority=TaskPriority.HIGH
)

# Background maintenance: LOW priority
tq.enqueue(
    perform_maintenance,
    priority=TaskPriority.LOW
)
```

### 5. Monitor Resource Quotas

```python
# Regular health checks
violations = rm.check_quotas()
if violations:
    # Either increase quotas or reduce load
    for component, issues in violations.items():
        logger.warning(f"Resource warning: {component} - {issues}")
```

---

## Best Practices

✅ **DO**: Use namespaces to organize cache entries
✅ **DO**: Set reasonable TTLs based on data freshness needs
✅ **DO**: Register components with realistic resource quotas
✅ **DO**: Use high priority only for critical operations
✅ **DO**: Monitor health status regularly

❌ **DON'T**: Set TTL to 0 (no caching)
❌ **DON'T**: Use CRITICAL priority for routine operations
❌ **DON'T**: Ignore resource quota violations
❌ **DON'T**: Submit unlimited tasks without backpressure
❌ **DON'T**: Skip error handling for critical operations

---

## API Reference

### System Orchestrator
```python
orchestrator.startup(config_dict)
orchestrator.shutdown()
orchestrator.register_component(name, instance, component_type, resource_config, depends_on)
orchestrator.get_system_status()
orchestrator.record_metric(component, metric_type, value, tags)
orchestrator.execute_task(fn, name, priority, timeout_seconds, *args, **kwargs)
```

### Health Checker
```python
hc.register_component(name, instance, check_function, recovery_function)
hc.start()
hc.stop()
hc.get_component_health(component_name)
hc.get_system_health()
hc.get_alerts(include_resolved)
```

### Metrics Collector
```python
mc.record(component, metric_type, value, tags)
mc.register_alert(component, metric_type, threshold, condition)
mc.get_stats(component, metric_type, time_window_hours)
mc.get_all_stats(time_window_hours)
mc.get_trend(component, metric_type, bucket_size_minutes, num_buckets)
```

### Task Queue
```python
tq.enqueue(fn, name, priority, *args, timeout_seconds, max_retries, depends_on, tags, **kwargs)
tq.get_task_status(task_id)
tq.get_queue_stats()
tq.clear_completed_tasks(keep_hours)
```

### Advanced Cache
```python
cache.get(key, namespace)
cache.set(key, value, ttl_seconds, namespace)
cache.delete(key, namespace)
cache.clear(namespace)
cache.warm_cache(data, namespace, ttl_seconds)
cache.get_stats()
```

### Resource Manager
```python
rm.register_component(name, max_memory_mb, max_cpu_percent, max_connections)
rm.allocate_memory(component_name, size_mb)
rm.release_memory(component_name, size_mb)
rm.check_quotas()
rm.get_system_resources()
rm.get_quota_status()
```

---

## Next Steps

1. **Instrument Existing Components**: Use patterns above to add Phase 1 features
2. **Create Monitoring Dashboard**: Visualize system status using orchestrator APIs
3. **Set Up Alerting**: Define critical thresholds and alert handlers
4. **Plan Phase 2**: Prepare for advanced orchestration features
5. **Document Custom Patterns**: Create team-specific usage patterns

For detailed documentation, see:
- `PHASE1_FOUNDATION_COMPLETE.md` - Complete Feature Overview
- `PHASE2_ADVANCED_ORCHESTRATION.md` - Next Phase Planning
