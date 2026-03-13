# How to Use & Run the Autonomous Evolution System

## Quick Start (2 minutes)

### Method 1: Run the Complete Demo

```bash
cd c:\Users\hphaniki\Downloads\Autonomous
python run_autonomous_system.py
```

This shows you:
- How to initialize the system
- How to run one evolution cycle
- How to check status
- How to inspect all components
- Practical examples of each feature

**Output**: You'll see a complete walkthrough of the system with results printed.

---

### Method 2: Run Continuous Evolution

```bash
cd c:\Users\hphaniki\Downloads\Autonomous
python run_continuous_evolution.py
```

This will:
- Run autonomously in a loop
- Improve itself continuously
- Print progress after each cycle
- Keep going until you press `Ctrl+C`

**Output**: Live status of each evolution cycle with improvements

---

### Method 3: Fast Continuous Mode

```bash
python run_continuous_evolution.py --fast
```

Same as above but with 5-second intervals instead of 60 seconds between cycles.

---

## Python Code Usage

If you want to use it in your own Python code:

### Basic Usage (Copy & Paste)

```python
from phase4_integration import get_phase4_integration_layer

# Initialize the system
evolution = get_phase4_integration_layer()

# Run ONE evolution cycle
result = evolution.execute_evolution_cycle()

# Print results
print(f"Improvements: {result['improvements_adopted']}")
print(f"Improvement: +{result['total_improvement']:.1%}")
print(f"Safety: {result['safety_score']:.1%}")
```

### Run Multiple Cycles

```python
from phase4_integration import get_phase4_integration_layer

evolution = get_phase4_integration_layer()

# Run 10 cycles
for cycle in range(10):
    result = evolution.execute_evolution_cycle()
    print(f"Cycle {cycle+1}: +{result['total_improvement']:.1%}")
```

### Check System Status

```python
status = evolution.get_evolution_status()

print(f"Cycles completed: {status['cycles_completed']}")
print(f"Total improvements: {status['total_improvements']}")
print(f"Safety score: {status['avg_safety_score']:.1%}")
```

### Check Self-Awareness

```python
# System analyzes itself
snapshot = evolution.self_model.analyze_self()

print(f"Health: {snapshot.health_score:.1%}")
print(f"Efficiency: {snapshot.efficiency:.1%}")
print(f"Bottlenecks: {len(snapshot.bottlenecks)}")
```

### Check Safety & Values

```python
alignment = evolution.value_engine.get_alignment_report()

print(f"Reliability: {alignment['values']['reliability']}")
print(f"Safety: {alignment['values']['safety']}")
print(f"Privacy: {alignment['values']['privacy']}")
```

### Check Autonomous Goals

```python
goals = evolution.goal_generator.get_active_goals()

for goal in goals[:5]:
    print(f"{goal.title}: {goal.progress*100:.1f}% progress")
```

---

## What Happens When You Run It?

### During Each Evolution Cycle:

```
1. OBSERVE
   ↓ System analyzes its own state
   └─ Components, health, performance, bottlenecks

2. FORMULATE_GOALS
   ↓ System identifies what to improve
   └─ Ranked by impact/effort ratio

3. GENERATE_OPTIONS
   ↓ System creates improvement variants
   └─ Code optimizations, parameter tuning, resource rebalancing

4. EVALUATE_OPTIONS
   ↓ System checks safety and values
   └─ Must pass all constraints

5. IMPLEMENT
   ↓ System applies changes
   └─ Hot-patches code, updates config

6. EXPERIMENT
   ↓ System tests improvements safely
   └─ A/B testing with statistical validation

7. MEASURE
   ↓ System quantifies impact
   └─ Metrics collection

8. INTEGRATE
   ↓ System adopts improvements
   └─ Winners become new baseline

9. REFLECT
   ↓ System learns from cycle
   └─ Meta-reasoning optimization

[NEXT CYCLE → Continuous improvement spiral]
```

---

## Expected Output

### Demo Mode Output:

```
======================================================================
  DEMO 1: Basic Autonomous Evolution
======================================================================

Importing the autonomous system...
✓ Creating evolution system...

Running ONE autonomous evolution cycle...

============================================================
EVOLUTION CYCLE #1 STARTED
============================================================

[PHASE 1] OBSERVE - System Introspection
  Components analyzed: 8
  Bottlenecks identified: 2
  Weaknesses found: 3

[PHASE 2] FORMULATE_GOALS - Autonomous Objective Setting
  Formulated 5 goals
  Activated 3 top goals

[PHASE 3] GENERATE_OPTIONS - Improvement Generation
  Generated 5 improvement options

[PHASE 4] EVALUATE_OPTIONS - Safety & Value Alignment
  Approved 4/5 options

[PHASE 5] IMPLEMENT - Apply Modifications
  ✓ Applied code modification
  ✓ Applied parameter tuning

[PHASE 6] EXPERIMENT - Safe Testing
  Created experiment: evolution_exp_1_0

[PHASE 7] MEASURE - Impact Measurement
  Avg improvement: 23.5%

[PHASE 8] INTEGRATE - Adopt Best Improvements
  ✓ Adopted improved algorithm: smart_cache

[PHASE 9] REFLECT - Meta-Learning
  Reasoning traces: 42
  Safety passing rate: 95%
  Value alignment: 0.87

============================================================
EVOLUTION CYCLE #1 COMPLETE
  Duration: 3.2s
  Outcomes:
    Goals formulated: 5
    Options generated: 5
    Options approved: 4
    Changes implemented: 2
    Improvements adopted: 1
    Total improvement: 23.5%
    Safety score: 95%
============================================================

RESULT:
  Status: complete
  Duration: 3.2 seconds
  Goals formulated: 5
  Changes implemented: 2
  Improvements adopted: 1
  Total improvement: 23.5%
  Safety score: 95%
```

### Continuous Mode Output:

```
╔════════════════════════════════════════════════════════════════╗
║                AUTONOMOUS EVOLUTION SYSTEM - CONTINUOUS MODE  ║
║                                                                ║
║     The system will now improve itself autonomously...        ║
║                       Press Ctrl+C to stop                     ║
╚════════════════════════════════════════════════════════════════╝

╔═ CYCLE #001 ================================================╗
║ Status: ✓ complete
║ Duration: 3.5s
║ Total runtime: 3.5s
╠════════════════════════════════════════════════════════════╣
║ Goals formulated: 5
║ Changes implemented: 2
║ Improvements adopted: 1
║ Total improvement: 18.5%
║ Safety score: 96%
╚════════════════════════════════════════════════════════════╝

Next cycle in 60 seconds...


╔═ CYCLE #002 ================================================╗
║ Status: ✓ complete
║ Duration: 3.2s
║ Total runtime: 66.7s
╠════════════════════════════════════════════════════════════╣
║ Goals formulated: 4
║ Changes implemented: 1
║ Improvements adopted: 1
║ Total improvement: 12.3%
║ Safety score: 97%
╚════════════════════════════════════════════════════════════╝

Next cycle in 60 seconds...
```

---

## If You Get Errors

### 1. "Module not found" Error:

Make sure you're in the right directory:
```bash
cd c:\Users\hphaniki\Downloads\Autonomous
```

### 2. "Import error" Error:

Install required dependencies:
```bash
pip install -r requirements.txt
```

### 3. "Logger not initialized" Error:

The system will create logs automatically. This is normal. Check:
```bash
cat logs/system.log
```

---

## Files You Need

The system needs these files in the `src/` folder:

- ✅ `phase4_integration.py` - Main orchestrator
- ✅ `learning_loop.py` - Learning engine
- ✅ `self_model.py` - Self-awareness
- ✅ `autonomous_goal_generator.py` - Goal formation
- ✅ `code_modification_engine.py` - Self-code evolution
- ✅ `experimentation_framework.py` - Safe testing
- ✅ `meta_reasoning_engine.py` - Thinking optimization
- ✅ `parameter_auto_tuner.py` - Configuration tuning
- ✅ `resource_reallocator.py` - Resource balancing
- ✅ `knowledge_integrator.py` - Knowledge absorption
- ✅ `value_alignment_engine.py` - Safety enforcement
- ✅ `logger.py` - Logging system
- ✅ `config.py` - Configuration

All these are already in your `src/` folder!

---

## Customization

### Adjust Cycle Timing

```python
evolution = get_phase4_integration_layer()

# Fast cycles (5 seconds)
for _ in range(100):
    evolution.execute_evolution_cycle()
    time.sleep(5)

# Slow cycles (5 minutes)
for _ in range(100):
    evolution.execute_evolution_cycle()
    time.sleep(300)
```

### Customize Human Values

```python
from value_alignment_engine import ValueType

evolution = get_phase4_integration_layer()

# Increase emphasis on efficiency
evolution.value_engine.values[ValueType.EFFICIENCY] = 0.95

# Increase emphasis on privacy
evolution.value_engine.values[ValueType.PRIVACY] = 1.0

# Then run cycles - they'll optimize for these values
evolution.execute_evolution_cycle()
```

### Monitor Specific Metrics

```python
status = evolution.get_evolution_status()

# Get last cycle details
last = status['last_cycle']
print(f"Last cycle improved by {last['total_improvement']:.1%}")

# Get average safety across all cycles
avg_safety = status['avg_safety_score']
print(f"Average safety: {avg_safety:.1%}")

# Check how many goals are active
print(f"Active goals: {status['active_goals']}")
```

---

## Example: Build Your Own Solution

```python
#!/usr/bin/env python3
import sys
import time
sys.path.insert(0, 'src')

from phase4_integration import get_phase4_integration_layer

def main():
    # Initialize
    evolution = get_phase4_integration_layer()
    
    print("AUTONOMOUS SYSTEM STARTING...")
    print("System will improve itself continuously.\n")
    
    total_improvement = 0
    
    try:
        cycle = 0
        while True:
            cycle += 1
            
            # Run evolution
            result = evolution.execute_evolution_cycle()
            total_improvement += result['total_improvement']
            
            # Print status
            print(f"Cycle {cycle}: " + 
                  f"+{result['total_improvement']:.1%} | " +
                  f"Adopted: {result['improvements_adopted']} | " +
                  f"Cumulative: {total_improvement:.1%} | " +
                  f"Safety: {result['safety_score']:.1%}")
            
            # Exit if no more improvements
            if result['improvements_adopted'] == 0:
                print(f"\nNo improvements found. Total gain: {total_improvement:.1%}")
                break
            
            time.sleep(10)
    
    except KeyboardInterrupt:
        print(f"\n\nStopped. Total improvement: {total_improvement:.1%}")

if __name__ == "__main__":
    main()
```

Save this as `my_autonomous_system.py` and run:
```bash
python my_autonomous_system.py
```

---

## Summary

You have THREE ways to use the system:

| Method | Command | Use Case |
|--------|---------|----------|
| **Demo** | `python run_autonomous_system.py` | Learn how it works |
| **Continuous** | `python run_continuous_evolution.py` | Run indefinitely |
| **Fast Mode** | `python run_continuous_evolution.py --fast` | Quick iterations |

**The system will automatically:**
- ✓ Observe itself
- ✓ Set improvement goals
- ✓ Generate solutions
- ✓ Test them safely
- ✓ Measure impact
- ✓ Adopt winners
- ✓ Get smarter each cycle

**All while maintaining safety and human values.**

---

## Next Steps

1. **Run the demo**: `python run_autonomous_system.py`
2. **Try continuous mode**: `python run_continuous_evolution.py`
3. **Read the detailed docs**: See `PHASE4_QUICKSTART.md`
4. **Customize**: Adjust values and parameters in the code
5. **Monitor**: Check logs in `logs/` folder

The system is ready to use. Just run it!

