# AstraNotes Requirements Specification

**Requirement ID Format:**
- `F-###`: Functional Requirements
- `NF-###`: Non-Functional Requirements
- `SEC-###`: Security Requirements

**Implementation Status Legend:**
- ✅ Implemented in MVP
- ⧗ Partially Implemented
- ❌ Not Yet Implemented (Future Work)

---

## Functional Requirements

**F-001: User Authentication & Authorization**
   - F-001a: User registration with email/username and password ✅
   - F-001b: Secure login/logout functionality ✅
   - F-001c: Password reset capability ❌
   - F-001d: Session management with configurable timeouts ✅

**F-002: Note CRUD Operations**
   - F-002a: Create new notes with title, content, and optional metadata ✅
   - F-002b: Read/view notes (individual and list views) ✅
   - F-002c: Update/edit existing notes ✅
   - F-002d: Delete notes (soft delete with recovery option) ✅
   - F-002e: Bulk operations for multiple notes ❌

**F-003: Note Organization**
   - F-003a: Categorization system (folders/tags) ✅
   - F-003b: Search functionality (full-text search across titles and content) ✅
   - F-003c: Sorting and filtering options (by date, category, title) ✅
   - F-003d: Note versioning (keep history of changes) ❌
   - F-003e: Favorites/bookmarking system ❌

**F-004: Command Line Interface (CLI)**
   - F-004a: Text-based interface for basic operations ❌
   - F-004b: Interactive menus and prompts ❌
   - F-004c: Keyboard shortcuts for power users ❌

**F-006: Web Interface (Future)**
   - F-006a: Browser-based access ✅
   - F-006b: Responsive design for mobile devices ⧗
   - F-006c: RESTful API for third-party integrations ✅


## Non-Functional Requirements

**NF-001: User Experience**
   - NF-001a: Intuitive interface design ✅
   - NF-001d: Multi-language support (future) ❌

**NF-002: Maintainability**
   - NF-002a: Modular architecture for easy feature addition ✅
   - NF-002b: Comprehensive documentation ✅
   - NF-002c: Automated testing (unit, integration, e2e) ✅
   - NF-002d: Code quality standards (linting, formatting) ✅

---

## Security Requirements

**SEC-001: Data Protection**
   - SEC-001a: End-to-end encryption for note content ❌
   - SEC-001b: Secure password hashing (bcrypt/Argon2) ✅
   - SEC-001c: Database encryption at rest ❌
   - SEC-001d: Secure communication protocols (HTTPS/TLS) ⧗
   - SEC-001e: Protection against common attacks (SQL injection, XSS, CSRF) ✅

**SEC-002: Privacy & Compliance**
   - SEC-002a: GDPR compliance for data handling ❌
   - SEC-002b: User data export/deletion capabilities ❌
   - SEC-002c: Audit logging for sensitive operations ⧗
   - SEC-002d: Zero-knowledge architecture (server cannot read user data) ❌
