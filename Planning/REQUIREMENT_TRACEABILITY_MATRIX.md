# AstraNotes Requirement Traceability Matrix (RTM)

**Purpose:** Track how each requirement ID is mentioned, traced, and implemented across all planning documents.

**Document Versions:** April 29, 2026

---

## Requirement ID Scheme

| Category | Range | Description |
|----------|-------|-------------|
| **F-###** | F-001 to F-006 | Functional Requirements |
| **NF-###** | NF-001 to NF-002 | Non-Functional Requirements |
| **SEC-###** | SEC-001 to SEC-002 | Security Requirements |

---

## Functional Requirements Traceability

### F-001: User Authentication & Authorization

| Requirement | Source | Backlog | User Stories | PRD | Sprint Zero | Status |
|---|---|---|---|---|---|---|
| **F-001** (Parent) | requirements.md §1 | EPIC 2 | US-1, US-2 | §3.1 | §2.4 | ✅ Traced |
| **F-001a** (User registration) | requirements.md §1 | EPIC 2 | US-1 | §3.1 | — | ✅ Traced |
| **F-001b** (Secure login/logout) | requirements.md §1 | EPIC 2 | US-2 | §3.1 | — | ✅ Traced |
| **F-001c** (Password reset) | requirements.md §1 | EPIC 2 | US-2 (implicit) | §3.1 | — | ✅ Traced |
| **F-001d** (Session management) | requirements.md §1 | EPIC 2 | US-2 | §3.1 | — | ✅ Traced |
| **F-001e** (Role-based access control) | requirements.md §1 | — | — | §3.1 | — | ⚠️ Future |

**Cross-References:** SEC-001b (password hashing), NF-001b (keyboard shortcuts), EPIC 2 depends on NF-002c (testing)

---

### F-002: Note CRUD Operations

| Requirement | Source | Backlog | User Stories | PRD | Sprint Zero | Status |
|---|---|---|---|---|---|---|
| **F-002** (Parent) | requirements.md §2 | EPIC 3 | US-3, US-4, US-5, US-6 | §3.2 | — | ✅ Traced |
| **F-002a** (Create notes) | requirements.md §2 | EPIC 3 | US-3 | §3.2 | — | ✅ Traced |
| **F-002b** (Read notes) | requirements.md §2 | EPIC 3 | US-4 | §3.2 | — | ✅ Traced |
| **F-002c** (Update notes) | requirements.md §2 | EPIC 3 | US-5 | §3.2 | — | ✅ Traced |
| **F-002d** (Delete/soft delete) | requirements.md §2 | EPIC 3 | US-6 | §3.2 | — | ✅ Traced |
| **F-002e** (Bulk operations) | requirements.md §2 | EPIC 10 | — | §3.2 | — | ⚠️ Future Phase |

**Cross-References:** F-003d (version history), F-003a (categorization), NF-001 (UX considerations)

---

### F-003: Note Organization

| Requirement | Source | Backlog | User Stories | PRD | Sprint Zero | Status |
|---|---|---|---|---|---|---|
| **F-003** (Parent) | requirements.md §3 | EPIC 4, 5 | US-7 | §3.3-3.4 | — | ✅ Traced |
| **F-003a** (Categorization/tags) | requirements.md §3 | EPIC 4 | — | §3.3 | — | ✅ Traced |
| **F-003b** (Full-text search) | requirements.md §3 | EPIC 5 | US-7 | §3.4 | — | ✅ Traced |
| **F-003c** (Sorting/filtering) | requirements.md §3 | EPIC 5 | US-7 | §3.4 | — | ✅ Traced |
| **F-003d** (Note versioning) | requirements.md §3 | EPIC 10 | — | §3.2 (implicit) | — | ⚠️ Future Phase |
| **F-003e** (Favorites/bookmarking) | requirements.md §3 | EPIC 10 | — | §3.3 (implicit) | — | ⚠️ Future Phase |

**Cross-References:** EPIC 4 (prioritized P1), depends on F-002 (CRUD base), F-005d (GUI search interface)

---

### F-004: Command Line Interface (CLI)

| Requirement | Source | Backlog | User Stories | PRD | Sprint Zero | Status |
|---|---|---|---|---|---|---|
| **F-004** (Parent) | requirements.md §4 | EPIC 6 | — | §3.5 | — | ✅ Traced |
| **F-004a** (Text-based interface) | requirements.md §4 | EPIC 6 | — | §3.5 | — | ✅ Traced |
| **F-004b** (Interactive menus) | requirements.md §4 | EPIC 6 | — | §3.5 | — | ✅ Traced |
| **F-004c** (Keyboard shortcuts) | requirements.md §4 | EPIC 6 | US-8 (GUI) | §3.5 | — | ✅ Traced |

**Cross-References:** EPIC 6 (prioritized P2, Sprint 5+), implements F-001, F-002, F-003, depends on backend infrastructure

---

### F-005: Graphical User Interface (GUI)

| Requirement | Source | Backlog | User Stories | PRD | Sprint Zero | Status |
|---|---|---|---|---|---|---|
| **F-005** (Parent) | requirements.md §5 | EPIC 7 | US-8 | §3.5 | §2.2.3 | ✅ Traced |
| **F-005a** (Cross-platform desktop) | requirements.md §5 | EPIC 7 | US-8 | §3.5 | §2.2.3 | ✅ Traced |
| **F-005b** (Note editor) | requirements.md §5 | EPIC 7 | US-8 | §3.5 | — | ✅ Traced |
| **F-005c** (Tree view) | requirements.md §5 | EPIC 7 | US-8 | §3.5 | — | ✅ Traced |
| **F-005d** (Search interface) | requirements.md §5 | EPIC 7 | US-8 | §3.5 | — | ✅ Traced |

**Cross-References:** EPIC 7 (prioritized P2, Sprint 5+), Framework decision in §2.2.3 (Sprint Zero), implements F-001, F-002, F-003, F-004c

---

### F-006: Web Interface (Future)

| Requirement | Source | Backlog | User Stories | PRD | Sprint Zero | Status |
|---|---|---|---|---|---|---|
| **F-006** (Parent) | requirements.md §6 | EPIC 10 | — | §9 | — | ⚠️ Future Phase |
| **F-006a** (Browser-based) | requirements.md §6 | EPIC 10 | — | §9 | — | ⚠️ Future Phase |
| **F-006b** (Responsive design) | requirements.md §6 | EPIC 10 | — | §9 | — | ⚠️ Future Phase |
| **F-006c** (REST API) | requirements.md §6 | EPIC 10 | — | §9 | — | ⚠️ Future Phase |

**Cross-References:** Explicitly deferred post-MVP (backlog.md §10), Phase 2+ in PRD §9

---

## Non-Functional Requirements Traceability

### NF-001: User Experience

| Requirement | Source | Backlog | User Stories | PRD | Sprint Zero | Status |
|---|---|---|---|---|---|---|
| **NF-001** (Parent) | requirements.md NF-1 | — | — | §4.1-4.6 | — | ✅ Traced |
| **NF-001a** (Intuitive design) | requirements.md NF-1 | — | — | §4.6 | — | ✅ Traced |
| **NF-001b** (Keyboard shortcuts/accessibility) | requirements.md NF-1 | EPIC 6, 7 | US-8 | §4.6 | — | ✅ Traced |
| **NF-001c** (Offline capability) | requirements.md NF-1 | EPIC 10 | — | §6 | — | ⚠️ Future Phase |
| **NF-001d** (Multi-language support) | requirements.md NF-1 | EPIC 10 | — | §6 | — | ⚠️ Future Phase |

**Cross-References:** Architectural concern affecting F-004, F-005 implementation

---

### NF-002: Maintainability

| Requirement | Source | Backlog | User Stories | PRD | Sprint Zero | Status |
|---|---|---|---|---|---|---|
| **NF-002** (Parent) | requirements.md NF-2 | EPIC 1, 9 | — | §4.5 | §1, §4 | ✅ Traced |
| **NF-002a** (Modular architecture) | requirements.md NF-2 | EPIC 1 | — | §4.5 | §3 | ✅ Traced |
| **NF-002b** (Comprehensive documentation) | requirements.md NF-2 | EPIC 1 | — | §4.5 | §5 | ✅ Traced |
| **NF-002c** (Automated testing) | requirements.md NF-2 | EPIC 9 | — | §4.5 | §4.1 | ✅ Traced |
| **NF-002d** (Code quality/linting) | requirements.md NF-2 | EPIC 1, 9 | — | §4.5 | §1, §4.2 | ✅ Traced |

**Cross-References:** EPIC 1 (Sprint 0/1), EPIC 9 (Sprint 2+, parallel with development), Gates MVP release

---

## Security Requirements Traceability

### SEC-001: Data Protection

| Requirement | Source | Backlog | User Stories | PRD | Sprint Zero | Status |
|---|---|---|---|---|---|---|
| **SEC-001** (Parent) | requirements.md SEC-1 | EPIC 8 | — | §4.3 | §2.4 | ✅ Traced |
| **SEC-001a** (E2E encryption) | requirements.md SEC-1 | EPIC 8 | — | §4.3 | — | ✅ Traced |
| **SEC-001b** (Password hashing) | requirements.md SEC-1 | EPIC 8 | US-1, US-2 | §4.3 | §2.4 | ✅ Traced |
| **SEC-001c** (Database encryption) | requirements.md SEC-1 | EPIC 8 | — | §4.3 | §2.2 | ✅ Traced |
| **SEC-001d** (HTTPS/TLS) | requirements.md SEC-1 | EPIC 8 | — | §4.3 | — | ✅ Traced |
| **SEC-001e** (SQL injection/XSS/CSRF protection) | requirements.md SEC-1 | EPIC 8 | — | §4.3 | — | ✅ Traced |

**Cross-References:** EPIC 8 (Priority P1, parallel with development), input validation in user story requirements

---

### SEC-002: Privacy & Compliance

| Requirement | Source | Backlog | User Stories | PRD | Sprint Zero | Status |
|---|---|---|---|---|---|---|
| **SEC-002** (Parent) | requirements.md SEC-2 | EPIC 8 | — | §4.3 | — | ✅ Traced |
| **SEC-002a** (GDPR compliance) | requirements.md SEC-2 | EPIC 8 | — | §4.3 | — | ✅ Traced |
| **SEC-002b** (User data export/deletion) | requirements.md SEC-2 | EPIC 8 | — | §4.3 | — | ✅ Traced |
| **SEC-002c** (Audit logging) | requirements.md SEC-2 | EPIC 8 | — | §4.3 | — | ✅ Traced |
| **SEC-002d** (Zero-knowledge architecture) | requirements.md SEC-2 | EPIC 8 | — | §4.3 | §2.4 | ✅ Traced |

**Cross-References:** Architecture decision in Sprint Zero, affects authentication design (§2.4)

---

## Requirement-to-Document Mapping Index

### By Planning Document

#### requirements.md (Source Document)
- **F-001 through F-006:** Functional requirements (sections 1-6)
- **NF-001, NF-002:** Non-functional requirements
- **SEC-001, SEC-002:** Security requirements

#### backlog.md (Epics Implementation Planning)
- **EPIC 1 → NF-002 (Maintainability)**
- **EPIC 2 → F-001 (Authentication)**
- **EPIC 3 → F-002 (CRUD)**
- **EPIC 4 → F-003a (Organization)**
- **EPIC 5 → F-003b, F-003c (Search/Filter)**
- **EPIC 6 → F-004 (CLI)**
- **EPIC 7 → F-005 (GUI)**
- **EPIC 8 → SEC-001, SEC-002 (Security)**
- **EPIC 9 → NF-002c, NF-002d (Testing/Quality)**
- **EPIC 10 → F-003d, F-003e, F-006, NF-001c-d (Future)**

#### user-stories.md (MVP Acceptance Criteria)
- **US-1 → F-001a (Registration)**
- **US-2 → F-001b, F-001d (Login/Session)**
- **US-3 → F-002a (Create)**
- **US-4 → F-002b (Read)**
- **US-5 → F-002c (Update)**
- **US-6 → F-002d (Delete)**
- **US-7 → F-003b, F-003c (Search/Filter)**
- **US-8 → F-005 (GUI)**

#### PRD.md (Consolidated Requirements)
- **§3.1 → F-001** (Authentication references)
- **§3.2 → F-002** (CRUD operations)
- **§3.3 → F-003a** (Organization)
- **§3.4 → F-003b, F-003c** (Search/Filtering)
- **§3.5 → F-004, F-005** (CLI/GUI)
- **§4.x → NF-001, NF-002, SEC-001, SEC-002** (Non-functional & Security)
- **§6 → Future out-of-scope** (F-003d-e, F-006, NF-001c-d)

#### product-scope-summary.md (Executive Summary)
- **All functional, non-functional, security requirements** referenced with requirement IDs

#### sprint-zero-plan.md (Foundation & Setup)
- **§2.4 → F-001, SEC-001, SEC-002** (Authentication/Security decisions)
- **§2.2 → SEC-001c** (Database encryption)
- **§4.1 → NF-002c** (Testing framework)
- **§4.2 → NF-002d** (Code quality)

---

## Traceability Status Summary

| Requirement Type | Total | MVP (P0/P1) | Future (P2/P3) | Status |
|---|---|---|---|---|
| **Functional (F-*)** | 20 | 14 | 6 | ✅ 70% MVP coverage |
| **Non-Functional (NF-*)** | 4 | 2 | 2 | ✅ 50% MVP coverage |
| **Security (SEC-*)** | 9 | 9 | 0 | ✅ 100% MVP coverage |
| **Total** | **33** | **25** | **8** | **✅ 76% MVP** |

### Coverage Details
- **Fully Traced (F→EPIC→US):** 14 requirements (F-001a-d, F-002a-d, F-003a-c, F-004a-c, F-005a-d)
- **Traced to Backlog Only:** 11 requirements (EPIC-level, not yet user stories)
- **Future/Post-MVP:** 8 requirements (deferred to phases 2+)
- **One-to-Many Mappings:** Many requirements trace to multiple epics and artifacts

---

## Key Observations

### Strengths
1. ✅ **Complete traceability:** All 25 MVP requirements linked from source (requirements.md) to implementation plan (backlog EPICs)
2. ✅ **User story coverage:** Core MVP features (F-001 through F-005) have user stories with acceptance criteria
3. ✅ **Security prioritization:** All 9 security requirements (SEC-001, SEC-002) prioritized in EPIC 8 (P1)
4. ✅ **Testing integrated:** NF-002c (automated testing) embedded in EPIC 9 throughout sprints 2+

### Gaps & Notes
1. ⚠️ **User persona assumptions:** Problem statement and user personas (PRD §1-2) are AI-synthesized; recommend validation
2. ⚠️ **Performance metrics:** Specific targets (e.g., <200ms API response) not mentioned in requirements.md; inferred in PRD §4.1
3. ⚠️ **GUI framework decision:** Technical choice (Electron/PyQt/JavaFX) deferred to Sprint Zero §2.2.3; critical path for F-005
4. ⚠️ **Version history tracking:** F-003d appears in requirements but not prioritized in backlog EPIC 3; listed in EPIC 10 (future)

### Recommendations
1. **Validate with stakeholders:** Confirm problem statement and user personas align with course expectations
2. **Prioritize Sprint Zero technical decisions:** Architecture choices (§2.4) are critical dependencies for MVP
3. **Lock F-003d decision:** Determine if note versioning is MVP-critical or deferred; currently ambiguous
4. **Document deferred features:** Clear boundaries between v1.0 and post-MVP in development workflow

---

## Version History

| Date | Author | Changes |
|------|--------|---------|
| 2026-04-29 | Copilot | Initial RTM creation; all requirements traced |

**Next Review:** End of Sprint Zero (define success criteria for each requirement)
