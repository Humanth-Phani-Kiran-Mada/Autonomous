# Self-Evolving AI System - Complete User Guide

## ✨ What You Have

A complete, production-ready **autonomous AI system** that:
- Crawls the web for knowledge
- Learns automatically from discovered content
- Reasons about problems and makes decisions
- Improves its own capabilities
- Maintains comprehensive memory
- Achieves self-directed goals
- ♾️ Operates indefinitely without human intervention

## Your Next Steps

### Step 1: Setup (Choose your OS)

**For Linux/Mac:**
```bash
cd /path/to/SELF_DEV_AI
chmod +x setup.sh
./setup.sh
source venv/bin/activate
```

**For Windows:**
```bash
cd C:\path\to\SELF_DEV_AI
setup.bat
venv\Scripts\activate
```

### Step 2: Verify Installation

```bash
# Check Python version
python --version

# Check dependencies
pip list | grep -E "torch|transformers|requests|aiohttp"
```

### Step 3: Start Using It

```bash
python main.py
```

You'll see a prompt to choose between:
- **Autonomous Mode** - Let it learn automatically (recommended)
- **Interactive Mode** - Control via commands

## Quick Start (60 seconds)

```bash
# 1. Setup (choose your OS above)

# 2. Run
python main.py

# 3. Choose: Autonomous mode (recommended)

# 4. Enter iterations: 10 (for quick test)

# 5. Watch as it learns!
```

## Documentation Map

| File | Purpose | Read Time |
|------|---------|-----------|
| **INDEX.md** | Overview & quick reference | 3 min |
| **GETTING_STARTED.md** | Detailed setup & usage | 5 min |
| **ARCHITECTURE.md** | Technical deep dive | 10 min |
| **README.md** | Full documentation | 8 min |
| **config.py** | All configuration options | 2 min |

**Start here:** -> INDEX.md -> GETTING_STARTED.md -> Try it -> ARCHITECTURE.md

## Understanding the System

### The 5-Phase Loop (Repeating Cycle)

Each iteration runs these phases in sequence:

1. ** Crawling** (discover web content)
2. ** Learning** (extract knowledge)
3. ** Reasoning** (analyze and plan)
4. ** Improvement** (develop skills)
5. ** Maintenance** (save and optimize)

### What Gets Better Over Time

- **Knowledge Base**: Grows larger and more comprehensive
- **Skills**: Domain-specific capabilities increase
- **Reasoning**: Better decision-making with experience
- **Memory**: More connections between concepts
- **Speed**: Faster processing as it optimizes

## 🎛️ Key Configuration Options

Edit `config.py` to adjust:

```python
# How fast it learns
LEARNING_RATE = 0.01 # Increase for faster learning

# How many pages to crawl per cycle
CRAWLER_MAX_WORKERS = 5

# Maximum knowledge to store
MAX_KNOWLEDGE_ENTRIES = 100000

# Enable/disable autonomous mode
AUTONOMOUS_MODE_ENABLED = True
```

## Monitoring Progress

### During Execution
```bash
In interactive mode, run:
> status

Shows:
- Knowledge entries
- Skills developed
- Success rate
- Memory usage
```

### After Execution
Check these files:
- `logs/ai_evolution.log` - All operations
- `data/learning_metrics.json` - Learning stats
- `data/skill_levels.json` - What it's good at
- `data/knowledge/knowledge_base.json` - Learned facts

## 💻 Commands (Interactive Mode)

**Learning:**
```bash
> learn # Run one learning cycle
> crawl # Crawl web for content
> improve # Improve skills
```

**Analysis:**
```bash
> query # Ask a question
> reason # Reason about a topic
```

**Management:**
```bash
> status # Show statistics
> auto 10 # Run 10 autonomous iterations
> exit # Exit program
```

## Recommended Usage Patterns

### Pattern 1: Quick Test (5 minutes)
```bash
python main.py
# Interactive mode
# Run: learn, query, status, exit
```

### Pattern 2: Exploration (30 minutes)
```bash
python main.py
# Autonomous mode
# 5 iterations
# Observe learning and improvement
```

### Pattern 3: Extended Training (Hours)
```bash
python main.py
# Autonomous mode 
# 50-100 iterations
# Monitor logs
# Review final results
```

### Pattern 4: Specific Learning (Goal-directed)
```bash
python main.py
# Interactive mode
# Set goals
# Run learning cycles
# Track progress
```

## What to Expect

### After 5 iterations
- Basic knowledge acquired
- First patterns identified
- Initial skills emerging

### After 20 iterations
- Substantial knowledge base built
- Multiple skills at decent levels
- Clear learning patterns

### After 50+ iterations
- Comprehensive knowledge across domains
- Well-developed skills
- Complex reasoning capability
- Emerging specializations

## Important Notes

**It's safe to:**
- Stop anytime (Ctrl+C) - state is saved
- Run multiple times - state persists
- Modify config between runs
- Check logs anytime

**Resource usage:**
- Memory: ~100-500 MB (configurable)
- CPU: Uses available resources
- Disk: ~100MB minimum for data

**Data:**
- Everything saved in `data/` folder
- Logs in `logs/` folder
- Safe to backup anytime
- Can be wiped to reset

## 🆘 Troubleshooting

**"Module not found"**
-> Run `pip install -r requirements.txt`

**"Python not found"**
-> Install Python 3.8+ from python.org

**"Permission denied"**
-> Run `chmod +x setup.sh` (Linux/Mac)

**"Slow performance"**
-> Reduce `CRAWLER_MAX_WORKERS` in config.py

**"High memory usage"**
-> Reduce `MAX_KNOWLEDGE_ENTRIES` in config.py

## Learning Outcomes

By using this system, you'll learn about:
- Autonomous agent architecture
- Knowledge representation
- Semantic search techniques
- Self-improvement mechanisms
- Goal-oriented AI
- Feedback loops
- Performance metrics

## Advanced Topics

### Customizing Learning Sources
Edit `config.py`:
```python
LEARNING_SOURCES = [
 "https://example.com",
 "https://another.com",
]
```

### Extending Capabilities
Modify `src/learning_engine.py` to add:
- Custom skill definitions
- Domain specialization
- Specialized reasoning

### Monitoring Deep Insights
Analyze `data/learning_metrics.json` to:
- Track learning patterns
- Identify weak areas
- Optimize performance

## 🌟 Key Achievements

This system demonstrates:
 Fully autonomous operation
 Self-directed learning 
 Web data acquisition
 Knowledge integration
 Persistent memory
 Goal management
 Performance optimization
 Error recovery

## Getting Help

1. **Check the logs**
 ```bash
 tail -f logs/ai_evolution.log
 ```

2. **Review documentation**
 - GETTING_STARTED.md for setup issues
 - ARCHITECTURE.md for understanding
 - config.py for customization

3. **Verify dependencies**
 ```bash
 pip list
 ```

## Pro Tips

1. **First run**: Use interactive mode to explore
2. **Extended training**: Run during off-peak hours
3. **Monitoring**: Open logs in another terminal
4. **Tuning**: Start with defaults, adjust gradually
5. **Analysis**: Review data files after runs

## Checklist Before First Run

- [ ] Python 3.8+ installed
- [ ] Virtual environment created
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Data directories exist (`data/`, `logs/`)
- [ ] .env file configured (copy from .env.example)
- [ ] config.py reviewed and customized

## You're Ready!

You now have a complete self-evolving AI system. 

**Next step:** Run `python main.py` and watch your AI learn!

## 📞 Final Notes

- All code is well-documented
- Logs are comprehensive
- Data is safely persisted
- System is designed to be resilient
- It can run unattended indefinitely

---

**Happy AI training! **

For detailed information:
- Setup: GETTING_STARTED.md
- Architecture: ARCHITECTURE.md
- Overview: INDEX.md
- Full docs: README.md
