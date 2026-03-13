# 🏭 Component Wrapper Factory Guide

> **Deep dive into the Component Wrapper Factory component**

**Version:** 1.0 | **Time to Read**: 30 minutes | **Status:** ✅ Complete

---

## 📌 Quick Summary

**What It Does:** Intelligently caches and wraps components for reuse

**How Fast:** 50-100x faster for cached components (< 1ms vs. 100ms+)

**Use When:** Component creation is expensive or repeated

---

## 🎯 Core Concepts

### The Basic Idea

```
Without Wrapper:
Request 1 → Create Component → Execute → Response
Request 2 → Create Component → Execute → Response
Request 3 → Create Component → Execute → Response
Result: 3×100ms = 300ms latency

With Wrapper:
Request 1 → Create Component (100ms) → Cache → Execute → Response
Request 2 → Get from cache (1ms) → Execute → Response
Request 3 → Get from cache (1ms) → Execute → Response
Result: 100ms + 1ms + 1ms = 102ms latency (3x better!)
```

### Caching Benefits

1. **Speed** - 50-100x faster cached access
2. **Resource Efficiency** - Fewer component instantiations
3. **Consistency** - Same component instance across requests
4. **Metrics** - Automatic performance tracking

---

## 💻 Basic Usage

### Installation & Setup

```python
from component_wrapper_factory import ComponentWrapperFactory

# Create wrapper instance
wrapper = ComponentWrapperFactory(
    cache_enabled=True,      # Enable caching
    cache_ttl=300,          # 5 minute TTL
    max_cache_size=1000,    # 1000 max components
    monitor_enabled=True    # Track metrics
)
```

### Getting Components

```python
# Get wrapped component (auto-discovered)
processor = wrapper.get_component('data_processor')

# Use it
result = processor.execute(input_data)

# On next call, it's cached!
processor2 = wrapper.get_component('data_processor')  # < 1ms!
```

### Clearing Cache

```python
# Clear specific component
wrapper.clear_cache('data_processor')

# Clear all components
wrapper.clear_cache()
```

---

## 🔍 Advanced Features

### Component Discovery

```python
# Discover all available components
available = wrapper.discover_components()
print(available)
# Output: ['ml_model', 'nlp_service', 'cache_service']

# Get component metadata
metadata = wrapper.get_component('ml_model').metadata
print(metadata)
# {
#   'name': 'ml_model',
#   'version': '1.0.0',
#   'capabilities': ['predict', 'train'],
#   'resource_limits': {'memory': '512MB'}
# }
```

### Performance Metrics

```python
# Get metrics for specific component
metrics = wrapper.get_metrics('ml_model')
print(metrics)
# {
#   'cache_hits': 1523,
#   'cache_misses': 47,
#   'total_calls': 1570,
#   'cache_hit_ratio': 0.97,
#   'avg_cache_hit_time': 0.8,  # milliseconds
#   'last_accessed': '2024-03-13 14:32:10'
# }

# Get all metrics
all_metrics = wrapper.get_metrics()
```

### Cache Configuration

```python
# Adjust cache settings
wrapper = ComponentWrapperFactory(
    cache_ttl=600,         # Longer TTL (10 min)
    max_cache_size=2000,   # Larger cache
)

# Dynamic adjustment (if supported)
wrapper.set_cache_ttl('ml_model', 1800)  # 30 min for this one
```

---

## 📚 Real-World Examples

### Example 1: ML Model Caching

```python
import time

# Create wrapper
w wrapper = ComponentWrapperFactory()

# First request (cache miss)
start = time.time()
model = wrapper.get_component('nlp_model')
elapsed = time.time() - start
print(f"First call: {elapsed*1000:.1f}ms")  # ~100ms

# Result: First request is slow (component creation)
```

Later requests:

```python
# Requests 2-100 (cache hits)
for i in range(100):
    start = time.time()
    model = wrapper.get_component('nlp_model')
    elapsed = time.time() - start
    if i % 20 == 0:
        print(f"Request {i+2}: {elapsed*1000:.2f}ms")  # ~0.8ms

# Result: Subsequent requests are fast (cache hit)
#Metrics show 99% hit ratio
```

### Example 2: Database Connection Caching

```python
# Setup
wrapper = ComponentWrapperFactory(
    cache_ttl=1800  # 30 minutes
)

# Get database connection (cached)
db = wrapper.get_component('postgres_connection')

# Use for first query
result = db.query("SELECT * FROM users")

# Get same connection (cached) for second query
db2 = wrapper.get_component('postgres_connection')  # Returns same instance!
assert db is db2  # Same object!

result2 = db2.query("SELECT * FROM orders")

# Benefits:
# - Connection pool reuse
# - Eliminates handshake overhead
# - Consistent session
```

### Example 3: Service Configuration Caching

```python
# Setup
wrapper = ComponentWrapperFactory()

# Get configuration (parsed and cached)
config = wrapper.get_component('app_config')
print(config.database_url)

# Get again - returns cached parsed config
config2 = wrapper.get_component('app_config')  # < 1ms!
print(config2.database_url)  # Same parsed config

# Benefits:
# - Parse YAML/JSON once
# - Reuse across requests
# - Avoid parsing overhead
# - Consistent configuration
```

---

## 🔧 Troubleshooting

### Low Cache Hit Ratio

```python
# Check status
metrics = wrapper.get_metrics()
hit_ratio = metrics['cache_hit_ratio']

if hit_ratio < 0.70:
    # Problem: Ratio below 70%
    
    # Cause 1: TTL too short
    # Solution: Increase TTL
    wrapper = ComponentWrapperFactory(cache_ttl=600)  # 10 min
    
    # Cause 2: Cache size too small (evictions)
    # Solution: Increase cache size
    wrapper = ComponentWrapperFactory(max_cache_size=2000)
    
    # Cause 3: Different component instances each time
    # Solution: Use same component ID consistently
```

### High Memory Usage

```python
# Monitor memory
metrics = wrapper.get_metrics()
cached_components = metrics['cached_components']

if memory_usage > acceptable_threshold:
    # Option 1: Reduce cache size
    wrapper.max_cache_size = 500  # Fewer components cached
    
    # Option 2: Reduce TTL
    wrapper.cache_ttl = 120  # Expire faster
    
    # Option 3: Manual cleanup
    wrapper.clear_cache()
    
    # Option 4: Check component sizes
    for component_type in wrapper.discover_components():
        comp = wrapper.get_component(component_type)
        size = sys.getsizeof(comp)
        if size > 10MB:
            print(f"Large component: {component_type} - {size/1024/1024:.1f}MB")
```

---

## ✅ Best Practices

### 1. Choose Appropriate TTL

```python
# ✅ Good - balanced TTL
wrapper = ComponentWrapperFactory(cache_ttl=300)  # 5 min

# ❌ Too short - no benefit
wrapper = ComponentWrapperFactory(cache_ttl=5)  # Components expire instantly

# ❌ Too long - stale data
wrapper = ComponentWrapperFactory(cache_ttl=86400)  # 24 hours - risky!
```

### 2. Monitor Cache Hit Ratio

```python
def check_cache_health():
    metrics = wrapper.get_metrics()
    hit_ratio = metrics['cache_hit_ratio']
    
    if hit_ratio > 0.90:
        return "Excellent"
    elif hit_ratio > 0.75:
        return "Good"
    elif hit_ratio > 0.50:
        return "Acceptable - consider tuning"
    else:
        return "Poor - investigate configuration"

print(check_cache_health())
```

### 3. Right-Size the Cache

```python
# Estimate component size
# Small: DB connections (50-200KB)
# Medium: Config objects (1-10MB)
# Large: ML models (100MB+)

# Calculate needed cache
# Example: 100 medium components
# 100 × 5MB average = 500MB needed

wrapper = ComponentWrapperFactory(max_cache_size=100)
```

### 4. Use Meaningful Component IDs

```python
# ✅ Good - clear naming
component = wrapper.get_component('ml_model_bert_v1')
component = wrapper.get_component('db_postgres_primary')

# ❌ Bad - unclear naming
component = wrapper.get_component('model')
component = wrapper.get_component('db')
# Can't distinguish between multiple databases/models
```

### 5. Handle Cache Invalidation

```python
# When component should be fresh, clear cache
def update_config():
    # Update configuration file
    update_config_file()
    
    # Clear cache so new config loaded
    wrapper.clear_cache('app_config')
    
    # Next access gets fresh config
    config = wrapper.get_component('app_config')

# Or set short TTL for frequently changing items
wrapper = ComponentWrapperFactory()
wrapper.set_cache_ttl('live_config', 60)  # 1 minute
```

---

## 📊 Performance Tuning

### Benchmark Your Setup

```python
import time
import statistics

def benchmark_wrapper(component_type, iterations=1000):
    times = []
    
    # Warm cache
    wrapper.get_component(component_type)
    
    # Test cache hits
    for _ in range(iterations):
        start = time.perf_counter()
        comp = wrapper.get_component(component_type)
        elapsed = (time.perf_counter() - start) * 1000
        times.append(elapsed)
    
    return {
        'mean': statistics.mean(times),
        'median': statistics.median(times),
        'min': min(times),
        'max': max(times),
        'p99': sorted(times)[int(len(times)*0.99)]
    }

result = benchmark_wrapper('ml_model')
print(f"Mean: {result['mean']:.2f}ms | P99: {result['p99']:.2f}ms")
```

### Optimization Checklist

- [ ] Cache hit ratio > 85%
- [ ] Typical cache hit < 2ms
- [ ] Memory usage acceptable
- [ ] TTL appropriate for component
- [ ] Component sizes reasonable
- [ ] No unnecessary clearances
- [ ] Metrics being monitored

---

<div align="center">

## ✅ Component Wrapper Guide Complete

**Next:** 
- Try [examples/01_basic_wrapping.py](../examples/01_basic_wrapping.py)
- Or read [DISTRIBUTED_TRACING.md](DISTRIBUTED_TRACING.md)
- Or check [guides/COMPLETE_GUIDE.md](COMPLETE_GUIDE.md)

</div>
