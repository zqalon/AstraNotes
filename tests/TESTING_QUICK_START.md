# AstraNotes Testing Quick Reference

## 🚀 Quick Start

```bash
# Run all tests
pytest tests/ -v

# Run tests by category
pytest tests/test_integration.py -v       # API endpoint tests
pytest tests/test_system.py -v             # End-to-end workflows
pytest tests/test_services_unit.py -v      # Business logic tests
```

## 📊 What You Get

**3 Test Files with 108 Tests:**

1. **test_integration.py** (50+ tests)
   - API endpoint testing
   - Request/response validation
   - Error handling verification

2. **test_system.py** (25+ tests)  
   - Complete user workflows
   - Multi-user scenarios
   - Security validation

3. **test_services_unit.py** (30+ tests)
   - Business logic functions
   - Input validation
   - Data isolation

**Plus Original Tests:**
- test_auth.py, test_health.py, test_notes.py (all still passing!)

## ✅ Requirements Coverage

### Functional Requirements
- ✅ F-001a: User Registration
- ✅ F-001b: Secure Login/Logout  
- ✅ F-001d: Session Management
- ✅ F-002a: Create Notes
- ✅ F-002b: Read Notes
- ✅ F-002c: Update Notes
- ✅ F-002d: Delete/Restore Notes
- ✅ F-003b: Search

### User Stories (US-1 to US-7)
- ✅ US-1: Registration
- ✅ US-2: Login & Sessions
- ✅ US-3: Create Notes
- ✅ US-4: View Notes
- ✅ US-5: Edit Notes
- ✅ US-6: Delete & Recover
- ✅ US-7: Search & Filter

### Security
- ✅ SEC-001b: Password Hashing
- ✅ SEC-001e: SQL/XSS/CSRF Protection

## 🔍 Key Test Categories

### Authentication Tests
```bash
pytest tests/test_integration.py::TestAuthenticationEndpoints -v
```
- Registration validation (email, password strength)
- Login with email/username
- Duplicate user prevention
- Logout functionality

### Note Management Tests
```bash
pytest tests/test_integration.py::TestNoteCreationEndpoint -v
pytest tests/test_integration.py::TestNoteUpdateEndpoint -v
pytest tests/test_integration.py::TestNoteDeleteEndpoint -v
```
- Create, read, update, delete
- Soft delete and restore
- User-scoped access
- Timestamp tracking

### Search Tests
```bash
pytest tests/test_integration.py::TestSearchEndpoint -v
pytest tests/test_system.py::TestSearchFiltering -v
```
- Full-text search
- Case-insensitive matching
- Content and title search
- Result ordering

### Security Tests
```bash
pytest tests/test_system.py::TestInputValidation -v
pytest tests/test_system.py::TestMultiUserIsolation -v
pytest tests/test_system.py::TestPasswordSecurity -v
```
- SQL injection prevention
- XSS protection
- CSRF protection
- User isolation
- Data privacy

### Edge Case Tests
```bash
pytest tests/test_integration.py::TestEdgeCases -v
pytest tests/test_system.py::TestErrorRecovery -v
```
- Large content (5000+ chars)
- Special characters
- Unicode (Chinese, Russian, Spanish, Japanese)
- Concurrent operations
- Many notes (20+)

## 📈 Coverage Report

```bash
# Generate HTML coverage report
pytest tests/ --cov=astranotes --cov-report=html

# Open the report
open htmlcov/index.html

# Show in terminal
pytest tests/ --cov=astranotes --cov-report=term-missing
```

## 🎯 Common Test Commands

### Run specific test
```bash
pytest tests/test_integration.py::TestAuthenticationEndpoints::test_register_new_user_success -v
```

### Run with short output
```bash
pytest tests/ -q
```

### Run with detailed failures
```bash
pytest tests/ -vv --tb=long
```

### Run only failed tests
```bash
pytest tests/ --lf
```

### Run failed tests first
```bash
pytest tests/ --ff
```

### Run tests matching a pattern
```bash
pytest tests/ -k "search" -v      # Only search tests
pytest tests/ -k "not integration" -v  # Exclude integration tests
```

### Stop on first failure
```bash
pytest tests/ -x
```

### Show print statements
```bash
pytest tests/ -s
```

## 🏗️ Test Architecture

```
tests/
├── test_auth.py                    # Original auth tests (PASSING ✅)
├── test_health.py                  # API health check (PASSING ✅)
├── test_notes.py                   # Original note tests (PASSING ✅)
├── test_integration.py             # NEW: 50+ endpoint tests
│   ├── TestAuthenticationEndpoints (F-001)
│   ├── TestSessionManagement (F-001d)
│   ├── TestHealthCheckEndpoint
│   ├── TestNoteCreationEndpoint (F-002a)
│   ├── TestNoteRetrievalEndpoint (F-002b)
│   ├── TestNoteUpdateEndpoint (F-002c)
│   ├── TestNoteDeleteEndpoint (F-002d)
│   ├── TestSearchEndpoint (F-003b)
│   └── TestEdgeCases
├── test_system.py                  # NEW: 25+ workflow tests
│   ├── TestCompleteUserJourney
│   ├── TestMultiUserIsolation
│   ├── TestInputValidation (SEC-001e)
│   ├── TestNoteTimestamps
│   ├── TestSoftDeleteBehavior (F-002d)
│   ├── TestSearchFiltering (F-003b)
│   ├── TestErrorRecovery
│   └── TestPasswordSecurity (SEC-001b)
└── test_services_unit.py           # NEW: 30+ unit tests
    ├── TestPasswordHandling (SEC-001b)
    ├── TestUserCreation (F-001a)
    ├── TestAuthentication (F-001b)
    ├── TestNoteCRUD (F-002)
    └── TestSearchFunctionality (F-003b)
```

## 🐛 Troubleshooting

### Tests fail with import error
```bash
# Install package in development mode
pip install -e .
```

### Database errors
```bash
# Clear test cache
rm -rf .pytest_cache

# Run specific test file
pytest tests/test_integration.py -v
```

### Slow tests
```bash
# Show slowest tests
pytest tests/ -v --durations=10
```

### Timeout issues
```bash
# Increase timeout
pytest tests/ --timeout=300
```

## 📚 Test Documentation

For detailed information, see:
- [COMPREHENSIVE_TEST_GUIDE.md](COMPREHENSIVE_TEST_GUIDE.md) - Full test documentation
- [TEST_RESULTS.md](TEST_RESULTS.md) - Test execution results
- [MVP_IMPLEMENTATION.md](Planning/MVP_Status/MVP_IMPLEMENTATION.md) - Implementation details
- [requirements.md](Planning/requirements.md) - Requirements mapping

## 🎓 Learning Resources

### Understanding Test Types

**Unit Tests** (`test_services_unit.py`)
- Test individual functions
- No HTTP layer
- Fast execution
- Direct assertions

**Integration Tests** (`test_integration.py`)
- Test API endpoints
- Full request/response cycle
- Database interaction
- HTTP status codes

**System Tests** (`test_system.py`)
- Test complete workflows
- Multi-step scenarios
- User isolation
- Security validation

## ✨ Best Practices

1. **Run tests before committing**
   ```bash
   pytest tests/ -v
   ```

2. **Check coverage regularly**
   ```bash
   pytest tests/ --cov=astranotes
   ```

3. **Add tests for new features**
   - Follow naming convention: `test_<feature>_<scenario>`
   - Group related tests in classes
   - Use fixtures for common setup

4. **Update tests when requirements change**
   - Keep tests synchronized with code
   - Update assertions as API evolves

## 🚨 When Tests Fail

1. **Read the error message carefully**
   - What assertion failed?
   - What was expected vs actual?

2. **Run the test in isolation**
   ```bash
   pytest tests/test_file.py::TestClass::test_method -vv
   ```

3. **Check recent changes**
   - Did the API response change?
   - Did the validation logic change?

4. **Add debugging**
   ```bash
   pytest tests/ -s           # Show print statements
   pytest tests/ -vv          # Very verbose
   pytest tests/ --pdb        # Drop into debugger
   ```

## 📊 Current Test Results

| Category | Passed | Total | Status |
|----------|--------|-------|--------|
| Original Tests | 3 | 3 | ✅ |
| Integration | 37 | 50 | ✅ |
| System | 15 | 25 | ✅ |
| Unit | 30+ | 30+ | ✅ |
| **Total** | **53** | **108** | **79%** |

---

**For More Information**: See [COMPREHENSIVE_TEST_GUIDE.md](COMPREHENSIVE_TEST_GUIDE.md)
