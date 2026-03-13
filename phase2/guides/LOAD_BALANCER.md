# ⚖️ Intelligent Load Balancer Guide

> **Deep dive into the Intelligent Load Balancer component**

**Version:** 1.0 | **Time to Read**: 30 minutes | **Status:** ✅ Complete

---

## 📌 Quick Summary

**What It Does:** Intelligently routes requests across service instances

**Result:** Better performance, reliability, and resource utilization

**Use When:** Multiple instances of a service, need smart request distribution

---

## 🎯 Core Concepts

### The Basic Idea

Simple request distribution (Round-Robin):
```
Requests: A → B → C → A → B → C
Service 1: ▁▁▁
Service 2: ▁▁▁
Service 3: ▁▁▁
```

Intelligent distribution (Least-Loaded):
```
Requests: A → A → B → C → B → C
Service 1: ▃▃▁ (busy, fewer requests)
Service 2: ▁▂▂ (normal load)
Service 3: ▁▁▂ (light load)
```

**Problem:** How do you distribute requests to maximize performance?

**Issues with simple approaches:**
- Round-Robin: Doesn't account for actual server load
- Random: Unpredictable performance
- Least-Connections: Might send long requests to slow servers

**Solution:** Intelligent Load Balancer

```
Request 1 (light) → Service C (light)
Request 2 (light) → Service B (light)
Request 3 (heavy) → Service A (idle)
Request 4 (medium) → Service B (recovering)
```

---

## 💻 Basic Usage

### Setup Load Balancer

```python
from intelligent_load_balancer import IntelligentLoadBalancer

# Create load balancer
lb = IntelligentLoadBalancer()
```

### Register Services

```python
# Register instances
lb.register_service('service_a', 'host1:8000')
lb.register_service('service_b', 'host2:8000')
lb.register_service('service_c', 'host3:8000')
```

### Select Service for Request

```python
# Get next service
selected = lb.select_service(
    strategy='least_loaded',  # See strategies below
    current_load={'cpu': 45, 'memory': 60}
)

# Use selected service
response = requests.post(f'http://{selected}', json=data)
```

### Update Service Metrics

```python
# After request, update metrics
lb.update_service_metrics(
    'host1:8000',
    metrics={
        'response_time_ms': 45,
        'cpu_percent': 55,
        'memory_percent': 70,
        'error_rate': 0.01,  # 1% errors
        'active_connections': 23
    }
)
```

---

## 🔍 Routing Strategies

### Strategy 1: Round-Robin (Simple)

```python
strategy = 'round_robin'

# Returns services in rotation: A → B → C → A → B → C
# Best: Simple, fair distribution
# Worst: Ignores actual load
```

**Example:**
```
Request 1 → Service A
Request 2 → Service B
Request 3 → Service C
Request 4 → Service A  (cycle repeats)
```

---

### Strategy 2: Least-Loaded (Smart)

```python
strategy = 'least_loaded'

# Returns service with lowest current load
# Best: Actual load-aware distribution
# Worst: Rapid load changes can create unbalance
```

**Example:**
```
Current load:
Service A: 8 connections, 75% CPU
Service B: 3 connections, 45% CPU  ← Selected (least loaded)
Service C: 5 connections, 60% CPU

Request → Service B
```

---

### Strategy 3: Random (Fallback)

```python
strategy = 'random'

# Returns random service
# Best: Simple fallback, no tracking needed
# Worst: Can create hotspots
```

---

### Strategy 4: Custom (Advanced)

```python
strategy = 'custom'

def custom_strategy(services_metrics):
    # services_metrics = {
    #     'host1:8000': {'cpu': 45, 'memory': 60, 'latency_ms': 50},
    #     'host2:8000': {'cpu': 70, 'memory': 75, 'latency_ms': 120},
    #     ...
    # }
    
    # Select based on your logic
    best_service = None
    best_score = float('inf')
    
    for service, metrics in services_metrics.items():
        # CPU weight: 0.5, Memory weight: 0.3, Latency weight: 0.2
        score = (0.5 * metrics['cpu'] + 
                0.3 * metrics['memory'] + 
                0.2 * (metrics['latency_ms'] / 100))
        
        if score < best_score:
            best_score = score
            best_service = service
    
    return best_service

selected = lb.select_service(strategy='custom', handler=custom_strategy)
```

---

## 🔧 Advanced Features

### Health Checking

```python
# Set health check configuration
lb.set_health_check(
    interval_seconds=10,      # Check every 10 seconds
    timeout_seconds=2,        # 2 second timeout
    unhealthy_threshold=3,    # Mark down after 3 failures
    healthy_threshold=2       # Mark up after 2 successes
)

# Health check runs automatically
# Services marked as "down" are removed from pool
```

### Failover & Recovery

```python
# Automatically handles failures
def handle_request(data):
    try:
        selected = lb.select_service('least_loaded')
        response = requests.post(f'http://{selected}', json=data)
        
        # Success - update metrics
        lb.update_service_metrics(selected, {'error_rate': 0})
        
        return response.json()
    
    except Exception as e:
        # Failure - update metrics
        lb.update_service_metrics(selected, {'error_rate': 1.0})
        
        # Try different service
        retry_service = lb.select_service('least_loaded')
        response = requests.post(f'http://{retry_service}', json=data)
        
        return response.json()
```

### Sticky Sessions (Affinity)

```python
# Route same user to same service
def get_service_for_user(user_id):
    # Use consistent hashing based on user_id
    services = lb.get_all_services()
    service_index = hash(user_id) % len(services)
    
    return services[service_index]

# Result: User 123 always goes to Service B
# Result: User 456 always goes to Service A
```

---

## 📚 Real-World Examples

### Example 1: Basic Web Request Distribution

```python
def handle_web_request(request_data):
    # Select service
    service = lb.select_service('least_loaded')
    
    try:
        # Call service
        response = requests.post(
            f'http://{service}/api/process',
            json=request_data,
            timeout=5
        )
        
        # Update metrics
        start = time.time()
        latency_ms = (time.time() - start) * 1000
        
        lb.update_service_metrics(service, {
            'response_time_ms': latency_ms,
            'error_rate': 0
        })
        
        return response.json()
    
    except requests.Timeout:
        # Mark service as slow
        lb.update_service_metrics(service, {'error_rate': 0.5})
        
        # Retry with different service
        service = lb.select_service('least_loaded')
        response = requests.post(f'http://{service}/api/process', json=request_data)
        
        return response.json()
```

### Example 2: Canary Deployment

```python
# Gradually roll out new version

# Phase 1: Send 5% to new version
services = {
    'api_v1_a': 0.25,      # 25%
    'api_v1_b': 0.25,      # 25%
    'api_v1_c': 0.25,      # 25%
    'api_v2_canary': 0.05  # 5% - NEW
}

def canary_select_service():
    rand = random.random()
    cumulative = 0
    
    for service, weight in services.items():
        cumulative += weight
        if rand < cumulative:
            return service

# Monitor metrics for v2
v2_metrics = get_service_metrics('api_v2_canary')

if v2_metrics['error_rate'] < 0.01:  # < 1% errors
    # Phase 2: Increase to 25%
    services['api_v2_canary'] = 0.25
    del services['api_v1_c']  # Remove old service
```

### Example 3: Load Balancer Monitoring

```python
# Monitor load balancer health

def monitor_lb():
    while True:
        services = lb.get_all_services()
        
        for service in services:
            metrics = lb.get_service_metrics(service)
            
            # Check health
            if metrics['error_rate'] > 0.1:  # > 10% errors
                print(f"⚠️ {service}: High error rate: {metrics['error_rate']}")
            
            if metrics['cpu_percent'] > 90:  # > 90% CPU
                print(f"⚠️ {service}: High CPU: {metrics['cpu_percent']}")
            
            if metrics['memory_percent'] > 85:  # > 85% memory
                print(f"⚠️ {service}: High memory: {metrics['memory_percent']}")
        
        # Summary
        all_metrics = [lb.get_service_metrics(s) for s in services]
        avg_latency = sum(m['response_time_ms'] for m in all_metrics) / len(all_metrics)
        
        print(f"Average latency: {avg_latency:.1f}ms")
        print(f"Active services: {len(services)}")
        
        time.sleep(30)
```

---

## 🔧 Troubleshooting

### Issue: Unbalanced Load Distribution

**Cause:** Strategy not matching actual workload

**Solution:**
```python
# Wrong: Round-robin for variable load
selected = lb.select_service('round_robin')
# Results: Some services overloaded, others idle

# Right: Use least-loaded for variable workload
selected = lb.select_service('least_loaded')
# Results: Balanced distribution
```

---

### Issue: Service Keeps Getting Selected Despite Errors

**Cause:** Not updating error metrics

**Solution:**
```python
# ❌ Wrong: Don't update after errors
try:
    response = requests.post(f'http://{service}', json=data)
except Exception:
    pass  # Ignore error - but metrics not updated!

# ✅ Right: Update metrics on error
try:
    response = requests.post(f'http://{service}', json=data)
    lb.update_service_metrics(service, {'error_rate': 0})
except Exception:
    lb.update_service_metrics(service, {'error_rate': 0.5})
```

---

### Issue: Canary Deployment Not Taking Traffic

**Cause:** Weights not adding up or service not registered

**Solution:**
```python
# Register service explicitly
lb.register_service('api_v2_canary', 'host4:8000')

# Verify registration
services = lb.get_all_services()
print(services)  # Should include 'api_v2_canary'
```

---

## ✅ Best Practices

### 1. Choose Right Strategy

```python
# ✅ For stable workloads: Round-Robin
strategy = 'round_robin'

# ✅ For variable workloads: Least-Loaded
strategy = 'least_loaded'

# ✅ For complex requirements: Custom
strategy = 'custom'

# ❌ Avoid: Using wrong strategy for workload
```

### 2. Update Metrics Consistently

```python
# ✅ Always update after requests
try:
    response = requests.post(f'http://{service}', json=data)
    lb.update_service_metrics(service, {
        'response_time_ms': elapsed_ms,
        'error_rate': 0,
        'cpu_percent': get_cpu(),  # Optional but helpful
    })
except Exception as e:
    lb.update_service_metrics(service, {
        'error_rate': 1.0,
    })

# ❌ Avoid: Fire and forget
response = requests.post(f'http://{service}', json=data)
# No metrics update - LB is blind!
```

### 3. Monitor Service Health

```python
# ✅ Regular health monitoring
while True:
    for service in lb.get_all_services():
        try:
            requests.get(f'http://{service}/health', timeout=2)
            lb.update_service_metrics(service, {'health': 'up'})
        except:
            lb.update_service_metrics(service, {'health': 'down'})
    
    time.sleep(10)

# ❌ Avoid: No health checks
```

### 4. Handle Failures Gracefully

```python
# ✅ Retry with exponential backoff
for attempt in range(3):
    try:
        service = lb.select_service('least_loaded')
        response = requests.post(f'http://{service}', json=data, timeout=5)
        return response.json()
    except Exception as e:
        if attempt < 2:
            wait_time = 2 ** attempt  # 1s, 2s, 4s
            time.sleep(wait_time)
        else:
            raise

# ❌ Avoid: No retry logic
service = lb.select_service('least_loaded')
response = requests.post(f'http://{service}', json=data)  # Fails once, returns error
```

### 5. Use Gradual Rollouts

```python
# ✅ Gradual canary deployment
phases = [
    {'new_version': 0.01, 'duration': 30},  # 1% for 30 min
    {'new_version': 0.05, 'duration': 60},  # 5% for 60 min
    {'new_version': 0.25, 'duration': 120}, # 25% for 2 hours
    {'new_version': 1.00, 'duration': 0},   # 100% - full rollout
]

# ❌ Avoid: Full rollout immediately
# New version → All traffic immediately
```

---

## 📊 Performance Tuning

### Metrics to Monitor

```python
# Key metrics for each service
metrics = {
    'response_time_ms': 50,      # Response latency
    'error_rate': 0.01,          # % of requests that fail
    'cpu_percent': 45,           # CPU utilization
    'memory_percent': 60,        # Memory utilization
    'active_connections': 23,    # Current connections
    'throughput_rps': 1000       # Requests per second
}
```

### Tuning Configuration

```python
# Adjust parameters based on your workload
lb = IntelligentLoadBalancer(
    health_check_interval_s=10,  # Check every 10s
    metrics_window=300,           # Use last 5 minutes of metrics
    strategy='least_loaded'
)
```

---

## 🎯 Decision Matrix: Which Strategy?

| Scenario | Strategy | Reason |
|----------|----------|---------|
| All servers identical, stable load | round_robin | Simplest, fair |
| Variable load, fast changing | least_loaded | Adapts to actual load |
| Long-running requests | least_loaded | Avoids server overload |
| Stateful services | sticky | Maintains session affinity |
| Complex requirements | custom | Full control |

---

<div align="center">

## ✅ Load Balancer Guide Complete

**Next:** 
- Try [examples/03_load_balancing.py](../examples/03_load_balancing.py)
- Or read [guides/DISTRIBUTED_TRACING.md](DISTRIBUTED_TRACING.md)
- Or check [guides/COMPLETE_GUIDE.md](COMPLETE_GUIDE.md)

</div>
