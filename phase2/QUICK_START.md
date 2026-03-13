# ⚡ Quick Start - 5 Minutes

> Get Phase 2 running in 5 minutes or less

---

## Step 1: Run the Demo (3 minutes)

```bash
cd ..  # Go back to Autonomous root
python src/run_phase2_demo.py
```

When prompted, select: `all`

**What you'll see:**
- ✅ Demo 1: Component caching in action
- ✅ Demo 2: Request tracing visualization  
- ✅ Demo 3: Load balancing distribution
- ✅ Demo 4: All systems working together

---

## Step 2: See Basic Code (2 minutes)

```python
# Component Wrapper (automatic caching)
from src.component_wrapper_factory import get_component_wrapper_factory

factory = get_component_wrapper_factory()
wrapped = factory.wrap_component(my_service, "my_service_id")
result = wrapped.method()  # ✅ Cached & monitored

# Distributed Tracing (request visibility)
from src.distributed_tracing import get_tracing_system

ts = get_tracing_system()
trace = ts.start_trace()
span = ts.start_span("Service", "operation")
# ... work ...
ts.end_span(span.span_id)

# Intelligent Load Balancer (smart routing)
from src.intelligent_load_balancer import get_load_balancer

lb = get_load_balancer()
lb.register_component("svc_a", service_a)
selected = lb.get_component()  # Picks best
```

---

## What You Just Did ✅

- ✅ Saw Phase 2 in action with 4 demos
- ✅ Learned the basic code patterns
- ✅ Understood how 3 components work

---

## Next Steps

### Want More Details? (15 minutes total)
→ Go to [`GETTING_STARTED.md`](GETTING_STARTED.md)

### Want CODE EXAMPLES? (20 minutes)
→ Go to [`examples/`](examples/) folder
```bash
python examples/01_basic_wrapping.py
python examples/02_distributed_tracing.py
python examples/03_load_balancing.py
python examples/04_full_integration.py
```

### Want COMPLETE GUIDE? (1 hour)
→ Go to [`guides/COMPLETE_GUIDE.md`](guides/COMPLETE_GUIDE.md)

### Want to INTEGRATE NOW? (30 min)
→ Go to [`docs/INTEGRATION.md`](docs/INTEGRATION.md)

### Lost? 
→ Go to [`INDEX.md`](INDEX.md) or [`README.md`](README.md)

---

## 💡 Key Takeaways

| Component | What | Why |
|-----------|------|-----|
| **Wrapper** | Wrap service → auto cache | 50-80% faster |
| **Tracing** | Track requests end-to-end | See what happens |
| **Balancer** | Route to best service | Optimized perf |

---

**Done! You now understand Phase 2 basics.** 🎉

→ **Next:** Choose your path above based on time available
