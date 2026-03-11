# Self-Evolving AI System - Getting Started Guide

## 🚀 Quick Start (5 Minutes)

### Step 1: Setup
```bash
# Linux/Mac
./setup.sh

# Windows
setup.bat
```

### Step 2: Activate Environment
```bash
# Linux/Mac
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### Step 3: Run the System
```bash
python main.py
```

## 📋 Complete Installation Guide

### Prerequisites
- Python 3.8 or higher
- pip package manager
- 4 GB RAM (recommended)
- Internet connection (for web crawling)

### Detailed Setup

1. **Clone/Navigate to Project**
   ```bash
   cd /path/to/SELF_DEV_AI
   ```

2. **Create Virtual Environment**
   ```bash
   python3 -m venv venv
   ```

3. **Activate Virtual Environment**
   - **Linux/Mac:**
     ```bash
     source venv/bin/activate
     ```
   - **Windows:**
     ```bash
     venv\Scripts\activate
     ```

4. **Upgrade pip**
   ```bash
   pip install --upgrade pip
   ```

5. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

6. **Configure Environment**
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

7. **Create Data Directories**
   ```bash
   mkdir -p data/memory data/knowledge data/cache logs
   ```

## 🎮 Usage Modes

### Autonomous Mode (Hands-Off)
The AI runs autonomously, continuously learning and improving.

```bash
python main.py
# Select "autonomous mode"
# Enter number of iterations (e.g., 100)
```

**What happens:**
- Crawls web for new knowledge
- Learns from discovered content
- Improves its capabilities
- Maintains persistent memory
- Generates detailed logs

### Interactive Mode (Control)
You control the AI with commands.

```bash
# Edit config.py
AUTONOMOUS_MODE_ENABLED = false

# Then run:
python main.py
```

**Available Commands:**
- `learn` - Run learning cycle
- `crawl` - Crawl web for new knowledge
- `reason` - Run reasoning cycle
- `improve` - Self-improvement cycle
- `query` - Ask a question
- `status` - Show agent statistics
- `auto` - Run N autonomous iterations
- `exit` - Exit program

## 🧠 System Architecture

### Component Breakdown

1. **Web Crawler** - Discovers knowledge from the internet
2. **Knowledge Base** - Stores and retrieves learned information
3. **Memory Manager** - Manages short/long-term memory
4. **Learning Engine** - Processes knowledge and improves skills
5. **Reasoning Engine** - Plans, decides, and solves problems
6. **Autonomous Agent** - Orchestrates all components

### Data Flow
```
Web Crawler → Extracted Knowledge
          ↓
Knowledge Base ← Semantic Storage
          ↓
Learning Engine → Skill Development
          ↓
Reasoning Engine → Decision Making
          ↓
Memory Manager → Persistent Storage
```

## 📊 Monitoring Progress

### Check Status During Runtime
```bash
> status
```

Shows:
- Knowledge base size
- Memory statistics
- Skill levels
- Success rates
- Number of goals

### View Logs
```bash
# Main log
tail -f logs/ai_evolution.log

# Error log
tail -f logs/errors.log
```

### Data Files
```
data/
├── memory/
│   ├── memory_state.json      # Short/long-term memory
│   └── episodic_memory.json   # Experiences
├── knowledge/
│   ├── knowledge_base.json    # All learned facts
│   ├── embeddings.pkl         # Vector embeddings
│   └── metadata.json          # Knowledge metadata
├── cache/                      # Web crawler cache
├── crawler_state.json         # Crawling history
├── learning_metrics.json      # Learning progress
├── skill_levels.json          # Developed skills
├── goals.json                 # Agent goals
└── agent_state.json           # Overall state
```

## 🎯 Example Workflows

### Workflow 1: Autonomous Learning (20 hours)
1. Start autonomous mode with 100 iterations
2. Set learning rate appropriately
3. Monitor logs periodically
4. Review final summary statistics
5. Analyze learned domains and skills

### Workflow 2: Focused Learning
1. Interactive mode
2. `query` about a specific topic
3. `learn` from results
4. `reason` about the topic
5. `improve` related skills

### Workflow 3: Goal-Directed Learning
1. Set specific goals in reasoning engine
2. Run reasoning cycle to plan
3. Execute learning cycles
4. Track progress with `status`
5. Evaluate goal achievement

## 🔧 Configuration Guide

### Key Settings (config.py)

**Learning Speed**
```python
LEARNING_RATE = 0.01  # Increase for faster learning
LEARNING_RATE = 0.05  # Faster but less stable
```

**Web Crawling**
```python
CRAWLER_MAX_WORKERS = 5      # Parallel crawlers
CRAWLER_BATCH_SIZE = 10      # Items per batch
CRAWLER_TIMEOUT = 30         # Seconds per request
```

**Knowledge Management**
```python
MAX_KNOWLEDGE_ENTRIES = 100000      # Max size
MEMORY_COMPRESSION_RATIO = 0.8      # Prune when full
```

**Autonomous Operation**
```python
AUTONOMOUS_MODE_ENABLED = true          # Auto run
AUTO_START_LEARNING = true              # Auto crawl
AUTO_IMPROVE = true                     # Auto improve
SELF_IMPROVE_INTERVAL = 3600            # Seconds
```

### Environment Variables (.env)
```bash
# Logging
LOG_LEVEL=INFO  # DEBUG, INFO, WARNING, ERROR

# Performance
MAX_MEMORY_MB=4096           # Memory limit
MAX_CPU_PERCENT=80           # CPU limit
RATE_LIMIT_PER_SECOND=10    # API calls/sec

# Model
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
```

## 🚨 Troubleshooting

### Issue: "Module not found"
**Solution:**
```bash
pip install -r requirements.txt
```

### Issue: "CUDA/GPU errors"
**Solution:**
- Remove with GPU support: `pip install torch-cpu`
- Or just use CPU (works fine for this)

### Issue: "Memory growing too fast"
**Solution:**
```python
# In config.py
MAX_KNOWLEDGE_ENTRIES = 50000        # Reduce
MEMORY_COMPRESSION_RATIO = 0.7       # Increase pruning
```

### Issue: "Web crawling too slow"
**Solution:**
```python
# In config.py
CRAWLER_MAX_WORKERS = 8              # Increase workers
CRAWLER_BATCH_SIZE = 20              # Larger batches
LEARNING_SOURCES = [...]             # Reduce sources
```

### Issue: "No improvements happening"
**Solution:**
- Check `logs/ai_evolution.log` for details
- Ensure `AUTO_IMPROVE = true`
- Verify knowledge is being acquired
- Check learning metrics

## 📈 Performance Optimization

### For Fast Learning
```python
LEARNING_RATE = 0.05
CRAWLER_MAX_WORKERS = 10
CRAWLER_BATCH_SIZE = 20
EXPLORATION_RATE = 0.5
```

### For Deep Learning
```python
LEARNING_RATE = 0.01
CRAWLER_MAX_WORKERS = 3
CRAWLER_BATCH_SIZE = 5
EXPLORATION_RATE = 0.1
MAX_KNOWLEDGE_ENTRIES = 200000
```

### For Resource-Constrained Systems
```python
MAX_MEMORY_MB = 2048
CRAWLER_MAX_WORKERS = 2
CRAWLER_BATCH_SIZE = 5
MAX_KNOWLEDGE_ENTRIES = 10000
```

## 🔐 Safety Best Practices

1. **Monitor Resource Usage**
   - Watch CPU/Memory in system monitor
   - Set limits in config.py

2. **Regular Backups**
   - Backup `data/` folder regularly
   - Backup logs for analysis

3. **Rate Limiting**
   - Don't crawl websites too aggressively
   - Respect `robots.txt`
   - Use appropriate delays

4. **Knowledge Review**
   - Periodically review learned patterns
   - Verify knowledge quality
   - Remove/correct undesired information

## 📚 Advanced Topics

### Custom Learning Sources
```python
# In config.py
LEARNING_SOURCES = [
    "https://yoursource.com",
    "https://anotherource.com",
]
```

### Custom Reasoning
Edit `src/reasoning_engine.py` to add custom reasoning logic.

### Extending Knowledge Types
Modify `src/knowledge_base.py` to support new data types.

### Custom Skills
Add skill tracking in `src/learning_engine.py`.

## 🎓 Learning from This Project

Key concepts demonstrated:
- Autonomous agent architecture
- Knowledge representation
- Self-improvement mechanisms
- Persistent memory management
- Web data acquisition
- Goal-oriented planning
- Skills development tracking
- Performance metrics

## 📞 Support

For issues:
1. Check the logs: `logs/ai_evolution.log`
2. Review configuration: `config.py`
3. Verify dependencies: `pip list`
4. Check README.md for comprehensive docs

## 🎉 Next Steps

1. **Run a quick test:**
   ```bash
   python main.py
   # Choose interactive mode
   # Try: query, status, exit
   ```

2. **Let it learn:**
   ```bash
   python main.py
   # Choose autonomous mode
   # Set iterations to 10
   # Monitor progress
   ```

3. **Analyze results:**
   ```bash
   # Check data/
   # Review logs/ai_evolution.log
   # View final summary
   ```

---

**Happy learning! Your AI is ready to evolve! 🚀**
