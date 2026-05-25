# AstraNotes Sprint Zero Plan

## Requirement ID Cross-Reference for Sprint Zero

Sprint Zero is foundational work that enables implementation of requirements in later sprints. Key requirement areas:
- **NF-002b, NF-002c, NF-002d:** Testing framework (§4), code quality setup (§4)
- **SEC-001, SEC-002:** Security architecture decisions (§2.4), discussed in Risk Assessment (§6)
- **F-001 through F-006:** Technical stack decisions (§2) determine technology choices for implementing these requirements

---

## Overview
Sprint Zero is a **planning and setup sprint** focused on establishing development infrastructure, technical decisions, and project readiness. This sprint does NOT include feature implementation—only foundational work.

**Duration:** 1 week (Week 1 of quarter)  
**Goal:** Achieve readiness to begin Sprint 1 with minimal blockers  
**Team:** Solo student developer  
**Scope:** Infrastructure, decisions, documentation, and risk mitigation only

---

## Sprint Zero Objectives

| Objective | Success Criteria |
|-----------|-----------------|
| **Development Environment** | All tools installed, repo configured, dependencies documented |
| **Technical Stack Decision** | Backend, database, and frontend frameworks selected and justified |
| **Project Structure** | Repo organized with proper folder hierarchy and build configuration |
| **Documentation** | Setup guide, architecture decisions, and contribution guidelines complete |
| **Risk Assessment** | High-risk items identified with mitigation strategies |
| **Team Workflow** | Development workflow documented, testing strategy outlined |

---

## Task Breakdown

### 1. Development Environment Setup (Day 1-2) [2 days]

#### 1.1 Version Control Configuration
- [ ] Initialize Git repository (or fork if using template)
- [ ] Set up `.gitignore` for project type
- [ ] Create branch naming conventions document
- [ ] Set up GitHub (or chosen platform) with:
  - [ ] Issue templates for bugs/features
  - [ ] Pull request template
  - [ ] README with project overview

#### 1.2 Local Development Setup
- [ ] Verify OS-specific tooling (macOS: Xcode Command Line Tools)
- [ ] Install required runtime (Node.js/Python/Java version)
- [ ] Set up IDE/editor with extensions/plugins
- [ ] Create `.env.example` for configuration
- [ ] Document environment setup in `SETUP.md`

#### 1.3 Database Setup
- [ ] Choose and install database (PostgreSQL/MongoDB/SQLite)
- [ ] Create local development database
- [ ] Document connection string format
- [ ] Set up database migration tool framework

**Deliverable:** `docs/SETUP.md` with step-by-step instructions
**Supports Requirements:** All data-related requirements (F-002, F-003, SEC-001c)

---

### 2. Technical Stack & Architecture Decisions (Day 2-3) [2 days]

#### 2.1 Backend Framework Selection
**Decision to make:**
- [ ] Node.js (Express/Fastify) vs Python (FastAPI/Django) vs Java (Spring Boot)
  
**Evaluation criteria:**
- Learning curve and familiarity
- Class requirements or recommendations
- Ecosystem maturity and available libraries
- Documentation quality

**Deliverable:** `docs/TECH_DECISIONS.md` with reasoning

#### 2.2 Database Technology
**Decision to make:**
- [ ] Relational (PostgreSQL) vs Document (MongoDB) vs Lightweight (SQLite)
  
**Considerations:**
- Schema structure (notes, users, categories)
- Query complexity (search requirements)
- Scalability needs vs simplicity

**Deliverable:** Updated `TECH_DECISIONS.md`

#### 2.3 Frontend/UI Technology
**Decision to make:**
- [ ] CLI only vs Desktop (Electron/PyQt/JavaFX) vs Full stack (add web later)
  
**Rationale:** Scope for quarter-long project

#### 2.4 Authentication Strategy
**Decision to make:**
- [ ] JWT tokens vs Session-based vs OAuth (future)
- [ ] Password hashing algorithm (bcrypt vs Argon2) (SEC-001b)

**Deliverable:** Architecture diagram in `docs/ARCHITECTURE.md`
**Supports Requirements:** F-001 (Authentication), SEC-001, SEC-002 (Security)

---

### 3. Project Structure & Initialization (Day 2-3) [2 days]

#### 3.1 Repository Organization
- [ ] Create folder structure:
  ```
  AstraNotes/
  ├── backend/
  │   ├── src/
  │   ├── tests/
  │   ├── package.json (or requirements.txt)
  │   └── .env.example
  ├── frontend/ (if applicable)
  ├── docs/
  │   ├── SETUP.md
  │   ├── ARCHITECTURE.md
  │   ├── TECH_DECISIONS.md
  │   └── API.md (template)
  ├── planning/
  │   ├── User_Stories.md
  │   ├── Product_Backlog.md
  │   └── Sprint_Zero_Plan.md
  ├── .gitignore
  └── README.md
  ```

#### 3.2 Initialize Backend Project
- [ ] Create initial project scaffolding
- [ ] Set up package manager (npm/pip)
- [ ] Install core dependencies (framework, database driver)
- [ ] Create `.gitignore` for dependencies

#### 3.3 Configure Build & Run Scripts
- [ ] Add `start` and `dev` scripts to package.json/Makefile
- [ ] Set up database initialization script
- [ ] Document commands in project README

**Deliverable:** Functional, runnable project scaffold

---

### 4. Testing & Code Quality Foundations (Day 3) [1 day]

#### 4.1 Testing Framework Setup [NF-002c]
- [ ] Install testing library (Jest/Pytest/JUnit)
- [ ] Create test directory structure
- [ ] Write 1-2 example unit tests (no real features yet)
- [ ] Configure test runner and coverage tools

#### 4.2 Code Linting & Formatting [NF-002d]
- [ ] Install linter (ESLint/Pylint)
- [ ] Set up code formatter (Prettier/Black)
- [ ] Configure pre-commit hooks (if applicable)
- [ ] Document code style in `CONTRIBUTING.md`

**Deliverable:** `package.json` with test scripts and verified test execution
**Supports Requirements:** NF-002c (Automated testing), NF-002d (Code quality)

---

### 5. Planning Artifacts & Documentation (Day 4) [1 day]

#### 5.1 API Design (Draft)
- [ ] Outline core API endpoints (using existing Product_Backlog.md)
- [ ] Create simple API documentation template
- [ ] Note any deferred design decisions

#### 5.2 Database Schema (Draft)
- [ ] Create initial ER diagram or schema diagram
- [ ] Define core tables: users, notes, categories, tags
- [ ] Document schema in `docs/SCHEMA.md`
- [ ] Note relationships and indexes needed

#### 5.3 Architecture Decision Log
- [ ] Document Sprint Zero decisions
- [ ] Note assumptions made
- [ ] Record deferred decisions for Sprint 1

**Deliverable:** `docs/ARCHITECTURE.md`, `docs/SCHEMA.md` (draft)

---

### 6. Risk Assessment & Mitigation (Day 4-5) [1 day]

#### 6.1 Identify High-Risk Items
Document in `docs/RISK_REGISTER.md`:

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|-----------|
| Unclear authentication requirements | High | Medium | Discuss with instructor in Sprint 1 planning |
| Database performance with search | Medium | Low | Use indexed queries, test with sample data |
| Cross-platform desktop build complexity | High | High | Start CLI-only if Electron unfamiliar |
| Time management for quarterly project | High | Medium | Strict Sprint 2 scope cap at Product Backlog P1 |
| Dependency version conflicts | Medium | Medium | Document required versions, use lock files |

#### 6.2 Mitigation Strategies
- [ ] Prioritize scope: Core CRUD > Organization > GUI
- [ ] Plan weekly check-ins for progress tracking
- [ ] Identify external dependencies (frameworks, APIs)
- [ ] Create fallback plans for "nice-to-have" features

**Deliverable:** `docs/RISK_REGISTER.md`

---

### 7. Team Workflow & Process (Day 5) [1 day]

#### 7.1 Development Workflow
- [ ] Document Git branching strategy (feature branches, PR requirements)
- [ ] Set up commit message conventions
- [ ] Define when to commit (meaningful checkpoints)
- [ ] Plan weekly progress check-ins

#### 7.2 Issue Tracking & Backlog Management
- [ ] Set up GitHub Issues for backlog items
- [ ] Assign labels (bug, feature, enhancement, blocked)
- [ ] Create milestones for each sprint
- [ ] Link issues to Product Backlog tasks

#### 7.3 Testing & Code Review Strategy
- [ ] Plan manual testing approach
- [ ] Define code review checklist (even for solo dev: pre-submit checklist)
- [ ] Document acceptable test coverage for each sprint

**Deliverable:** `CONTRIBUTING.md` with workflow guidelines

---

### 8. Scope Validation & Planning (Day 5) [Half day]

#### 8.1 Quarter Feasibility Check
- [ ] Review Product Backlog against 10-week timeline
- [ ] Confirm MVP scope fits in Sprint 1-2
- [ ] Identify features that would be "scope creep"
- [ ] Define hard scope boundaries

#### 8.2 Sprint 1 Preparation
- [ ] Create Sprint 1 task list (from Product_Backlog.md EPIC 1-2)
- [ ] Estimate effort for Sprint 1 items
- [ ] Assign priority within Sprint 1
- [ ] Document Sprint 1 goals

**Deliverable:** `planning/Sprint_1_Plan.md` (draft, finalized in Sprint 1 kickoff)

---

## Deliverables Checklist

**Code & Configuration:**
- [ ] Git repository with clean history
- [ ] Project scaffold with working build
- [ ] `.gitignore`, `.env.example` configured
- [ ] Testing framework set up with passing test example
- [ ] Package manager with locked dependency versions

**Documentation:**
- [ ] `README.md` with project overview and quick start
- [ ] `docs/SETUP.md` with environment setup instructions
- [ ] `docs/TECH_DECISIONS.md` with framework choices and rationale
- [ ] `docs/ARCHITECTURE.md` with system architecture and API outline
- [ ] `docs/SCHEMA.md` with database design (draft)
- [ ] `docs/RISK_REGISTER.md` with risks and mitigations
- [ ] `CONTRIBUTING.md` with workflow and code style guidelines

**Planning:**
- [ ] Sprint 1 task list (detailed breakdown of EPIC 1-2)
- [ ] Updated Product_Backlog.md aligned with technical decisions
- [ ] Issue templates configured in GitHub

**Readiness Verification:**
- [ ] ✅ Project builds and runs locally
- [ ] ✅ Tests execute successfully (even if trivial)
- [ ] ✅ All team members (or self) aware of architecture choices
- [ ] ✅ Development workflow documented and ready to use

---

## Success Criteria for Sprint Zero

At the end of Sprint Zero, you should be able to answer:

1. **"Can I start coding tomorrow?"** → Yes, environment is ready
2. **"What am I building and why?"** → Architecture and tech stack documented
3. **"What could go wrong?"** → Risks identified with mitigation plans
4. **"How do I work on this project?"** → Workflow documented
5. **"What's my first sprint?"** → Sprint 1 tasks clearly defined
6. **"Can I test my code?"** → Testing framework ready

---

## Time Allocation

| Category | Days | Notes |
|----------|------|-------|
| Environment & Setup | 2 | Git, IDE, database, local dev |
| Technical Decisions | 2 | Stack, architecture, design patterns |
| Project Structure | 2 | Scaffold, folders, build config |
| Documentation | 1 | Architecture, schema, decisions |
| Risk & Quality | 1 | Risk register, testing framework |
| Workflow & Planning | 1 | Contributing guide, Sprint 1 prep |
| **TOTAL** | **~1 week** | Compressed timeline for student sprint |

---

## What Sprint Zero Does NOT Include

❌ Implementing user registration  
❌ Creating database tables  
❌ Building any UI components  
❌ Writing application business logic  
❌ Integrating third-party services  
❌ Performance optimization  

These belong in Sprint 1 and beyond.

---

## Sprint Zero Retrospective (End of Week 1)

Before starting Sprint 1, reflect on:

1. **Environment Setup:** Was the setup smooth? What took longer than expected?
2. **Technology Choices:** Do the selected tools still feel right?
3. **Documentation:** Is any critical information still missing?
4. **Risk Mitigation:** Are there new risks discovered during setup?
5. **Process:** Is the workflow actually practical, or does it need adjustment?

Document findings and adjust Sprint 1 if needed.

---

## Next Steps: Sprint 1 Kickoff

Once Sprint Zero is complete:
1. Schedule Sprint 1 planning (prioritize EPIC 1-2 from Product_Backlog)
2. Break down first user stories into smaller tasks
3. Begin implementation on backend infrastructure
4. Execute first meaningful development cycle

**Expected Sprint 1 Outcome:** Functional backend with authentication working (Users can register and log in)
