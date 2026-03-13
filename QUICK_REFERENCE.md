# Quick Start: Using the Code Quality Improvements

A quick reference guide for developers using the new standards.

## 1. Exception Handling

```python
from src.exceptions import (
    ValidationException,
    KnowledgeBaseException,
    CrawlerException,
    CircuitBreakerOpenException
)

try:
    kb.add_knowledge(content, source, kind)
except ValidationException as e:
    # Input was invalid
    print(f"Error: {e.message}")
    print(f"Code: {e.error_code}")
except KnowledgeBaseException as e:
    # KB operation failed
    print(f"KB Error: {e.message}")
    print(f"Context: {e.context}")
except CircuitBreakerOpenException:
    # External service is failing, try again later
    retry_later()
```

---

## 2. Type Safety & IDE Support

```python
from src.types_and_constants import (
    KnowledgeEntry,
    Goal,
    SystemConstants,
    GoalStatus
)
from typing import List, Dict, Any

# TypedDict provides IDE autocomplete
entry: KnowledgeEntry = {
    "id": "KB_123",
    "content": "...",
    # IDE shows all valid keys ↓
    "source": "https://...",
    "type": "article",
    "created_at": "2026-03-13T...",
    "accessed_count": 0,
    "relevance_score": 0.85,
    "metadata": {}
}

# Enums prevent invalid values
goal: Goal = {
    "status": GoalStatus.IN_PROGRESS,  # Type checker validates!
    # "status": "invalid"  # ← Type checker warns!
}

# Use constants instead of magic numbers
if entry["relevance_score"] > SystemConstants.EXPERT_THRESHOLD:
    print("Expert-level knowledge")
```

---

## 3. Input Validation

### Simple Validation
```python
from src.validators import (
    validate_url,
    validate_content,
    validate_priority
)

# Individual validators
url = validate_url("https://example.com")  # Raises ValidationException if bad
content = validate_content("Some text", min_length=10)
priority = validate_priority(0.85)
```

### Batch Validation
```python
from src.validators import ValidationChain

# Chain multiple validations
result = (ValidationChain()
    .validate(url, validate_url, "URL")
    .validate(content, validate_content, "Content")
    .validate(priority, validate_priority, "Priority")
    .execute())

url, content, priority = result
```

---

## 4. Resilience: Decorators

### Retry with Backoff
```python
from src.utilities import retry_with_backoff
import asyncio

# Auto-retries with increasing delays
@retry_with_backoff(max_retries=3, initial_delay=1.0)
async def fetch_data(url):
    # Retries: 1s, 2s, 4s delays
    response = await fetch(url)
    return response

# Sync version (works the same)
@retry_with_backoff(max_retries=3)
def process_file(path):
    return open(path).read()
```

### Performance Monitoring
```python
from src.utilities import measure_performance

@measure_performance
def expensive_operation():
    # Auto-logs: "expensive_operation completed in 2.345s"
    # Or: "expensive_operation failed after 1.234s: Error"
    pass
```

### Caching
```python
from src.utilities import cached

@cached(ttl_seconds=300)
def get_data(key):
    # First call: computes and caches
    # Next calls within 5 min: returns cached result
    # After 5 min: computes again
    return expensive_fetch(key)
```

### Resource Limits
```python
from src.utilities import ensure_resource_limits

@ensure_resource_limits(max_memory_mb=512, timeout_seconds=30)
async def large_operation():
    # Enforces timeout
    # Raises TimeoutException if exceeds 30s
    pass
```

---

## 5. Circuit Breaker Pattern

```python
from src.utilities import get_circuit_breaker

# Prevents cascading failures
crawler_cb = get_circuit_breaker("crawler")

for url in urls:
    try:
        # Circuit breaker opens after 5 failures
        # Then rejects requests to prevent storms
        crawler_cb.call(fetch_page, url)
    except CircuitBreakerOpenException:
        # Service is failing, skip for now
        logger.warning(f"Skipping {url}: circuit breaker open")
        continue
```

---

## 6. Knowledge Base with All Improvements

```python
from src.knowledge_base import KnowledgeBase
from src.exceptions import ValidationException, KnowledgeBaseException

kb = KnowledgeBase()

# All inputs validated automatically
try:
    kid = kb.add_knowledge(
        content="Comprehensive article about machine learning",
        source="https://arxiv.org/papers/ml-guide",
        knowledge_type="article",  # Type validated
        metadata={"difficulty": "advanced"}
    )
    logger.info(f"Added knowledge: {kid}")
except ValidationException as e:
    logger.error(f"Invalid input: {e.message}")
except KnowledgeBaseException as e:
    logger.error(f"KB error: {e.error_code} - {e.message}")

# Search with explicit error handling
try:
    results = kb.search("machine learning", top_k=5)
    for result in results:
        print(f"{result['type']}: {result['similarity_score']:.2f}")
except KnowledgeBaseException as e:
    logger.error(f"Search failed: {e.message}")

# Check statistics
stats = kb.get_statistics()
print(f"Total entries: {stats['total_entries']}")
print(f"Types: {stats['types']}")
```

---

## 7. Checking Type Safety with mypy

```bash
# Install mypy
pip install mypy

# Check your code
mypy src/your_module.py

# Fix type errors
# mypy will tell you exactly where types don't match
```

---

## 8. Running Tests

```bash
# Install pytest
pip install pytest

# Run all tests
pytest tests/

# Run specific test
pytest tests/test_knowledge_base.py::TestKnowledgeBaseOperations::test_add_knowledge_success

# Verbose output
pytest tests/ -v

# With coverage
pytest tests/ --cov=src
```

---

## 9. Common Patterns

### Pattern 1: Safe API Call
```python
from src.utilities import retry_with_backoff, measure_performance
from src.exceptions import CrawlerException

@retry_with_backoff(max_retries=3)
@measure_performance
async def fetch_with_safety(url):
    try:
        result = await fetch(url)
        return result
    except Exception as e:
        raise CrawlerException(
            f"Failed to fetch {url}: {e}",
            error_code="FETCH_FAILED",
            context={"url": url}
        )
```

### Pattern 2: Expensive Operation with Caching
```python
from src.utilities import cached, measure_performance

@measure_performance
@cached(ttl_seconds=3600)
def compute_embeddings(texts):
    # First call: computes and logs time
    # Later calls: returns cached result instantly
    return model.encode(texts)
```

### Pattern 3: Batch Operations
```python
from src.validators import ValidationChain, validate_url

urls = [...]

# Validate all first
try:
    validated = (ValidationChain()
        .validate(urls[0], validate_url, "URL 1")
        .validate(urls[1], validate_url, "URL 2")
        .execute())
except ValidationException as e:
    logger.error(f"Validation failed: {e.message}")
    return

# Then process
for url in validated:
    try:
        process(url)
    except Exception as e:
        logger.error(f"Processing failed: {e}")
```

---

## 10. Creating New Components Following Standards

```python
"""
New component following all standards
"""
from typing import Optional, Dict, Any, List
from src.exceptions import AutonomousAIException
from src.validators import validate_content
from src.utilities import measure_performance, retry_with_backoff
from src.logger import logger


class CustomException(AutonomousAIException):
    """This component's specific exceptions"""
    pass


class MyComponent:
    """
    Brief description of what this component does.
    
    Longer description with implementation details.
    
    Attributes:
        state: Current component state
        metrics: Performance metrics
    """
    
    def __init__(self):
        """Initialize component"""
        self.state = {}
        self.metrics = []
        logger.info("MyComponent initialized")
    
    @retry_with_backoff(max_retries=2)
    @measure_performance
    def process(self, data: str) -> Dict[str, Any]:
        """
        Process input data.
        
        Args:
            data: Input to process
        
        Returns:
            Processing result
        
        Raises:
            ValidationException: If data invalid
            CustomException: If processing fails
        
        Example:
            >>> component = MyComponent()
            >>> result = component.process("input")
        """
        # Validate input
        data = validate_content(data, min_length=1)
        
        try:
            # Process with error handling
            result = self._process_internal(data)
            self.metrics.append({"success": True})
            return result
        except Exception as e:
            self.metrics.append({"success": False, "error": str(e)})
            raise CustomException(
                f"Processing failed: {e}",
                error_code="PROCESS_FAILED"
            )
    
    def _process_internal(self, data: str) -> Dict[str, Any]:
        """Internal processing logic"""
        return {"processed": data, "length": len(data)}
```

---

## 11. Common Issues & Solutions

### Issue: "No attribute error" when using TypedDict
```python
# Wrong
entries = kb.entries
for e in entries:
    print(e["unknown_field"])  # ← Type checker should catch this

# Right
entry: KnowledgeEntry = kb.entries[0]
print(entry["content"])  # ✅ Type checker verifies key exists
```

### Issue: Catching wrong exception
```python
# Wrong
try:
    kb.add_knowledge(...)
except Exception:  # ← Too generic, won't help debug
    logger.error("Failed")

# Right
try:
    kb.add_knowledge(...)
except ValidationException as e:
    logger.error(f"Invalid input: {e.message}")
except KnowledgeBaseException as e:
    logger.error(f"KB error: {e.error_code}")
```

### Issue: Magic numbers in code
```python
# Wrong
if skill > 0.9:  # What does 0.9 mean?
    print("Expert")

# Right
if skill > SystemConstants.EXPERT_THRESHOLD:  # Clear intent
    print("Expert")
```

---

## 12. Performance Tips

```python
# Use @cached for expensive operations
@cached(ttl_seconds=300)
def expensive_compute():
    return compute()  # Only runs every 5 minutes

# Use @measure_performance to find bottlenecks
@measure_performance
def slow_operation():
    # Logs actual execution time
    pass

# Use circuit breaker for external services
cb = get_circuit_breaker("api")
try:
    cb.call(fetch_external_data)
except CircuitBreakerOpenException:
    use_cached_fallback()  # Graceful degradation
```

---

## Need More Help?

- **Exceptions**: See `src/exceptions.py`
- **Decorators**: See `src/utilities.py`
- **Types**: See `src/types_and_constants.py`
- **Validation**: See `src/validators.py`
- **Examples**: See `EXAMPLES_AND_USAGE.py`
- **Detailed Guide**: See `CODE_QUALITY_IMPROVEMENTS.md`
- **Standards**: See `IMPROVEMENT_STANDARDS.md`

---

**Quick Reference Created**: March 13, 2026  
**Standards Version**: 1.0  
**Status**: Production Ready ✅
