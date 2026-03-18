# Troubleshooting Guide

Solutions to common problems.

## Installation Issues

### Python 3.8+ Not Found
```bash
# Check Python version
python --version

# Should show: Python 3.x.x (x >= 8)
```

**Solution**: Download from [python.org](https://www.python.org/downloads/)

---

### ModuleNotFoundError: No module named 'X'

```bash
# Re-install dependencies
pip install -r requirements.txt --force-reinstall

# Or specific module
pip install torch transformers numpy
```

---

### Permission Denied: setup.sh

**Linux/Mac:**
```bash
chmod +x setup.sh
./setup.sh
```

**Windows**: Use `setup.bat` instead

---

## Runtime Issues

### "Port Already in Use"

**Windows:**
```bash
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

**Linux/Mac:**
```bash
lsof -i :8000
kill -9 <PID>
```

Or change port in `src/config.py`:
```python
PORT = 9000  # Changed from 8000
```

---

### Out of Memory Errors

**Solution 1: Reduce batch size**
```bash
# Edit src/config.py
BATCH_SIZE = 8  # Reduce from 32
```

**Solution 2: Increase virtual memory**
```bash
# Windows: System → Advanced settings → Performance
# Linux: Add swap space
sudo fallocate -l 4G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

---

### Slow Performance

**Solution 1: Check resource usage**
```bash
# Linux/Mac
top

# Windows
tasklist /v
```

**Solution 2: Reduce crawl depth**
```python
# src/config.py
MAX_CRAWL_DEPTH = 2  # Reduce from 3
BATCH_SIZE = 16      # Reduce from 32
```

---

### Network/Crawling Issues

**"Connection timeout"**
```bash
# Check internet
ping google.com

# Increase timeout in src/config.py
CRAWL_TIMEOUT = 30  # seconds (increased from 10)
```

**"SSL certificate error"**
```python
# src/config.py - CAREFUL with this
VERIFY_SSL = False  # Only if absolutely necessary
```

---

## Test Failures

### Some Tests Fail

```bash
# Run with verbose output
pytest tests/ -vv

# Run single test file
pytest tests/unit/test_core/test_knowledge_base.py -v

# Run specific test
pytest tests/unit/test_core/test_knowledge_base.py::TestKnowledgeBase::test_search -v
```

**Most common**: Missing test dependencies
```bash
pip install pytest pytest-asyncio pytest-cov
```

---

## Type Checking Issues

### Mypy Errors

```bash
# Run mypy to see errors
mypy src/ --config-file=mypy.ini --show-error-codes

# Fix specific file
mypy src/core/web_crawler.py
```

**Common**: Missing type stubs
```bash
# Install stubs
pip install types-requests types-PyYAML
```

---

## Performance Degradation

### System Slowing Down Over Time

**Cause**: Cache/logs growing  
**Solution**:
```bash
# Clear old caches
rm -rf data/cache/*
rm -rf logs/*.log

# Or rotate logs
python scripts/rotate_logs.py
```

---

### High CPU Usage

```bash
# Check what's running
ps aux | grep python  # Linux/Mac
tasklist /v | grep python  # Windows

# Reduce concurrent operations
# src/config.py
MAX_WORKERS = 2  # Reduce from 8
```

---

## Data Issues

### Lost Data After Restart

Check if data is saved:
```bash
ls -la data/memory/
ls -la data/knowledge/
```

**Fix**: Ensure directories exist
```bash
mkdir -p data/{memory,knowledge,cache}
```

---

### Corrupted JSON Files

**Symptoms**: "JSONDecodeError" when starting

**Solution**:
```bash
# Backup corrupted file
cp data/memory/sessions.json data/memory/sessions.json.backup

# Clear corrupted data
rm data/memory/*.json
```

System will rebuild on next start.

---

## Getting Help

### Enable Debug Logging

```python
# src/config.py
LOG_LEVEL = "DEBUG"  # More verbose logging
```

### Check Logs

```bash
# View recent errors
grep "ERROR" logs/*.log

# Full debug output
tail -200 logs/debug.log
```

### System Diagnostics

```bash
# Run diagnostic
python scripts/verify_installation.py

# Detailed system status
python -m src.main --status
```

---

## Still Stuck?

1. **Check documentation**: [../guide/](../guide/)
2. **Run tests**: `pytest tests/ -v`
3. **Check logs**: `logs/system.log`
4. **Search issues**: GitHub issues or documentation
5. **Get help**: See [CONTRIBUTING.md](../development/contributing.md)

---

**Common error not listed?**  
Check the [reference docs](../reference/) or file an issue.
