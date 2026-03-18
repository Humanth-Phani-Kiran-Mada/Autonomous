# Detailed Setup Guide

Complete, step-by-step setup for all platforms.

## Prerequisites

- **Python 3.8 or higher** installed
- **Git** installed (for version control)
- **Virtual environment support** (built-in with Python 3.3+)
- **4 GB RAM** recommended
- **2 GB disk space**

---

## Windows Setup

### 1. Install Python
- Download from [python.org](https://www.python.org/downloads/)
- **Important**: Check "Add Python to PATH" during installation
- Verify: Open CMD and run `python --version`

### 2. Clone/Extract Project
```bash
cd C:\Users\YourUsername\Documents
git clone <repo-url>
cd autonomous-ai-system
```

### 3. Create Virtual Environment
```bash
python -m venv venv
```

### 4. Activate Virtual Environment
```bash
venv\Scripts\activate
```

**You should see `(venv)` prefix in command line**

### 5. Upgrade pip
```bash
python -m pip install --upgrade pip
```

### 6. Install Dependencies
```bash
pip install -r requirements.txt
```

This installs: PyTorch, Transformers, scikit-learn, etc.

### 7. Configuration
```bash
copy .env.example .env
# Edit .env with Notepad if needed
```

### 8. Create Directories
```bash
mkdir data\memory data\knowledge data\cache
mkdir logs
```

### 9. Test Installation
```bash
python -c "import torch; print(torch.__version__)"
```

---

## Linux/Mac Setup

### 1. Install Python (if needed)

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install python3.8 python3.8-venv python3-pip
```

**Mac (with Homebrew):**
```bash
brew install python@3.8
```

### 2. Clone/Extract Project
```bash
cd ~/Documents
git clone <repo-url>
cd autonomous-ai-system
```

### 3. Create Virtual Environment
```bash
python3.8 -m venv venv
```

### 4. Activate Virtual Environment
```bash
source venv/bin/activate
```

**You should see `(venv)` prefix in terminal**

### 5. Upgrade pip
```bash
pip install --upgrade pip setuptools wheel
```

### 6. Install Dependencies
```bash
pip install -r requirements.txt
```

### 7. Configuration
```bash
cp .env.example .env
# Edit .env if needed: nano .env or vim .env
```

### 8. Create Directories
```bash
mkdir -p data/memory data/knowledge data/cache
mkdir -p logs
```

### 9. Make Setup Script Executable
```bash
chmod +x setup.sh
```

### 10. Test Installation
```bash
python -c "import torch; print(torch.__version__)"
```

---

## Docker Setup (Optional)

If you prefer containerization:

```dockerfile
FROM python:3.8-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

CMD ["python", "-m", "src.main"]
```

Build and run:
```bash
docker build -t autonomous-ai .
docker run -it autonomous-ai
```

---

## Troubleshooting Setup

### Virtual Environment Not Activating

**Windows:**
```bash
# Try PowerShell instead of CMD
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
venv\Scripts\Activate.ps1
```

**Linux/Mac:**
```bash
source venv/bin/activate
# Verify with: which python
```

### Pip Install Errors

```bash
# Clear pip cache
pip cache purge

# Upgrade pip first
pip install --upgrade pip

# Try install again
pip install -r requirements.txt
```

### Missing CUDA (GPU)

```bash
# This is fine, CPU works too
# PyTorch will auto-detect available hardware
python -c "import torch; print(f'CUDA: {torch.cuda.is_available()}')"
```

### Port Already in Use

If you get "Address already in use" error:

**Windows:**
```bash
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

**Linux/Mac:**
```bash
lsof -i :5000
kill -9 <PID>
```

---

## Verify Everything Works

Run this comprehensive test:

```bash
# Activate venv first
source venv/bin/activate  # Linux/Mac
# OR
venv\Scripts\activate  # Windows

# Run test suite
pytest tests/ -v

# Run type checking
mypy src/ --config-file=mypy.ini

# Quick system test
python -m src.main --version
```

---

## Environment Configuration

Edit `.env` to customize:

```bash
# Logging
LOG_LEVEL=INFO

# Web Crawler
MAX_CRAWL_DEPTH=3
MAX_PAGES=100

# Learning
LEARNING_BATCH_SIZE=32
LEARNING_RATE=0.001

# Autonomous Mode
AUTONOMOUS_MODE_ENABLED=True
AUTONOMOUS_ITERATIONS=10
```

See [reference/configuration.md](../reference/configuration.md) for all options.

---

## Next Steps After Setup

1. ✅ Installation complete
2. 👉 Run the system: `python -m src.main`
3. 📖 Read [architecture.md](../guide/architecture.md)
4. 🧪 Run tests: `pytest tests/ -v`
5. 🔧 Customize [src/config.py](../../src/config.py)

---

See [01-quickstart.md](01-quickstart.md) for quick start or [troubleshooting.md](04-troubleshooting.md) for help.
