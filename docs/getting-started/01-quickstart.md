# Autonomous AI System - Getting Started Guide

Welcome! This guide will help you get the Autonomous AI System up and running in 5 minutes.

## 🚀 Quick Start (5 Minutes)

### Step 1: Setup Environment
```bash
# Linux/Mac
./setup.sh

# Windows  
setup.bat
```

### Step 2: Activate Virtual Environment
```bash
# Linux/Mac
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### Step 3: Run the System
```bash
python -m src.main
```

That's it! You'll be prompted to choose between Autonomous or Interactive mode.

---

## 💻 Installation (Complete)

### Requirements
- **Python**: 3.8 or higher
- **RAM**: 4 GB minimum
- **Disk**: 2 GB free
- **Internet**: Required for web crawling

### Step-by-Step Setup

#### 1. Clone or Navigate to Project
```bash
cd /path/to/autonomous-ai-system
```

#### 2. Create Virtual Environment
```bash
python3 -m venv venv
```

#### 3. Activate Virtual Environment

**Linux/Mac:**
```bash
source venv/bin/activate
```

**Windows:**
```bash
venv\Scripts\activate
```

#### 4. Upgrade pip
```bash
pip install --upgrade pip setuptools wheel
```

#### 5. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 6. Configure Environment
```bash
cp .env.example .env
# Edit .env with your specific settings if needed
```

#### 7. Create Data Directories
```bash
mkdir -p data/memory data/knowledge data/cache
mkdir -p logs
```

---

## ▶️ Running the System

### Autonomous Mode (Recommended)
```bash
python -m src.main
# Select: Autonomous Mode
# Enter desired iterations (e.g., 10)
```

The system will automatically:
- Crawl the web for knowledge
- Learn from discovered content
- Reason about problems
- Improve its own capabilities
- Save progress

### Interactive Mode
```bash
# Edit src/config.py: AUTONOMOUS_MODE_ENABLED = False
python -m src.main
```

Available commands:
- `learn` - Run learning cycle
- `crawl` - Web crawling cycle
- `reason` - Reasoning cycle
- `improve` - Self-improvement cycle
- `query <question>` - Ask a question
- `status` - Show agent status
- `auto <iterations>` - Run iterations in sequence
- `exit` - Exit program

---

## ✅ Verify Installation

```bash
# Check Python version (should be 3.8+)
python --version

# Check key dependencies installed
pip list | grep -E "torch|transformers|aiohttp|beautifulsoup"

# Run tests
pytest tests/ -v

# Check type safety
mypy src/ --config-file=mypy.ini
```

---

## 📋 Common Issues & Solutions

### Issue: "Python 3.8 not found"
**Solution**: Install Python 3.8+ from [python.org](https://www.python.org)

### Issue: "ModuleNotFoundError: No module named 'X'"
**Solution**: Run `pip install -r requirements.txt` again

### Issue: "Permission denied: setup.sh"
**Solution**: Run `chmod +x setup.sh` then `./setup.sh`

### Issue: "CUDA not available"
**Solution**: CPU mode works fine, PyTorch will auto-detect

---

## 📚 Next Steps

1. **Read Architecture**: See [architecture.md](../guide/architecture.md)
2. **Run Examples**: Check [examples.md](../guide/examples.md)
3. **Configure**: Customize [src/config.py](../../src/config.py)
4. **Run Tests**: `pytest tests/ -v`
5. **Join Development**: See [CONTRIBUTING.md](../development/contributing.md)

---

**Need help?** Check [troubleshooting.md](04-troubleshooting.md) or the [reference docs](../reference/).
