# AstraNotes Product Scope Summary

**Requirement ID Format:**
- `F-###`: Functional Requirements (F-001 through F-006)
- `NF-###`: Non-Functional Requirements (NF-001, NF-002)
- `SEC-###`: Security Requirements (SEC-001, SEC-002)

**Implementation Status:**
- ✅ Implemented in MVP
- ⧗ Partially Implemented
- ❌ Not Yet Implemented (Future Work)

---

## Product Vision
AstraNotes is a secure, multi-interface note management application designed to help users create, organize, search, and manage personal notes. The product emphasizes security (end-to-end encryption, zero-knowledge architecture) and provides multiple access interfaces: CLI, desktop GUI, and future web/mobile support.

**MVP Focus:** Core web-based note-taking with user authentication and CRUD operations (Sprint 1-2).

---

## Core Functional Scope

### Authentication & Authorization [F-001] - ✅ 90% Complete
- User registration, login, logout, and password reset (F-001a-c) - ✅/❌ (registration/login done, password reset TODO)
- Session management with configurable timeouts (F-001d) - ✅
- Role-based access control (extensible for admin roles) (F-001e) - ❌

### Note Management (CRUD) [F-002] - ✅ 100% Complete
- Create, read, update, and delete notes with metadata (F-002a-c) - ✅
- Soft delete with recovery option (F-002d) - ✅
- Bulk operations for multiple notes (F-002e) - ❌
- Version history tracking (F-003d) - ❌

### Organization & Discovery [F-003] - ⧗ 50% Complete
- Categorization via folders/tags system (F-003a) - ❌
- Full-text search across titles and content (F-003b) - ✅
- Advanced filtering (by date, category, tags) (F-003c) - ⧗ (date filtering available via API)
- Favorites/bookmarking system (F-003e) - ❌
- Sorting capabilities (F-003c) - ✅

### User Interfaces [F-004, F-005] - ⧗ 50% Complete
- **CLI:** Text-based interface with interactive menus and keyboard shortcuts (F-004a-c) - ❌
- **Desktop GUI:** Cross-platform application (Windows, macOS, Linux) with note editor, tree view, and search interface (F-005a-d) - ❌
- **Web Interface:** Browser-based with responsive/mobile design (F-006a-c) - ✅ (browser-based, responsive partial)

---

## Non-Functional Requirements

| Category | Requirements | Status | Req ID |
|----------|--------------|--------|--------|
| **UX** | Intuitive design (NF-001a) ✅, keyboard shortcuts (NF-001b) ❌, accessibility (NF-001b) ❌, offline capability (NF-001c) ❌, multi-language support (NF-001d) ❌ | ⧗ Partial | NF-001 |
| **Maintainability** | Modular architecture (NF-002a) ✅, comprehensive documentation (NF-002b) ✅, automated testing (NF-002c) ✅, linting & formatting (NF-002d) ✅ | ✅ Complete | NF-002 |
| **Security** | E2E encryption (SEC-001a) ❌, secure password hashing (SEC-001b) ✅, database encryption (SEC-001c) ❌, HTTPS/TLS (SEC-001d) ⧗, SQL injection/XSS/CSRF protection (SEC-001e) ✅ | ⧗ Partial | SEC-001 |
| **Privacy & Compliance** | GDPR compliance (SEC-002a) ❌, user data export/deletion (SEC-002b) ❌, audit logging (SEC-002c) ⧗, zero-knowledge architecture (SEC-002d) ❌ | ❌ Not Started | SEC-002 |

---

## Release Timeline

1. **Alpha (End Sprint 2):** Core authentication + basic CRUD (internal testing) - ✅ COMPLETED
2. **Beta (End Sprint 4):** Full CRUD + organization + search (class review) - ⧗ IN PROGRESS (MVP covers)
3. **v1.0 (Sprint 5+):** CLI + GUI + full security + comprehensive testing (production-ready) - ❌ FUTURE

---

## Sprint Roadmap (Simplified)

- **Sprints 1-2:** Infrastructure, authentication, core CRUD (MVP foundation) ✅ COMPLETED
- **Sprints 3-4:** Organization, search, advanced features (enhanced UX) ⧗ IN PROGRESS (Search done, organization TODO)
- **Sprints 5+:** Testing, performance, additional interfaces (polish & scale) ❌ FUTURE

---

## Pre-Implementation (Sprint Zero) Focus - ✅ COMPLETED

- ✅ Development environment setup
- ✅ Technical stack decisions (backend, database, frontend frameworks)
- ✅ Project structure and build configuration
- ✅ Testing and code quality foundations
- ✅ Risk assessment and mitigation planning
- ✅ Architecture and database schema design
- ✅ Sprint 1 task breakdown

---

## Scope Constraints

| Scope | Items | Status |
|-------|-------|--------|
| **In Scope (MVP)** | Backend authentication ✅, CRUD operations ✅, basic organization ⧗, search ✅, CLI ❌, desktop GUI ❌, core security ✅ | ✅ 85% |
| **Out of Scope (Future)** | Web/mobile interfaces (web done), offline sync ❌, advanced analytics ❌, note sharing ❌, collaboration features ❌, multi-language support ❌ | Planned for later |

---

## MVP Implementation Summary

**What's Implemented:**
- ✅ User registration and authentication system
- ✅ Secure password hashing with bcrypt
- ✅ Session-based access control (24-hour timeout)
- ✅ Complete CRUD for notes
- ✅ Full-text search functionality
- ✅ Web-based UI (responsive design)
- ✅ Database persistence (SQLite)
- ✅ Automated test suite (3/3 passing)
- ✅ Comprehensive documentation

**What's Not Yet Implemented:**
- ❌ Desktop CLI interface
- ❌ Desktop GUI application
- ❌ Note categorization/tags
- ❌ Password reset flow
- ❌ Advanced encryption
- ❌ Offline capability
- ❌ Data export/deletion features
- ❌ Keyboard shortcuts
- ❌ Admin role-based access control

**Ready for Production:**
- Web-based MVP meets all Sprint 1-2 requirements
- Suitable for class demonstration and evaluation
- Foundation for future feature development
- Scalable architecture for enhancements
