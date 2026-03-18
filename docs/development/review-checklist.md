# Code Review Checklist

Use this before submitting a pull request.

## Code Quality

- [ ] Code follows PEP 8 style guide
- [ ] No trailing whitespace
- [ ] Lines ≤ 100 characters
- [ ] Uses 4-space indentation
- [ ] Consistent naming conventions

## Testing

- [ ] All tests pass: `pytest tests/ -v`
- [ ] New code has unit tests
- [ ] Edge cases tested
- [ ] Error paths tested
- [ ] Test coverage maintained or improved

## Type Safety

- [ ] Type hints on all functions
- [ ] Complex types documented
- [ ] No bare `Any` types
- [ ] Mypy passes: `mypy src/`

## Documentation

- [ ] Module/class docstrings added
- [ ] Method docstrings added
- [ ] Docstrings in Google style
- [ ] Examples in docstrings
- [ ] README updated if appropriate
- [ ] Comments for complex logic

## Error Handling

- [ ] Uses custom exceptions
- [ ] Exceptions have error codes
- [ ] Error messages are clear
- [ ] No bare `except:` clauses
- [ ] Handles all foreseeable errors

## Performance

- [ ] No N+1 queries
- [ ] Async used appropriately
- [ ] Caching applied properly
- [ ] Resource limits enforced
- [ ] No memory leaks

## Security

- [ ] No hardcoded credentials
- [ ] No SQL injection vulnerabilities
- [ ] Input validated
- [ ] Secrets not in logs
- [ ] HTTPS used for external calls

## Git

- [ ] Feature branch created
- [ ] Commits describe changes
- [ ] No merge commits
- [ ] Branch up to date with main
- [ ] No unintended files added

## Code Organization

- [ ] Files in correct directories
- [ ] No circular imports
- [ ] Imports organized (stdlib, 3rd-party, local)
- [ ] No unused imports
- [ ] Constants in appropriate locations

## Documentation Files

- [ ] Markdown is well-formatted
- [ ] Links work correctly
- [ ] Code examples are correct
- [ ] Tone is consistent
- [ ] No broken references

---

## Reviewer Checklist

- [ ] Understand the purpose
- [ ] Code implements requirements
- [ ] Solution is elegant
- [ ] No unnecessary complexity
- [ ] Follows project standards
- [ ] Tests are adequate
- [ ] Documentation is clear

---

Before marking as "ready for review":

```bash
# Run full suite
pytest tests/ -v
black --check src/
mypy src/ --config-file=mypy.ini
pylint src/ --disable=all --enable=E

# Fix any issues
black src/
pytest tests/ -vv

# Final check
echo "Ready!" ✓
```

---

See: [contributing.md](contributing.md), [code-quality.md](code-quality.md)
