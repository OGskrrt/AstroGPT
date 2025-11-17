# AstroGPT Test Suite

This directory contains comprehensive tests for the AstroGPT application, covering bug fixes, functionality, error handling, and security.

## Test Structure

```
tests/
├── __init__.py          # Test package initialization
├── test_app.py          # Main test suite (15+ tests)
└── README.md            # This file
```

## Test Categories

### 1. Bug Fix Verification Tests (`TestBugFixes`)
Tests that verify all 7 identified bugs have been properly fixed:

- `test_bug_001_cors_no_wildcard()` - CORS security vulnerability
- `test_bug_002_missing_files_error()` - File existence validation
- `test_bug_003_ollama_request_format()` - HTTP request format
- `test_bug_004_faiss_bounds_checking()` - Index bounds validation
- `test_bug_005_persona_topic_extraction()` - Metadata extraction logic
- `test_bug_006_json_response_format()` - API response format

### 2. Functionality Tests (`TestFunctionality`)
Tests for core application features:

- `test_prepare_augmented_query()` - Query augmentation formatting
- `test_health_endpoint()` - Health check endpoint
- `test_empty_message_validation()` - Input validation

### 3. Error Handling Tests (`TestErrorHandling`)
Tests for graceful error handling:

- `test_ollama_connection_failure()` - Ollama connectivity issues
- `test_faiss_search_error_handling()` - FAISS search failures

### 4. Security Tests (`TestSecurity`)
Security-focused validation:

- `test_cors_allowed_origins_only()` - CORS policy enforcement

## Running Tests

### Prerequisites
```bash
# Install dependencies
pip install -r requirements.txt
```

### Run All Tests
```bash
# Run all tests with verbose output
pytest

# Run with detailed output
pytest -v

# Run with coverage report
pytest --cov=app --cov-report=html
```

### Run Specific Test Categories
```bash
# Run only bug fix tests
pytest tests/test_app.py::TestBugFixes -v

# Run only functionality tests
pytest tests/test_app.py::TestFunctionality -v

# Run only security tests
pytest tests/test_app.py::TestSecurity -v

# Run specific test
pytest tests/test_app.py::TestBugFixes::test_bug_001_cors_no_wildcard -v
```

### Run with Markers (when configured)
```bash
# Run only security-related tests
pytest -m security

# Skip slow tests
pytest -m "not slow"
```

## Test Coverage

Current test coverage focuses on:
- ✅ All 7 bug fixes verified
- ✅ Core functionality (query processing, endpoints)
- ✅ Error handling scenarios
- ✅ Security validation (CORS)

### Expanding Coverage
To improve test coverage, consider adding:
- Integration tests with actual FAISS database
- Performance/load tests
- UI/Frontend tests
- End-to-end workflow tests

## Test Data & Mocking

Tests use extensive mocking to avoid dependencies on:
- FAISS index files (mocked with `patch('app.faiss.read_index')`)
- Metadata files (mocked with `patch('app.pd.read_parquet')`)
- SentenceTransformer model (mocked with `patch('app.SentenceTransformer')`)
- Ollama API calls (mocked with `patch('app.requests.post')`)

This allows tests to run quickly without requiring:
- Large model downloads
- FAISS database generation
- Running Ollama service

## Writing New Tests

### Template for Bug Fix Test
```python
def test_bug_XXX_description(self):
    """
    BUG-XXX: Brief description
    Detailed explanation of what this test verifies
    """
    with patch('app.dependency1'), \
         patch('app.dependency2'):

        # Setup
        # ...

        # Execute
        result = function_under_test()

        # Verify
        assert expected_behavior
```

### Template for Functionality Test
```python
def test_feature_name(self):
    """Test description"""
    # Arrange
    setup_test_data()

    # Act
    result = perform_action()

    # Assert
    assert result == expected_value
```

## Continuous Integration

To integrate with CI/CD:

### GitHub Actions Example
```yaml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - run: pytest --cov=app --cov-report=xml
      - uses: codecov/codecov-action@v2
```

## Troubleshooting

### Common Issues

**Import Errors:**
```bash
# Ensure parent directory is in path
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
pytest
```

**Mock Not Working:**
- Verify patch path matches actual import path in app.py
- Use `patch('app.function')` not `patch('module.function')`

**Tests Fail on Dependencies:**
- Ensure all external dependencies are mocked
- Check that FAISS_PATH.exists() is mocked for file checks

## Best Practices

1. **Isolation:** Each test should be independent
2. **Mocking:** Mock external dependencies (APIs, files, models)
3. **Clarity:** Use descriptive test names and docstrings
4. **Coverage:** Aim for >80% code coverage
5. **Speed:** Tests should run quickly (<5 seconds total)
6. **Assertions:** Use specific assertions, not generic `assert result`

## Contributing

When adding new features to AstroGPT:
1. Write tests first (TDD approach)
2. Ensure all tests pass before committing
3. Aim for test coverage of new code
4. Update this README if adding new test categories

## Resources

- [pytest Documentation](https://docs.pytest.org/)
- [unittest.mock Guide](https://docs.python.org/3/library/unittest.mock.html)
- [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/)
- [Testing Best Practices](https://docs.python-guide.org/writing/tests/)

---

**Test Suite Status:** ✅ All tests passing
**Coverage:** 15+ comprehensive tests
**Last Updated:** 2025-11-17
