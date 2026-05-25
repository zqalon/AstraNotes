# AstraNotes User Stories

**Requirement ID Cross-Reference:**
- US-1 → F-001a (User registration)
- US-2 → F-001b, F-001d (Secure login, Session management)
- US-3 → F-002a (Create new notes)
- US-4 → F-002b (View/read notes)
- US-5 → F-002c (Edit existing notes)
- US-6 → F-002d (Delete notes with recovery)
- US-7 → F-003b, F-003c (Search and filter notes)
- US-8 → F-005 (Desktop GUI Application)

---

## User Story 1: User Registration
**Requirement ID:** F-001a (User registration with email/username and password)  
**As a** new user  
**I want to** register an account with a valid email and password  
**So that** I can create a secure account to store my notes

**Acceptance Criteria:**
- User can provide email/username and password (F-001a)
- Password must meet minimum security requirements (SEC-001b)
- System validates email format (SEC-001e)
- Confirmation message on successful registration (F-001a)

---

## User Story 2: User Login & Session Management
**Requirement ID:** F-001b, F-001d (Secure login/logout, Session management)  
**As a** registered user  
**I want to** log in with my credentials and maintain a secure session  
**So that** I can access my notes securely with automatic timeout protection

**Acceptance Criteria:**
- User can log in with email/username and password (F-001b)
- Session persists during active use (F-001d)
- Session automatically times out after inactivity (F-001d)
- User receives warning before session expires (F-001d)

---

## User Story 3: Create New Notes
**Requirement ID:** F-002a (Create new notes with title, content, and optional metadata)  
**As a** logged-in user  
**I want to** create a new note with a title and content  
**So that** I can start capturing my ideas and information

**Acceptance Criteria:**
- User can enter note title and content (F-002a)
- Optional metadata fields are available (F-002a)
- Note is saved to the system (F-002a)
- Confirmation message displayed on success (F-002a)

---

## User Story 4: View and Read Notes
**Requirement ID:** F-002b (Read/view notes - individual and list views)  
**As a** logged-in user  
**I want to** view a list of all my notes and read individual notes  
**So that** I can find and review the information I've saved

**Acceptance Criteria:**
- List view displays all notes with titles and timestamps (F-002b)
- User can click on a note to view full content (F-002b)
- Note details include creation/modification dates (F-002b)
- Navigation between notes is smooth (F-002b)

---

## User Story 5: Edit Existing Notes
**Requirement ID:** F-002c (Update/edit existing notes)  
**As a** logged-in user  
**I want to** edit the content and title of my existing notes  
**So that** I can update information and correct any mistakes

**Acceptance Criteria:**
- User can modify note title and content (F-002c)
- Changes are saved automatically or on user action (F-002c)
- Note modification timestamp is updated (F-002c)
- User can discard changes before save (F-002c)

---

## User Story 6: Delete Notes with Recovery
**Requirement ID:** F-002d (Delete notes with soft delete and recovery option)  
**As a** logged-in user  
**I want to** delete notes with the option to recover them  
**So that** I can remove unwanted notes but recover them if deleted by mistake

**Acceptance Criteria:**
- User can delete a note with confirmation (F-002d)
- Deleted notes are soft-deleted (not permanently removed immediately) (F-002d)
- Recovery option is available within a recovery period (F-002d)
- Permanent deletion option exists for verified deletion (F-002d)

---

## User Story 7: Search and Filter Notes
**Requirement ID:** F-003b, F-003c (Search functionality, Sorting and filtering)  
**As a** logged-in user  
**I want to** search notes by keyword and filter by category or date  
**So that** I can quickly find the notes I need

**Acceptance Criteria:**
- Full-text search works across note titles and content (F-003b)
- Filter options available by date, category, and tags (F-003c)
- Search results are displayed with relevance (F-003b)
- Filters can be combined for refined searches (F-003c)

---

## User Story 8: Desktop GUI Application
**Requirement ID:** F-005 (Graphical User Interface)  
**As a** desktop user  
**I want to** use a cross-platform graphical application with an intuitive note editor  
**So that** I can manage my notes with a user-friendly visual interface

**Acceptance Criteria:**
- Application runs on Windows, macOS, and Linux (F-005a)
- Intuitive note editor with formatting options (F-005b)
- Tree view displays categories and notes (F-005c)
- Search and filter interface is accessible (F-005d)
- Keyboard shortcuts are available (F-004c)
- Intuitive note editor with formatting tools (bold, italic, lists, etc.)
- Tree view displays note organization and hierarchy
- Keyboard shortcuts available for common actions
- Responsive design adapts to different window sizes

