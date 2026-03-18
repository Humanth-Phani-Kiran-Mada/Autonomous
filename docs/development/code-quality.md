# Code Quality Standards

Development standards for the Autonomous AI System.

## 1. Code Style

### Python Style Guide (PEP 8)
- 4-space indentation
- Max line length: 100 characters
- Use lowercase with underscores for variables
- Use UPPERCASE for constants

### Formatting
```bash
# Format code
black src/

# Check formatting
black --check src/
```

---

## 2. Type Hints

Required for all public methods:

```python
def process_data(items: List[str], count: int = 10) -> Dict[str, int]:
    """Process items and return statistics."""
    return {"count": len(items), "processed": count}
```

Check with mypy:
```bash
mypy src/ --config-file=mypy.ini
```

---

## 3. Documentation

Every module, class, and public function needs docs:

```python
def calculate_relevance(query: str, document: str) -> float:
    """
    Calculate relevance score between query and document.
    
    Uses TF-IDF scoring for fast retrieval.
    
    Args:
        query: Search query string
        document: Document text
        
    Returns:
        Relevance score between 0.0 and 1.0
        
    Raises:
        ValidationException: If query or document is empty
        
    Example:
        >>> score = calculate_relevance("AI", "Artificial Intelligence")
        >>> print(score)  # 0.92
    """
    # Implementation...
```

---

## 4. Error Handling

Use custom exceptions:

```python
from src.infrastructure.exceptions import ValidationException

def validate_input(data):
    if not data:
        raise ValidationException(
            "Input data cannot be empty",
            error_code="INPUT_001"
        )
```

---

## 5. Testing

Write tests for new code:

```python
import pytest
from src.core import KnowledgeBase

class TestKnowledgeBase:
    def test_store_and_retrieve(self):
        kb = KnowledgeBase()
        kb.store("test content")
        result = kb.search("content")
        assert len(result) > 0
    
    def test_invalid_query(self):
        kb = KnowledgeBase()
        with pytest.raises(ValidationException):
            kb.search("")
```

Run tests:
```bash
pytest tests/ -v
pytest tests/unit/test_core/ -v
```

---

## 6. Performance

Don't block operations:

```python
# Good - async
async def fetch_data(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            return await resp.text()

# Bad - blocks
def fetch_data(url):
    response = requests.get(url)  # Blocks!
    return response.text()
```

Use decorators for monitoring:

```python
from src.infrastructure.utilities import measure_performance

@measure_performance
def expensive_operation():
    # Operation is timed automatically
    pass
```

---

## 7. Logging

Use logger, not print():

```python
from src.logger import logger

# Good
logger.info("Starting crawl")
logger.error("Failed to parse", extra={"url": url})

# Bad
print("Starting crawl")  # Don't use this!
```

---

## 8. Git Workflow

### Commit Messages
```
<Type>: <Subject>

<Body>

Fixes: #123
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

### Branch Naming
- `feature/add-attention-system`
- `fix/memory-leak`
- `docs/api-reference`

### Before Pushing
```bash
pytest tests/ -v
mypy src/
black src/
```

---

## 9. Code Review Checklist

- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] No breaking changes
- [ ] No hardcoded values
- [ ] Error handling present
- [ ] Performance acceptable
- [ ] No unused imports
- [ ] Follows PEP 8

---

## 10. Naming Conventions

| Item | Convention | Example |
|------|-----------|---------|
| Modules | lowercase_with_underscores | `web_crawler.py` |
| Classes | PascalCase | `WebCrawler` |
| Methods | lowercase_with_underscores | `fetch_page()` |
| Constants | UPPERCASE_WITH_UNDERSCORES | `MAX_RETRIES = 3` |
| Private | Prefix with _ | `_internal_method()` |

---

See: [contributing.md](contributing.md), [review-checklist.md](review-checklist.md)
