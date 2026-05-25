# AstraNotes Testing Strategy

**Version:** 1.0  
**Date Created:** May 18, 2026  
**Status:** Active  
**Focus:** MVP Phase (Sprint 1-4)

---

## Executive Summary

The AstraNotes testing strategy balances comprehensive coverage of security-critical features (authentication, data protection) with pragmatic testing of core functionality (CRUD operations, search). The strategy prioritizes:

1. **Authentication & Authorization (F-001)** — Highest priority for security
2. **Core Note CRUD (F-002)** — Foundation for all user workflows
3. **Search & Organization (F-003)** — High-value user features
4. **Security (SEC-001, SEC-002)** — Data protection and privacy requirements

Testing is organized in three layers: **unit tests** for business logic, **integration tests** for API contracts, and **feature tests** for end-to-end user workflows. Testing begins immediately in Sprint 1 alongside feature development, with test-driven development (TDD) practices for high-risk features.

---

## Testing Strategy Overview

### Testing Pyramid

```
          ╔════════════════════╗
          ║   Feature Tests    ║  5-10% (E2E workflows, UI interactions)
          ║   (Slow/Expensive) ║
          ╠════════════════════╣
          ║  Integration Tests ║  30-40% (API contracts, database)
          ║  (Medium Speed)    ║
          ╠════════════════════╣
          ║    Unit Tests      ║  50-60% (Business logic, utilities)
          ║   (Fast/Cheap)     ║
          ╚════════════════════╝
```

### Testing Scope by Phase

| Phase | Focus | Key Requirements |
|-------|-------|------------------|
| **Sprint 0-1** | Infrastructure, Authentication, Health Checks | F-001, NF-002c (automated testing) |
| **Sprint 2-3** | Core CRUD, Basic Organization | F-002, F-003a |
| **Sprint 4** | Search, Advanced Features, Security | F-003b, SEC-001, SEC-002 |
| **Sprint 5+** | Polish, Performance, GUI/CLI | F-004, F-005, NF-001, NF-002 |

### Test Automation Tooling

- **Framework:** pytest (Python-based, aligns with FastAPI backend)
- **Coverage Target:** 70% minimum for Sprint 1-3, 80%+ for MVP
- **CI/CD Integration:** Tests run on every commit and PR
- **Fixtures:** Reusable database fixtures, user factories, test data

---

## First Test Set: Create Notes Feature (US-3, F-002a)

**Requirement ID:** F-002a (Create new notes with title, content, and optional metadata)  
**User Story:** US-3 (Create New Notes)  
**Priority:** P0 (Highest)

### Context & Rationale

The "Create Notes" feature is the first core CRUD operation and is critical to the MVP. It serves as a foundation for downstream features (edit, delete, search, organization). Testing this feature early ensures:
- API contract stability for frontend development
- Data validation and error handling
- Database persistence and schema correctness
- Security compliance (input sanitization, access control)

### Test Outline: Unit & Integration Tests

#### Unit Tests (Business Logic Layer)

**Test File:** `tests/test_notes_service.py`

**UT-001: Create Note with Valid Input**
```
GIVEN: A valid note creation request with title, content, and optional metadata
WHEN: The note service processes the creation request
THEN: A note object is created with correct attributes
AND: Timestamps (created_at, updated_at) are automatically set
AND: The note is associated with the authenticated user
```
- **Inputs:** `{"title": "Meeting Notes", "content": "...", "tags": ["work"], "category": "Professional"}`
- **Expected Output:** Note object with all fields populated, valid UUIDs
- **Test Type:** Unit
- **Run Time:** ~10ms

**UT-002: Create Note with Minimal Input (Title Only)**
```
GIVEN: A note creation request with only a title
WHEN: The note service processes the request
THEN: A note is created with the title
AND: Content defaults to empty string
AND: Metadata fields (tags, category) are initialized as empty collections
```
- **Inputs:** `{"title": "Quick Note"}`
- **Expected Output:** Note with populated title, empty content and metadata
- **Test Type:** Unit
- **Run Time:** ~10ms

**UT-003: Reject Note Creation with Missing Title**
```
GIVEN: A note creation request without a title
WHEN: The note service validates the input
THEN: A validation error is raised
AND: No note is persisted to the database
```
- **Inputs:** `{"content": "..."}`
- **Expected Exception:** `ValidationError` with message "Title is required"
- **Test Type:** Unit
- **Run Time:** ~5ms

**UT-004: Reject Note with Title Exceeding Length Limit**
```
GIVEN: A note creation request with a title > 500 characters
WHEN: The note service validates the input
THEN: A validation error is raised
AND: Error message indicates title length constraint
```
- **Inputs:** `{"title": "x" * 501}`
- **Expected Exception:** `ValidationError` with message "Title must not exceed 500 characters"
- **Test Type:** Unit
- **Run Time:** ~5ms

**UT-005: Generate Proper Timestamps on Creation**
```
GIVEN: A note is created at a specific time
WHEN: The note is persisted
THEN: created_at and updated_at are set to the same timestamp (ISO 8601 format)
AND: Timestamps are UTC timezone-aware
```
- **Validation:** `note.created_at == note.updated_at` and both are timezone-aware datetime objects
- **Test Type:** Unit
- **Run Time:** ~10ms

**UT-006: Handle Metadata Associations (Tags & Category)**
```
GIVEN: A note creation request with tags and category
WHEN: The note is created
THEN: Tags are associated as a flat list
AND: Category is associated with hierarchical awareness (e.g., "Work/Projects")
AND: Both associations are properly normalized (lowercase, no duplicates)
```
- **Inputs:** `{"title": "Note", "tags": ["WORK", "work", "Project"], "category": "Work/Projects"}`
- **Expected Output:** Tags normalized to `["work", "project"]`, category stored as "Work/Projects"
- **Test Type:** Unit
- **Run Time:** ~15ms

---

#### Integration Tests (API Contract & Database Layer)

**Test File:** `tests/test_notes_api.py`

**IT-001: POST /notes Creates Note and Returns 201**
```
GIVEN: An authenticated user makes a POST request to /notes
WITH: Valid JSON body containing title and content
WHEN: The API processes the request
THEN: HTTP status 201 (Created) is returned
AND: Response includes the created note object with all fields
AND: Location header contains the URL of the newly created note (/notes/{id})
```
- **Request:** `POST /notes` with `{"title": "Test", "content": "Content"}`
- **Expected Response:** 
  ```json
  {
    "id": "uuid-string",
    "title": "Test",
    "content": "Content",
    "created_at": "2026-05-18T12:00:00Z",
    "updated_at": "2026-05-18T12:00:00Z",
    "tags": [],
    "category": null
  }
  ```
- **Test Type:** Integration
- **Run Time:** ~50ms
- **Dependencies:** Database, authentication middleware

**IT-002: Reject Unauthenticated Note Creation with 401**
```
GIVEN: An unauthenticated user (no session/token)
WHEN: They attempt POST to /notes
THEN: HTTP status 401 (Unauthorized) is returned
AND: Response body contains error message "Authentication required"
AND: No note is created in the database
```
- **Request:** `POST /notes` without auth header/session
- **Expected Response:** 401 with error message
- **Test Type:** Integration
- **Run Time:** ~20ms

**IT-003: Note Persists to Database**
```
GIVEN: A note is successfully created via POST /notes
WHEN: The response is returned
THEN: The note is persisted in the database
AND: Retrieving /notes/{id} returns the same note
AND: The note is associated with the authenticated user in the database
```
- **Validation:** Query database, verify record exists with correct user_id foreign key
- **Test Type:** Integration
- **Run Time:** ~60ms

**IT-004: Metadata Relationships Persist Correctly**
```
GIVEN: A note is created with tags and category
WHEN: The note is persisted to the database
THEN: Tag associations are stored in the tags table
AND: Category association is stored correctly
AND: Retrieving the note via GET /notes/{id} includes all associations
```
- **Validation:** Query tag and category junction tables, verify relationships
- **Test Type:** Integration
- **Run Time:** ~80ms

**IT-005: Concurrent Note Creation (Race Condition Test)**
```
GIVEN: Two users simultaneously create notes
WHEN: Both POST requests are processed concurrently
THEN: Both notes are created successfully
AND: Both notes have unique IDs
AND: Each note is associated with the correct user
AND: No data corruption or conflicts occur
```
- **Test Type:** Integration (with concurrency simulation)
- **Run Time:** ~100ms
- **Concurrency Model:** Use threading or async to simulate simultaneous requests

**IT-006: API Returns Validation Errors with 422**
```
GIVEN: An API request with invalid input (e.g., missing title, oversized content)
WHEN: The API validates the request
THEN: HTTP status 422 (Unprocessable Entity) is returned
AND: Response body includes detailed error messages
AND: Error format is consistent with FastAPI validation error schema
```
- **Request:** `POST /notes` with missing title
- **Expected Response:** 422 with validation error details
- **Test Type:** Integration
- **Run Time:** ~30ms

---

### Requirements & User Stories Alignment

| Test ID | Test Name | Requirement(s) | User Story | Acceptance Criteria Covered |
|---------|-----------|----------------|------------|---------------------------|
| UT-001 | Valid Note Creation | F-002a, SEC-001e | US-3 | ✓ User can enter title/content ✓ Note saved to system |
| UT-002 | Minimal Input | F-002a | US-3 | ✓ Optional metadata support |
| UT-003 | Reject Missing Title | F-002a | US-3 | ✓ Validation of required fields |
| UT-004 | Reject Oversized Title | F-002a, SEC-001e | US-3 | ✓ Input sanitization/security |
| UT-005 | Proper Timestamps | F-002a, NF-002c | US-3 | ✓ Note saved with metadata |
| UT-006 | Metadata Associations | F-002a, F-003a | US-3 | ✓ Optional metadata fields |
| IT-001 | POST /notes Returns 201 | F-002a, NF-001a | US-3 | ✓ Confirmation message (via 201 + response) |
| IT-002 | Reject Unauthenticated | F-001a, F-002a | US-3 | ✓ Secure account required |
| IT-003 | Persists to Database | F-002a, NF-002c | US-3 | ✓ Note saved to system |
| IT-004 | Metadata Relationships | F-002a, F-003a | US-3 | ✓ Metadata persisted correctly |
| IT-005 | Concurrent Creation | F-002a, NF-002a | US-3 | ✓ Data integrity under load |
| IT-006 | Validation Errors | F-002a, SEC-001e | US-3 | ✓ Error handling |

**Coverage Summary:**
- ✓ **F-002a:** All acceptance criteria covered by tests (input, storage, metadata, errors)
- ✓ **F-001a:** Authentication requirement validated (IT-002)
- ✓ **F-003a:** Optional metadata handling covered (UT-006, IT-004)
- ✓ **SEC-001e:** XSS/injection protection via input validation tested (UT-004, IT-006)
- ✓ **NF-002c:** Automated testing requirement demonstrated

---

## Test Type Classification

### Unit Tests (50-60% of test suite)
- **Scope:** Business logic, validation rules, data transformations
- **Example:** `test_note_validation()`, `test_timestamp_generation()`
- **Tools:** pytest, mock/patch for dependencies
- **Speed:** < 50ms per test
- **Isolation:** No database or network calls (fully mocked)
- **Count (Create Notes):** 6 tests (UT-001 through UT-006)

### Integration Tests (30-40% of test suite)
- **Scope:** API contracts, database persistence, external service interactions
- **Example:** `test_post_notes_returns_201()`, `test_note_persists_to_db()`
- **Tools:** pytest + TestClient (FastAPI), real database or in-memory SQLite
- **Speed:** 50-500ms per test
- **Setup:** Requires test database, fixtures, user authentication
- **Count (Create Notes):** 6 tests (IT-001 through IT-006)

### Feature/E2E Tests (5-10% of test suite)
- **Scope:** End-to-end user workflows across multiple features
- **Example:** `test_complete_note_lifecycle()` (create → edit → search → delete)
- **Tools:** Selenium/Playwright (GUI), TestClient + business workflow simulation
- **Speed:** 500ms-5s per test
- **Coverage:** Post-MVP, after GUI/CLI implementations
- **Count (Create Notes Phase):** 0 (planned for Sprint 4+)

---

## Test Execution Timeline During Development

### Sprint 1-2: Authentication & Foundation (Weeks 1-3)
- **When:** Tests written alongside code (TDD approach)
- **Frequency:** Continuous integration on every commit
- **Trigger:** Pre-commit hook (unit tests), PR check (integration tests)
- **Reporting:** Coverage metrics in CI dashboard, failures block merge

### Sprint 2: Core CRUD (Weeks 4-6)
- **When:** Create Notes tests finalized by end of Week 4
- **Regression:** All authentication tests re-run with each update
- **New Tests:** Added incrementally as features complete
- **Checkpoint:** Code review includes test validation

### Sprint 3-4: Organization & Search (Weeks 7-10)
- **When:** Feature tests added for multi-feature workflows
- **Examples:** Create → Search, Create → Categorize → Filter
- **Performance Tests:** Added for search queries on 10k+ notes

### Continuous Integration Setup
```
Commit → Pre-commit Checks
  ├─ Unit tests (must pass, ~2min)
  └─ Linting/formatting (pre-merge)
       ↓
Pull Request → PR Checks
  ├─ All unit + integration tests (must pass, ~5min)
  ├─ Coverage report (must be > 70%)
  └─ Security scan (dependency check)
       ↓
Merge → Post-Merge
  └─ Full test suite + E2E tests (optional, ~15min)
```

---

## AI Assistance in Testing Strategy Development

### How AI Was Used

1. **Test Case Generation**
   - AI drafted comprehensive test cases for edge cases (oversized input, concurrent requests)
   - Suggested boundary conditions (e.g., empty strings, max-length titles)
   - Generated realistic test data scenarios

2. **Coverage Analysis**
   - AI identified gaps in requirement coverage (authentication check, race conditions)
   - Suggested tests for implicit requirements (e.g., SEC-001e input sanitization from F-002a)
   - Mapped tests to acceptance criteria

3. **Best Practice Integration**
   - AI suggested pytest conventions and fixtures
   - Recommended test naming patterns (descriptive Given-When-Then)
   - Proposed testing pyramid ratios (unit/integration/E2E split)

4. **Traceability Documentation**
   - AI created cross-reference matrix (test ID ↔ requirement ↔ user story)
   - Generated test execution timeline aligned with sprint schedule
   - Documented CI/CD pipeline triggers

### AI-Generated Sections
- Test outline structure (UT-001 through IT-006)
- Acceptance criteria mapping table
- Testing pyramid diagram
- CI/CD pipeline pseudocode

---

## What Was Kept, Changed, or Rejected

### ✓ Kept (From AI Generation)

| Item | Rationale |
|------|-----------|
| **Test Naming Convention** (UT-001, IT-001, etc.) | Clear, sortable IDs simplify test selection and CI logs |
| **Given-When-Then Format** | Aligns with user story acceptance criteria, improves readability |
| **Unit/Integration/E2E Split** | Follows industry best practice (testing pyramid); matches team's likely experience |
| **Concurrent Request Test (IT-005)** | Catches race conditions early; important for data integrity (NF-002a) |
| **Metadata Association Test (UT-006, IT-004)** | Validates complex relationships before full CRUD implementation |
| **Coverage Mapping Table** | Provides traceability; useful for compliance documentation |
| **Sprint Timeline Alignment** | Ensures testing doesn't lag behind development |
| **Mock/Fixture Approach** | Enables fast unit tests; critical for developer productivity |

### 🔄 Changed (Modified from AI Suggestions)

| Item | Original AI Suggestion | Change Made | Reason |
|------|------------------------|-------------|--------|
| **Total Test Count** | AI suggested 15 tests | Reduced to 12 for Phase 1 | Focus on MVP; feature/E2E tests deferred to Sprint 4+ |
| **Coverage Target** | AI recommended 85% | Changed to 70% for Sprints 1-3, 80%+ post-MVP | Pragmatic balance; allows iterative development without over-engineering |
| **CI/CD Frequency** | AI suggested test on every file save | Changed to commit/PR triggers only | Avoid notification fatigue; aligns with team workflow |
| **Database Selection** | AI suggested PostgreSQL initially | Use in-memory SQLite for unit/integration tests | Faster local development; production uses PostgreSQL |
| **E2E Testing Tool** | AI suggested Playwright | Deferred E2E tests to post-GUI implementation | Playwright requires deployed GUI; premature for current phase |

### ✗ Rejected (Not Included)

| Item | AI Suggestion | Reason for Rejection |
|------|----------------|-------|
| **Property-Based Testing (Hypothesis)** | Generate random test inputs to find edge cases | Overkill for MVP; useful post-launch for stability testing |
| **Load Testing (Locust)** | Simulate 1000+ concurrent users | Performance requirements not yet defined; deferred to Scale phase |
| **Mutation Testing** | Verify test effectiveness by mutating code | Too advanced for team stage; revisit in Sprint 5+ |
| **API Contract Testing (Pact)** | Ensure API contracts between frontend/backend | Single-team development; premature for sprint 1-2 |
| **Compliance Testing (GDPR/SEC-002)** | Automated tests for data deletion/export | Legal/privacy review required first; add in Sprint 4+ |
| **Screenshot Comparison Tests** | Visual regression testing for GUI | GUI not yet implemented; defer to post-MVP |

---

## Success Metrics & Checkpoints

### Sprint 1 Checkpoint (Week 2)
- [ ] Unit tests for note validation logic written and passing
- [ ] Integration tests for POST /notes endpoint written and passing
- [ ] Test coverage for authentication (F-001) > 80%
- [ ] CI/CD pipeline configured; tests run on every commit

### Sprint 2 Checkpoint (Week 4)
- [ ] Create Notes tests finalized (12 tests, 100% passing)
- [ ] Coverage for F-002a (Create operation) > 85%
- [ ] Read Notes tests outline started (IT-010 through IT-013 drafted)
- [ ] Zero test flakiness; all tests deterministic

### Sprint 3-4 Checkpoint (Week 8)
- [ ] Feature tests for Create → Search → Filter workflow passing
- [ ] Overall test suite coverage > 75%
- [ ] All core CRUD operations (US-3 through US-6) tested

### MVP Release Criterion
- [ ] All unit & integration tests passing
- [ ] Coverage > 70% across codebase
- [ ] Zero known security vulnerabilities in test infrastructure
- [ ] Test execution time < 10 minutes (full suite)

---

## Test Maintenance & Evolution

### Monthly Review
- Analyze flaky tests; fix or remove
- Review coverage reports; identify gaps
- Update test data and fixtures for new features

### Post-MVP
- Implement feature-level tests for GUI/CLI (F-004, F-005)
- Add compliance/security tests (SEC-001, SEC-002)
- Introduce performance benchmarks for search (F-003b)
- Evaluate advanced tools (mutation testing, load testing)

---

## Appendix: Sample Test Code (Pseudocode)

### Unit Test Example: `test_note_validation.py`

```python
import pytest
from astranotes.services.note_service import NoteService, ValidationError

def test_create_note_with_valid_input():
    """UT-001: Create note with valid input"""
    service = NoteService()
    note = service.create_note(
        title="Meeting Notes",
        content="Discussed Q2 roadmap",
        user_id="user-123",
        tags=["work"],
        category="Professional"
    )
    
    assert note.title == "Meeting Notes"
    assert note.content == "Discussed Q2 roadmap"
    assert note.user_id == "user-123"
    assert note.tags == ["work"]
    assert note.category == "Professional"
    assert note.created_at is not None
    assert note.updated_at == note.created_at

def test_reject_missing_title():
    """UT-003: Reject note creation with missing title"""
    service = NoteService()
    
    with pytest.raises(ValidationError) as exc_info:
        service.create_note(title="", content="Content", user_id="user-123")
    
    assert "Title is required" in str(exc_info.value)
```

### Integration Test Example: `test_notes_api.py`

```python
from fastapi.testclient import TestClient
from astranotes.main import app

def test_post_notes_returns_201(client: TestClient, authenticated_user):
    """IT-001: POST /notes creates note and returns 201"""
    response = client.post(
        "/notes",
        json={"title": "Test Note", "content": "Content"},
        headers={"Authorization": f"Bearer {authenticated_user.token}"}
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Note"
    assert "id" in data
    assert response.headers.get("Location") == f"/notes/{data['id']}"

def test_reject_unauthenticated(client: TestClient):
    """IT-002: Reject unauthenticated note creation with 401"""
    response = client.post(
        "/notes",
        json={"title": "Test Note", "content": "Content"}
    )
    
    assert response.status_code == 401
    assert "Authentication required" in response.json()["detail"]
```

---

## Related Documents

- [requirements.md](requirements.md) — Functional and security requirements
- [user-stories.md](user-stories.md) — User story acceptance criteria
- [backlog.md](backlog.md) — EPIC 9 (Automated Testing)
- [REQUIREMENT_TRACEABILITY_MATRIX.md](REQUIREMENT_TRACEABILITY_MATRIX.md) — Full requirement mapping

---

**Document Status:** ✓ Ready for Sprint 1  
**Next Review:** End of Sprint 2 (Week 5)  
**Owner:** QA & Development Team  
**Approval:** Pending
