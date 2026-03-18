# Contributing Guide

How to contribute to the Autonomous AI System.

## Getting Started

1. Fork the repository
2. Clone locally: `git clone <your-fork>`
3. Create branch: `git checkout -b feature/your-feature`
4. Make changes
5. Test locally
6. Push to branch
7. Create pull request

---

## Development Setup

```bash
# Clone
git clone <repo-url>
cd autonomous-ai-system

# Setup virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# OR
venv\Scripts\activate  # Windows

# Install dev dependencies
pip install -r requirements.txt
pip install pytest black mypy pylint

# Create feature branch
git checkout -b feature/your-feature
```

---

## Making Changes

### Add a New Feature

1. Create feature branch
2. Write tests first (TDD)
3. Implement feature
4. Add documentation
5. Pass all checks

### Fix a Bug

1. Create fix branch
2. Write test that reproduces bug
3. Fix the bug
4. Verify test passes
5. Update documentation if needed

### Update Documentation

1. Find correct file in docs/
2. Make changes
3. Use clear, concise language
4. Include examples if applicable

---

## Testing

### Run All Tests
```bash
pytest tests/ -v
```

### Run Specific Tests
```bash
pytest tests/unit/test_core/ -v
pytest tests/unit/test_core/test_knowledge_base.py::TestKnowledgeBase::test_search -v
```

### Add Tests for Your Feature
```python
# tests/unit/test_core/test_my_feature.py

import pytest
from src.core import MyFeature

class TestMyFeature:
    def test_basic_functionality(self):
        feature = MyFeature()
        result = feature.do_something()
        assert result is not None
    
    def test_error_handling(self):
        feature = MyFeature()
        with pytest.raises(ValidationException):
            feature.do_something_invalid()
```

---

## Code Quality

### Format Code
```bash
black src/
```

### Check Types
```bash
mypy src/ --config-file=mypy.ini
```

### Lint Code
```bash
pylint src/ --disable=all --enable=E
```

### Run All Checks
```bash
pytest tests/ -v
black --check src/
mypy src/
```

---

## Documentation

### Update README
- Top-level overview
- Installation instructions
- Quick start guide
- Links to full docs

### Update Getting Started
- Step-by-step instructions
- Screenshots/examples
- Troubleshooting

### Update API Docs
- Method signatures
- Parameter descriptions
- Return values
- Exception handling

### Example Format
```python
def my_function(param1: str, param2: int = 10) -> dict:
    """
    Short description of what function does.
    
    Longer description explaining the algorithm
    or behavior if needed.
    
    Args:
        param1: Description of param1
        param2: Description of param2, defaults to 10
    
    Returns:
        Dictionary with keys:
        - 'result': The actual result...
        - 'status': Success/failure status...
    
    Raises:
        ValueError: If param1 is invalid
        TypeError: If param2 is not an integer
    
    Example:
        >>> result = my_function("test", 5)
        >>> print(result['status'])
        "success"
    """
```

---

## Commit Guidelines

### Good Commit
```
feat: Add attention system for resource allocation

- Implement AttentionSystem class
- Add focus switching logic
- Add unit tests (18 test cases)
- Add documentation and examples

Fixes: #123
```

### Bad Commit
```
Update stuff
```

### Commit Types
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Style changes (no code change)
- `refactor`: Code restructuring
- `test`: Test additions
- `chore`: Build/tooling changes

---

## Pull Request Process

1. **Update from main**
   ```bash
   git fetch origin
   git rebase origin/main
   ```

2. **Verify Tests Pass**
   ```bash
   pytest tests/ -v
   ```

3. **Run Quality Checks**
   ```bash
   black src/
   mypy src/
   ```

4. **Push to Your Fork**
   ```bash
   git push origin feature/your-feature
   ```

5. **Create Pull Request**
   - Clear title
   - Describe changes
   - Link any issues
   - Screenshots if UI change

---

## Code Review

### What Reviewers Look For
- Correctness
- Code quality
- Test coverage
- Documentation
- Performance
- Security

### Review Comments
- Be respectful
- Suggest improvements
- Ask questions if unclear
- Praise good code


### Responding to Reviews
- Address all comments
- Push updates to same branch
- Don't force push to reviewed branch
- Thank reviewers

---

## Areas for Contribution

### High Priority
- [ ] Expand test coverage
- [ ] Add performance tests
- [ ] Improve documentation
- [ ] Fix reported bugs
- [ ] Add examples

### Medium Priority
- [ ] Code refactoring
- [ ] Performance optimization
- [ ] Add logging
- [ ] Improve error messages

### Low Priority
- [ ] Code style
- [ ] Comments
- [ ] Documentation polish

---

## Community

- **Questions?** Check docs first
- **Bug report?** Use GitHub Issues
- **Feature request?** Open GitHub Issue
- **Questions?** Start GitHub Discussion

---

See: [code-quality.md](code-quality.md), [review-checklist.md](review-checklist.md)
