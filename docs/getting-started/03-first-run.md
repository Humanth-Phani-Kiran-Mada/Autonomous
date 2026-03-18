# Your First Run

Quick walkthrough of your first time running the system.

## Run the System

```bash
# Make sure virtual environment is activated first
source venv/bin/activate  # Linux/Mac
# OR
venv\Scripts\activate  # Windows

# Run the system
python -m src.main
```

---

## What You'll See

### Startup
```
╔════════════════════════════════════════════╗
║   Autonomous AI System Started             ║
║   Version: 4.0                             ║
╚════════════════════════════════════════════╝

System Status:
  ✓ Knowledge Base initialized
  ✓ Memory Manager ready
  ✓ Web Crawler configured
  ✓ Learning Engine loaded
  ✓ Reasoning Engine ready

Choose mode:
  [1] Autonomous (recommended)
  [2] Interactive
  
Enter choice (1 or 2):
```

### Autonomous Mode (Default)
```
Selected: Autonomous Mode

Enter number of iterations (default 5): 10

Starting autonomous learning loop...
```

Then watch as it cycles through:
1. **Crawling** - Discovers web content
2. **Learning** - Extracts knowledge
3. **Reasoning** - Makes decisions
4. **Improvement** - Refines itself
5. **Reflection** - Learns from experience

### Interactive Mode
```
Selected: Interactive Mode

Welcome to the interactive console.
Type 'help' for commands.

> help
Available commands:
  learn     - Run learning cycle
  crawl     - Run crawling cycle
  reason    - Run reasoning cycle
  improve   - Run improvement cycle
  query <q> - Ask a question
  status    - Show system status
  auto <n>  - Run <n> autonomous iterations
  exit      - Exit program

>
```

---

## First Commands to Try

### 1. Check System Status
```
> status

System Status Report:
═══════════════════════════════════════════
Session Time: 0:00:23
Iterations Completed: 5

Knowledge Base:
  Total Entries: 156
  Unique Concepts: 42
  Coverage Score: 0.78

Memory:
  Short-term: 234 MB
  Long-term: 1.2 GB
  Cache: 45 MB

Performance:
  Avg Cycle Time: 2.3s
  Throughput: 4.2 items/sec
  Resource Usage: 48%
```

### 2. Ask a Question
```
> query What can you tell me about machine learning?

Processing query...

Response:
"Based on my knowledge base, machine learning is a branch of
artificial intelligence that enables systems to learn and improve
from experience without being explicitly programmed. Key concepts
include supervised learning, unsupervised learning, and reinforcement
learning..."

Confidence: 0.82
Sources: 12 documents
Processing Time: 450ms
```

### 3. Run a Learning Cycle
```
> learn

Starting Learning Cycle...

Learning Phase Results:
═══════════════════════════════════════════
✓ Processed 15 knowledge items
✓ Updated 23 concepts
✓ Created 4 skill categories
✓ Identified 8 patterns
✓ Generated 12 insights

Learning Metrics:
  Success Rate: 94%
  Avg Confidence: 0.81
  Processing Time: 2.3s
```

### 4. Run Autonomous Iterations
```
> auto 5

Running 5 autonomous iterations...

Cycle 1: ████████░░ 87%
Cycle 2: ██████████ 100% Complete
Cycle 3: ███████░░░ 71%
Cycle 4: ██████████ 100% Complete
Cycle 5: ██████████ 100% Complete

Final Summary:
  Total Knowledge Acquired: 456 items
  Improvements Implemented: 8
  System Efficiency Gain: 12%
  Time Elapsed: 5m 23s
```

---

## Log Files

All activity is logged to `logs/`:

```
logs/
├── system.log          # Main system log
├── debug.log           # Detailed debugging
└── performance.log     # Performance metrics
```

View logs:
```bash
# Real-time log (Linux/Mac)
tail -f logs/system.log

# Last 100 lines
tail -100 logs/system.log

# Search logs
grep "ERROR" logs/system.log
```

---

## Data Storage

Check what the system learned:

```bash
ls -la data/
│
├── knowledge/          # Learned concepts
│   └── embeddings.npz
│   └── concepts.json
│
├── memory/             # Persistent memory
│   └── episodes.json
│   └── skills.json
│
└── cache/              # Web content cache
    └── urls_visited.json
    └── page_cache/
```

---

## Stopping the System

### Graceful Shutdown
In Interactive mode, type:
```
> exit
```

Or press `Ctrl+C`:
- First press: Graceful shutdown (saves state)
- Second press: Force exit

### Check Previous Runs

All sessions are saved to `data/memory/sessions.json`:
```json
{
  "sessions": [
    {
      "id": "2026-03-18-14:35:42",
      "duration": "5h 23m",
      "iterations": 42,
      "knowledge_acquired": 1230,
      "improvements": 23
    }
  ]
}
```

---

## Next Steps

- ✅ System runs and responds
- 👉 Read [architecture.md](../guide/architecture.md) to understand how it works
- 👉 Try [examples.md](../guide/examples.md) for advanced usage
- 👉 Configure [src/config.py](../../src/config.py) for your needs

---

**Stuck?** → See [troubleshooting.md](04-troubleshooting.md)

**Want to customize?** → See [usage.md](../guide/usage.md)
