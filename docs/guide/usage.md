# Usage Guide

How to use the Autonomous AI System effectively.

## Basic Usage

### Starting the System

```bash
# Run with defaults
python -m src.main

# Run with custom config
python -m src.main --config custom.yaml

# Run specific mode
python -m src.main --mode autonomous
python -m src.main --mode interactive
```

---

## Autonomous Mode

Fully automatic operation - system learns continuously.

```bash
python -m src.main --mode autonomous --iterations 20
```

The system will:
1. Crawl web for knowledge
2. Learn from content
3. Reason and plan
4. Improve itself
5. Reflect on experience

Repeat for N iterations.

---

## Interactive Mode

Manual control mode - you direct operations.

```bash
python -m src.main --mode interactive
```

Available commands:

### System Commands
```
status              Show current status
config              View configuration
help                Show all commands
exit                Exit program
```

### Operation Commands
```
crawl [depth]       Run web crawling
learn               Run learning cycle
reason              Run reasoning cycle
improve             Self-improvement cycle
```

### Query Commands
```
query <question>    Ask a question
search <term>       Search knowledge base
recall <query>      Recall from memory
```

### Batch Operations
```
auto [n]            Run n autonomous cycles
cycle [name]        Run specific cycle
benchmark           Run performance test
```

---

## Programmatic Usage

Use as a library in your code:

```python
from src.core import AutonomousAgent

# Initialize
agent = AutonomousAgent()
agent.initialize()

# Run operations
result = agent.reason("What is machine learning?")
print(result)

# Run learning cycle
metrics = agent.run_cycle()
print(f"Learned: {metrics['items_learned']} items")

# Shutdown gracefully
agent.shutdown()
```

---

## Advanced Patterns

### Custom Learning Loop

```python
from src.core import WebCrawler, LearningEngine
from src.core import MemoryManager, ReasoningEngine

# Initialize components
crawler = WebCrawler()
learner = LearningEngine()
memory = MemoryManager()
reasoner = ReasoningEngine()

# Custom loop
for iteration in range(10):
    # Crawl
    content = crawler.crawl("https://example.com")
    
    # Learn
    knowledge = learner.learn(content)
    memory.store_long_term(f"iter_{iteration}", knowledge)
    
    # Reason
    insights = reasoner.reason(knowledge)
    
    print(f"Iteration {iteration}: Found {len(insights)} insights")
```

---

### Custom Reasoning

```python
from src.core import ReasoningEngine

reasoner = ReasoningEngine()

# Complex query
query = {
    "type": "planning",
    "goal": "Solve coding problem",
    "constraints": ["Use Python", "2 hour limit"],
    "optimization": "code quality"
}

result = reasoner.reason(query)
print(f"Plan: {result['action_plan']}")
print(f"Confidence: {result['confidence']}")
```

---

### Memory Operations

```python
from src.core import MemoryManager

memory = MemoryManager()

# Short-term (temporary)
memory.store_short_term("current_task", task_data, ttl=300)  # 5 minutes

# Long-term (persistent)
memory.store_long_term("learned_skill", skill_data)

# Recall
task = memory.recall_short_term("current_task")
skill = memory.recall_long_term("learned_skill")

# Consolidate
memory.consolidate()  # Move short→long term
```

---

## Configuration

### Via Environment File

Create `.env`:
```bash
LOG_LEVEL=DEBUG
AUTONOMOUS_MODE_ENABLED=true
MAX_CRAWL_DEPTH=3
BATCH_SIZE=32
LEARNING_RATE=0.001
```

### Via Config File

Edit `src/config.py`:
```python
# Crawler settings
MAX_CRAWL_DEPTH = 3
MAX_PAGES_CRAWL = 100
CRAWL_TIMEOUT = 10

# Learning settings
BATCH_SIZE = 32
LEARNING_RATE = 0.001
EPOCHS = 10

# Memory settings
SHORT_TERM_TTL = 3600  # 1 hour
MAX_MEMORY_GB = 4

# Logging
LOG_LEVEL = "INFO"
LOG_FILE = "logs/system.log"
```

### Via Command Line

```bash
python -m src.main --batch-size 16 --log-level DEBUG
```

---

## Performance Tuning

### For Speed
```python
# Reduce batch size
BATCH_SIZE = 8

# Fewer iterations
MAX_CRAWL_DEPTH = 2

# Less memory overhead
SHORT_TERM_TTL = 600  # 10 minutes
```

### For Accuracy
```python
# Larger batches
BATCH_SIZE = 64

# More crawling
MAX_CRAWL_DEPTH = 5

# Keep more memory
SHORT_TERM_TTL = 7200  # 2 hours
```

### For Resource Usage
```python
# Single-threaded
MAX_WORKERS = 1

# Limited memory
MAX_KNOWLEDGE_ENTRIES = 10000

# Smaller embeddings
EMBEDDING_DIMENSION = 256  # Reduced
```

---

## Monitoring

### Check Status

```bash
# Interactive
> status

# Programmatic
status = agent.get_status()
print(f"Running for {status['uptime']}")
print(f"Iterations: {status['iterations']}")
print(f"Memory: {status['memory_used_mb']} MB")
```

### View Logs

```bash
# Real-time
tail -f logs/system.log

# Errors only
grep ERROR logs/system.log

# Performance metrics
grep METRIC logs/system.log
```

### Performance Metrics

```python
# Get metrics
metrics = agent.get_metrics()
print(f"Queries: {metrics['total_queries']}")
print(f"Avg response: {metrics['avg_response_time']}ms")
print(f"Success rate: {metrics['success_rate']}%")
```

---

## Troubleshooting

### High Memory Usage
```python
# Reduce cache
SHORT_TERM_TTL = 300

# Prune knowledge
knowledge_base.prune()

# Consolidate memory
memory.consolidate()
```

### Slow Responses
```python
# Check logs
tail -50 logs/system.log

# Run benchmark
agent.run_benchmark()

# Profile code
python -m cProfile -s cumtime -m src.main
```

### Crashed or Hung
```bash
# Kill process
# Windows: taskkill /IM python.exe
# Linux: killall python

# Clear locks
rm -f data/.lock

# Restart
python -m src.main
```

---

See: [architecture.md](architecture.md), [examples.md](examples.md)
