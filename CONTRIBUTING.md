# Contributing to Autonomous AI System

First off, thank you for considering contributing to the Autonomous AI System! It's people like you that make this project great.

## Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the issue list as you might find the issue already exists. When you create a bug report, please include as many details as possible:

- **Use a clear and descriptive title**
- **Describe the exact steps which reproduce the problem**
- **Provide specific examples to demonstrate the steps**
- **Describe the behavior you observed after following the steps**
- **Explain which behavior you expected to see and why**
- **Include screenshots/logs if applicable**

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, please include:

- **Use a clear and descriptive title**
- **Provide a step-by-step description of the suggested enhancement**
- **Provide specific examples to demonstrate the steps**
- **Describe the current behavior vs. expected behavior**
- **Explain why this enhancement would be useful**

### Pull Requests

Please follow these guidelines:

1. **Branch naming**: Use `feature/your-feature` or `fix/your-fix`
2. **One feature per PR**: Keep PRs focused and atomic
3. **Write good commit messages**: Use conventional commits format
4. **Include tests**: Add tests for new features
5. **Update documentation**: Update README and docstrings
6. **Code style**: Follow PEP 8 and use black, mypy, flake8

#### Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: A new feature
- `fix`: A bug fix
- `docs`: Documentation only changes
- `style`: Changes that don't affect code meaning
- `refactor`: Code change without feature/bug changes
- `perf`: Performance improvement
- `test`: Adding or updating tests
- `chore`: Changes to build process or dependencies

**Example:**
```
feat(core): implement knowledge cache optimization

Add LRU cache to knowledge base searches to reduce
latency for repeated queries. Implements TTL-based
expiration for cache entries.

Closes #42
```

### Development Setup

1. **Fork the repository**
2. **Clone your fork**: `git clone https://github.com/your-username/Autonomous.git`
3. **Create virtual environment**: `python -m venv venv`
4. **Activate venv**: `source venv/bin/activate` (or `venv\Scripts\activate` on Windows)
5. **Install dependencies**: `pip install -r requirements.txt`
6. **Install dev dependencies**: `pip install pytest black mypy flake8`

### Testing Requirements

All contributions must include:

- **Unit tests** for new functions/classes
- **Integration tests** for new features
- **No breaking changes** to existing APIs
- **All tests passing**: `pytest tests/ -v`

### Code Style Guidelines

#### Type Hints
```python
# Good - annotate parameters and return types
def search_knowledge(
    query: str,
    top_k: int = 5
) -> List[Dict[str, Any]]:
    """Search knowledge base for similar items."""
    pass
```

#### Docstrings
```python
def learn_from_content(
    content: str,
    source: str,
    weight: float = 1.0
) -> bool:
    """Extract and learn patterns from content.
    
    Args:
        content: Raw text content to learn from
        source: Source identifier for tracking
        weight: Learning weight (0.0-1.0)
        
    Returns:
        True if learning was successful
        
    Raises:
        ValidationException: Invalid content
        LearningException: Learning processing failed
    """
    pass
```

#### Error Handling
```python
# Good - specific exceptions with context
from src.utils.exceptions import ValidationException

try:
    result = kb.search(query)
except ValidationException as e:
    logger.error(f"Invalid search query: {e}")
    raise
```

### Module Organization

When adding new files:

1. **Determine the appropriate module** (core, advanced, infrastructure, integration, utils)
2. **Add to correct src/ subdirectory**
3. **Update `__init__.py`** if adding new public API
4. **Update documentation** in README.md

### Performance Considerations

- Avoid blocking operations in async code
- Use batch processing for multiple items
- Profile code with large datasets
- Consider memory usage for knowledge base operations
- Implement caching for expensive operations

### Testing Checklist

- [ ] Unit tests written and passing
- [ ] Integration tests verify new behavior
- [ ] Code coverage maintained or improved
- [ ] No new warnings from flake8/mypy
- [ ] Black formatting applied
- [ ] Documentation updated
- [ ] No hardcoded values (use config)
- [ ] Error handling implemented
- [ ] Type hints added
- [ ] Docstrings added

### Documentation Checklist

- [ ] README updated if needed
- [ ] Code docstrings added/updated
- [ ] Type hints included
- [ ] Examples provided for new APIs
- [ ] Configuration options documented

## Recognition

Contributors will be recognized in:
1. GitHub contributors page
2. Release notes
3. Maintainer communication

## Questions?

Feel free to ask questions by:
- Creating a GitHub Discussion
- Opening an issue with [QUESTION] tag
- Emailing: humanathphanikiran@gmail.com

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for helping make the Autonomous AI System better! 🚀
