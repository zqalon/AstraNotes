# AstraNotes Product Requirements Document (PRD)

**Version:** 1.0  
**Last Updated:** April 29, 2026  
**Status:** Draft  
**Project Duration:** 10-week quarter (4 sprints + Sprint Zero)

---

## Requirement ID Cross-Reference for PRD Sections

| PRD Section | Requirement IDs | Source Document(s) |
|-------------|-----------------|-------------------|
| §3.1: Authentication & Authorization | F-001, F-001a-e, SEC-001b | requirements.md, user-stories.md US-1/US-2 |
| §3.2: Core CRUD Operations | F-002, F-002a-e | requirements.md, user-stories.md US-3/US-4/US-5/US-6 |
| §3.3: Note Organization | F-003, F-003a-e | requirements.md, backlog.md EPIC 4 |
| §3.4: Search & Filtering | F-003b, F-003c | requirements.md, user-stories.md US-7, backlog.md EPIC 5 |
| §3.5: CLI | F-004, F-004a-c | requirements.md §4, backlog.md EPIC 6 |
| §3.5: GUI | F-005, F-005a-d | requirements.md §5, backlog.md EPIC 7, user-stories.md US-8 |
| §4: Non-Functional Requirements | NF-001, NF-002 | requirements.md Non-Functional Requirements |
| §5: Security | SEC-001, SEC-002 | requirements.md Security Requirements, backlog.md EPIC 8 |
| §6: Out-of-Scope | F-003d-e, F-006, NF-001c-d | backlog.md EPIC 10 |
| §9: Future Vision | F-006, F-003d-e, F-002e | backlog.md EPIC 10 |

---

## Traceability & Source Documentation

This PRD consolidates content from existing course artifacts. The table below shows which sections are sourced from which documents:

| Section | Source Document(s) | Notes |
|---------|-------------------|-------|
| **Problem Statement** | AI-synthesized | Inferred from requirements.md and backlog.md context |
| **Target Users** | requirements.md (implicit) | User personas expanded and detailed; not explicitly defined in artifacts |
| **Core Features 3.1-3.4** | requirements.md, backlog.md, user-stories.md | Directly traceable: Functional Requirements + Epics 2-5 + User Stories 1-7 |
| **Core Features 3.5 (CLI/GUI)** | requirements.md, backlog.md | Directly traceable: Functional Requirements section 4-5 + Epics 6-7 |
| **Non-Functional Requirements** | requirements.md | Directly traceable: Non-Functional Requirements and Security Requirements sections |
| **Key Risks & Mitigations** | sprint-zero-plan.md | Sourced from section 6 (Risk Assessment & Mitigation); reformatted as table |
| **Out-of-Scope Items** | backlog.md | Directly traceable: EPIC 10 (Future Phases) and section "What Sprint Zero Does NOT Include" |
| **Success Criteria** | backlog.md, sprint-zero-plan.md | Release Plan (backlog) + Sprint Zero Success Criteria (sprint-zero); milestones organized by sprint |
| **Constraints & Assumptions** | sprint-zero-plan.md | Timeline and technical decisions from Sprint Zero section |
| **Glossary** | AI-generated | Reference definitions for domain terms |
| **Future Vision (Phase 2+)** | backlog.md | Sourced from EPIC 10 (Additional Features - Post-MVP) |

**Key Addition:** Problem Statement and user personas were synthesized by AI but align with the functional and non-functional requirements. Recommend validating these with instructor/stakeholders to confirm they match course vision.

---

## Synthesis Notes

### AI-Synthesized Content Requiring Validation
1. **Problem Statement (§1):** Written to contextualize the requirements but not explicitly stated in artifacts. Recommended discussion point with stakeholders.
2. **User Personas (§2):** Job titles and profiles inferred from use cases. Confirm that the three user categories (individual, power user, collaborative team) align with instructor expectations.
3. **Performance Metrics (§4.1):** Target values (< 200ms API response, < 500ms search) are reasonable defaults for an MVP but not specified in artifacts. Recommend confirmation in Sprint Zero.
4. **UI Specifications (GUI mockup details):** Screen layout (left sidebar, center panel, right panel) follows common note-app patterns but not explicitly designed in artifacts.

### Content Directly Traceable to Artifacts (High Confidence)
- All functional requirements sections (3.1-3.4) map 1:1 to requirements.md section 2-3
- All user stories (3.1-3.4) cross-referenced to user-stories.md US-1 through US-8
- Security, maintainability, and UX requirements (§4) directly sourced from requirements.md
- Risk register (§5) consolidated from sprint-zero-plan.md §6 table
- Out-of-scope items (§6) from backlog.md EPIC 10 and explicitly deferred items
- Release timeline and success criteria (§7) aligned with backlog.md Release Plan

### Deferred Decisions (To Be Made in Sprint Zero)
- Backend framework selection (Node.js vs. Python vs. Java)
- Database technology (PostgreSQL vs. SQLite)  
- Authentication approach (JWT vs. session-based)
- GUI framework (Electron vs. PyQt vs. JavaFX)

---

## 1. Problem Statement

### The Challenge
Users struggle to manage personal notes across multiple contexts (work, personal, academic) due to:
- **Fragmentation:** Notes scattered across email, cloud storage, and messaging apps
- **Disorganization:** Difficulty finding notes when needed despite having many notes
- **Security concerns:** Storing sensitive information on commercial platforms with unclear privacy policies
- **Accessibility friction:** Switching between web, mobile, and desktop environments

### The Solution
AstraNotes provides a unified, secure, personal note management system with a single source of truth—accessible via CLI, desktop GUI, and eventually web/mobile interfaces. Emphasis on **user privacy** (zero-knowledge architecture) and **ease of use** (intuitive organization and powerful search).

### Success Metric
Users can create, organize, search, and retrieve notes efficiently across multiple interfaces with confidence in data privacy and security.

---

## 2. Target Users

*Note: User personas are AI-synthesized based on implied requirements. Profiles are inferred; needs are sourced from requirements.md Functional Requirements.*

### Primary User: Individual Note-Taker
- **Profile:** Students, professionals, or knowledge workers who take 10-100+ notes daily *(AI inferred)*
- **Needs:** Fast note creation (US-3), reliable organization (requirements §3), quick retrieval via search (US-7), privacy (non-functional security req)
- **Devices:** Desktop (primary), eventually mobile and web *(source: requirements.md §4-6)*
- **Tech Comfort:** Intermediate to advanced (CLI adoption) *(source: backlog.md EPIC 6)*

### Secondary User: Power Users / Developers
- **Profile:** Technical users who prefer command-line interfaces and automation
- **Needs:** CLI toolkit for note management, scriptable workflows, API access (future)
- **Motivation:** Integration with existing development workflows

### Future User: Collaborative Team
- **Profile:** Small teams or study groups (post-MVP)
- **Needs:** Note sharing, collaborative editing, permissions
- **Timing:** Post-v1.0 release

---

## 3. Core Features (MVP)

### 3.1 Authentication & Session Management
*Source: requirements.md §1 (User Authentication & Authorization) + backlog.md EPIC 2 + user-stories.md US-1/US-2*
- **Registration:** Email-based signup with password validation (minimum 8 characters, complexity rules)
- **Login/Logout:** Secure credentials verification with JWT or session tokens
- **Session Timeout:** Configurable inactivity timeout (default 30 minutes per US-2) with auto-logout
- **Password Reset:** Email-based reset flow with secure token generation
- **Not Included:** OAuth, multi-factor authentication (future)

### 3.2 Core CRUD Operations
*Source: requirements.md §2 (Note CRUD Operations) + backlog.md EPIC 3 + user-stories.md US-3/US-4/US-5/US-6*
- **Create Notes:** Title, content, optional metadata (tags, category, due date per US-3)
- **Read Notes:** 
  - Single note view with full content (US-4)
  - List view with pagination (20 notes per page per requirements)
  - Metadata display (created, modified, tags, category per US-4)
- **Update Notes:** Edit title and content with automatic timestamp updates (US-5)
- **Delete Notes:** 
  - Soft delete (recoverable per US-6)
  - Permanent deletion option (US-6 acceptance criteria)
  - Recovery/restore functionality (US-6)

### 3.3 Note Organization
*Source: requirements.md §3 (Note Organization) + backlog.md EPIC 4*
- **Categories/Folders:** Hierarchical structure (unlimited nesting depth per backlog EPIC 4)
  - Create, rename, delete categories
  - Move notes between categories
  - Default "Inbox" and "Archived" categories
- **Tags:** Flat tagging system per requirements
  - Add/remove multiple tags per note
  - Tag management (view all tags, tag statistics)
- **Relationship:** Notes can have one category and multiple tags

### 3.4 Search & Filtering
*Source: requirements.md §3 (Note Organization - search & filtering) + backlog.md EPIC 5 + user-stories.md US-7*
- **Full-Text Search:** Query across note titles and content (US-7 acceptance criteria)
  - Case-insensitive search
  - Ranked results (title matches weighted higher than content per backlog EPIC 5)
- **Advanced Filters:** Per US-7 and requirements
  - By date range (created, modified)
  - By category
  - By tags (single and multiple per US-7)
  - Combination of filters
- **Sorting:** By date (newest/oldest), alphabetical, relevance per requirements

### 3.5 User Interfaces

#### Command Line Interface (CLI)
*Source: requirements.md §4 (Command Line Interface) + backlog.md EPIC 6*
- Interactive menu system for navigation (requirements §4)
- Command-based operations: `create`, `list`, `search`, `edit`, `delete`, `tag`, `category` (backlog EPIC 6)
- Keyboard shortcuts for power users (requirements §4 + backlog EPIC 6)
- Help documentation accessible via `help` command
- Supports piping and scripting (future enhancement)

#### Desktop GUI (Electron/PyQt/JavaFX)
*Source: requirements.md §5 (Graphical User Interface) + backlog.md EPIC 7 + user-stories.md US-8*
- **Authentication Screen:** Login and registration forms (US-8)
- **Main Window:**
  - Left sidebar: Category/folder tree navigation (requirements §5, US-8)
  - Center panel: Note list with preview (US-8)
  - Right panel: Full note editor (requirements §5)
- **Search Interface:**
  - Search bar at top with filter options (requirements §5)
  - Results displayed in list view
- **Cross-Platform:** Windows, macOS, Linux support (requirements §5, US-8)
- **Keyboard Shortcuts:** Common shortcuts (Ctrl+N for new, Ctrl+S for save) (requirements §4)

---

## 4. Non-Functional Requirements

*Source: requirements.md Non-Functional Requirements & Security Requirements sections*

### 4.1 Performance
- **API Response Time:** < 200ms for CRUD operations on 10,000 notes
- **Search Response Time:** < 500ms for full-text search across 10,000 notes
- **UI Responsiveness:** < 100ms perceived lag for user interactions
- **Startup Time:** Desktop app launches within 3 seconds

### 4.2 Scalability
- **Initial Target:** Single user, ~10,000 notes
- **Database:** Efficient indexing on search fields (title, content, tags)
- **Future:** Multi-user support, cloud sync (not MVP)

### 4.3 Security
- **Data Encryption:**
  - Passwords hashed with bcrypt (cost factor 12) or Argon2
  - Database encryption at rest (if using file-based DB; PostgreSQL encryption for server)
  - HTTPS/TLS for future API communications
- **Input Validation:** Sanitization against SQL injection, XSS attacks, CSRF tokens (if applicable)
- **Access Control:** User isolation (users can only access their own notes)
- **Audit Logging:** Log authentication attempts, note deletions, password resets

### 4.4 Reliability & Availability
- **Data Persistence:** No data loss on application crash or system reboot
- **Graceful Degradation:** CLI continues working if GUI fails
- **Error Handling:** User-friendly error messages, no stack traces exposed

### 4.5 Maintainability
- **Code Quality:** 70%+ code coverage for core features (unit & integration tests)
- **Documentation:** 
  - Setup guide (`SETUP.md`)
  - Architecture overview (`ARCHITECTURE.md`)
  - API documentation (template)
  - Contributing guidelines (`CONTRIBUTING.md`)
- **Code Standards:** Linting (ESLint/Pylint), formatting (Prettier/Black), pre-commit hooks

### 4.6 Usability
- **Accessibility:** Keyboard-navigable interfaces, screen reader support (progressive enhancement)
- **Learning Curve:** Intuitive defaults, in-app help system or tooltips
- **Consistency:** Uniform UI patterns across GUI and CLI

---

## 5. Key Risks & Mitigations

*Source: sprint-zero-plan.md §6 (Risk Assessment & Mitigation) - reformatted from narrative form to risk register table*

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|-----------|
| Unclear authentication architecture requirements | High | Medium | Early discussion with instructor; finalize JWT vs sessions in Sprint Zero |
| Search performance degradation with large note volumes | Medium | Low | Index frequently-searched fields; test scalability with 10K+ notes in Sprint 3-4 |
| Desktop GUI build complexity unfamiliar to developer | High | High | Prioritize CLI for MVP; delay GUI to Sprint 5 if needed; use proven frameworks (Electron) |
| Database schema design changes mid-project | Medium | Medium | Finalize schema in Sprint Zero; use migration tools; plan for schema versioning |
| Quarter timeline constraint vs. feature scope creep | High | High | Strict MVP scope boundary; prioritize P0/P1 items only; defer P2/P3 to future phases |
| Dependency version conflicts or library incompatibility | Medium | Medium | Document minimum versions; use lock files (package-lock.json, requirements.txt); test compatibility early |
| User data privacy concerns with zero-knowledge architecture | High | Low | Implement E2E encryption; document architecture; no server-side data read capability |
| Testing coverage gaps in critical auth/security paths | High | Medium | Priority testing on authentication and data deletion flows; 80%+ coverage for sensitive code |

---

## 6. Out-of-Scope Items (MVP)

*Source: backlog.md EPIC 10 (Additional Features - Future Phases) + sprint-zero-plan.md section "What Sprint Zero Does NOT Include"*

### Features Explicitly Excluded from v1.0
- **Collaboration:** Note sharing, collaborative editing, team workspaces
- **Advanced Interfaces:** Web interface, mobile app, browser plugin
- **Data Sync:** Cloud backup, cross-device sync, offline-first architecture
- **Note Features:** Rich media (images, PDFs), markdown rendering, code highlighting (future)
- **Advanced Organization:** Note templates, recurring notes, calendar integration
- **Security Add-ons:** Multi-factor authentication (MFA), OAuth, LDAP integration, SSO
- **Analytics:** Usage statistics, note activity tracking, trends
- **Integrations:** Third-party API integrations, zapier/IFTTT automation, Slack bot
- **Localization:** Multi-language support, regional date/number formats
- **Offline Mode:** Local-first sync, conflict resolution for offline edits

### Deferred by Design
- **Mobile App** → Post-MVP (evaluate during v1.0 stabilization)
- **Note Versioning** → P2 feature (future sprint)
- **Favorites/Bookmarking** → P2 feature (future sprint)
- **Bulk Operations** → P2 feature (future sprint)
- **REST API** → Post-MVP (once backend stability proven)

---

## 7. Success Criteria

*Source: backlog.md Release Plan + sprint-zero-plan.md Sprint Zero Success Criteria - consolidated and expanded*

### End of Sprint Zero (Week 1)
- ✅ Development environment fully configured and documented
- ✅ Technical stack finalized and justified (backend, database, frontend)
- ✅ Project structure scaffolded with working build
- ✅ Testing framework initialized with example tests
- ✅ Architecture and database schema documented

### End of Sprint 2 (Alpha Release)
- ✅ User registration and login fully functional
- ✅ Basic CRUD operations working (create, read, update, delete notes)
- ✅ Session management implemented
- ✅ Core security measures in place (password hashing, input validation)
- ✅ CLI interface operational
- ✅ 70%+ code coverage for authentication and CRUD
- ✅ Ready for internal testing and instructor review

### End of Sprint 4 (Beta Release)
- ✅ Note organization (categories and tags) complete
- ✅ Search and filtering fully functional
- ✅ Desktop GUI application running on multiple platforms (Windows, macOS, Linux)
- ✅ 70%+ code coverage across all features
- ✅ Documentation complete and accurate
- ✅ Ready for class review and feedback

### End of Sprint 5+ (v1.0 Production Release)
- ✅ All P0 and P1 items completed
- ✅ Comprehensive testing suite (unit, integration, e2e)
- ✅ Performance benchmarks met (response times, search speed)
- ✅ Security audit completed with zero critical vulnerabilities
- ✅ User documentation and onboarding guide available
- ✅ Production-ready deployment checklist signed off

---

## 8. Constraints & Assumptions

*Source: sprint-zero-plan.md§2 (Technical Stack & Architecture Decisions) + backlog.md Release Plan*

### Project Constraints
- **Timeline:** 10-week quarter divided into 4 implementation sprints + Sprint Zero (source: sprint-zero-plan)
- **Resources:** Solo student developer
- **Platforms:** Initially desktop-focused (CLI + GUI); web/mobile deferred (source: sprint-zero-plan §2.3)
- **Budget:** None (open-source, no paid services required initally)

### Technical Assumptions
- Backend framework chosen from: Node.js/Express, Python/FastAPI, or Java/Spring Boot (source: sprint-zero-plan §2.1)
- Database: PostgreSQL (relational) or SQLite (file-based) for MVP simplicity (source: sprint-zero-plan §2.2)
- GUI framework: Electron, PyQt, or JavaFX (source: sprint-zero-plan §2.3)
- Authentication: JWT tokens or session-based (source: sprint-zero-plan §2.4)

### User Assumptions
- Users are comfortable with CLI for power features
- Initial user base: Solo developer (future: multi-user support deferred to Cloud phase)
- Users have basic computer literacy; not a barrier to entry

---

## 9. Glossary

| Term | Definition |
|------|-----------|
| **E2E Encryption** | End-to-end encryption; data encrypted on client, server cannot decrypt |
| **Zero-Knowledge Architecture** | Server stores data but has no cryptographic keys to decrypt user content |
| **MVP** | Minimum Viable Product; core features to ship and gather feedback |
| **CRUD** | Create, Read, Update, Delete; standard data operations |
| **JWT** | JSON Web Token; stateless authentication token |
| **Soft Delete** | Logical delete; data marked as deleted but retained for recovery |
| **Full-Text Search** | Search algorithm that indexes and queries across all word content |
| **Taxonomy** | System of classification; in this case, categories and tags |

---

## 10. Appendix: Future Vision (Post-MVP)

*Source: backlog.md EPIC 10 (Additional Features - Future Phases) + requirements.md §6 (Web Interface - Future)*

### Phase 2: Collaboration & Cloud (Sprints 6-8)
- Multi-user architecture with collaborative editing (future extensibility per backlog)
- Cloud storage backend with automatic sync (backlog EPIC 10)
- Note sharing with granular permissions (backlog EPIC 10)
- Real-time collaboration indicators

### Phase 3: Advanced Features (Sprints 9-12)
- Rich media support (images, files, code snippets) (backlog EPIC 10)
- Note templates and batch operations (backlog EPIC 10: bulk operations, note versioning)
- Mobile app (iOS/Android) (backlog EPIC 10)
- Web interface with responsive design (requirements.md §6 + backlog EPIC 10)
- REST API for third-party integrations (backlog EPIC 10)

### Phase 4: Enterprise & AI (Future)
- Multi-factor authentication (MFA) (future security enhancement)
- Team management and audit logging (future)
- AI-powered note summarization and tagging (future)
- Advanced search with natural language processing (future)
- Integration marketplaces (future)

---

**Document Owner:** Product Team  
**Last Review Date:** April 29, 2026  
**Next Review:** After Sprint Zero completion
