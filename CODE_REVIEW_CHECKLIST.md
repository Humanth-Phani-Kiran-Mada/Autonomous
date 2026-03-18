# Code Review Checklist

Use this checklist before committing changes to the Autonomous AI System.

## Pre-Commit Checks (Self Review)

### Code Quality
- [ ] All linting passes: `pylint src/`
- [ ] No type errors: `mypy src/`
- [ ] Code formatted: `black src/`
- [ ] No unused imports
- [ ] No hardcoded credentials/secrets
- [ ] No print() statements (use logger instead)

### Documentation
- [ ] Function docstrings added (Google style)
- [ ] Complex logic has explanatory comments
- [ ] Type hints on all function parameters
- [ ] Error conditions documented
- [ ] Example usage in docstring if applicable

### Testing
- [ ] New functions have unit tests
- [ ] All tests pass: `pytest tests/ -v`
- [ ] Test coverage maintained or improved
- [ ] Edge cases tested
- [ ] Error paths tested

### Error Handling
- [ ] Specific exceptions used (not generic Exception)
- [ ] Exceptions have error codes
- [ ] Recovery strategies documented
- [ ] No bare except clauses
- [ ] Timeout handling present in async code

### Performance
- [ ] No N+1 queries
- [ ] Caching applied for repeated calls
- [ ] Async/await used appropriately
- [ ] Resource limits enforced
- [ ] Memory leaks checked in long-running code

## Commit Message Format

```
<Type>: <Subject>

<Body>

<Footer>
```

**Types**: feat, fix, docs, style, refactor, test, chore

**Example**:
```
feat: Add validation for crawler URLs

- Implemented URL validation with protocol checking
- Added KnowledgeBaseException for validation errors
- Updated crawler to validate URLs before fetching

Fixes: #123
```

## Modified Files Checklist

For each modified file:
- [ ] Reviewed all changes
- [ ] Changes are minimal and focused
- [ ] No unrelated formatting changes
- [ ] Breaking changes documented
- [ ] Backwards compatibility maintained

## Specific Component Checklists

### Adding a New Module
- [ ] File follows naming convention: lowercase_with_underscores.py
- [ ] Placed in correct directory (src/ vs tests/)
- [ ] Has module docstring
- [ ] Imports organized (stdlib, third-party, local)
- [ ] All public functions documented
- [ ] __init__.py updated if needed

### Modifying Core Components
- [ ] Changes won't break existing code
- [ ] Performance impact assessed
- [ ] Memory impact assessed
- [ ] Logging added for debugging
- [ ] Metrics collected for monitoring

### Adding External Dependencies
- [ ] Justified in commit message
- [ ] Added to requirements.txt
- [ ] Version pinned (no floating versions)
- [ ] License compatible
- [ ] Security implications checked

## Git Hygiene

- [ ] Commit is atomic (single logical change)
- [ ] No merge conflicts
- [ ] Branch is up to date with main
- [ ] No accidental binary files committed
- [ ] .gitignore rules followed

## Final Verification

```bash
# Run all checks
pylint src/
mypy src/
black --check src/
pytest tests/ -v
```

If all pass ✅ → Ready to commit!
