This is the document that will keep our project consistent from the first commit to the last.

The **PRD** answered **"Why are we building this?"**
The **FBD** answered **"What are we building?"**
The **SDD** answers **"How are we going to build it?"**

---

# System Design Document (SDD)

## Project

**Knowledge Hub**

---

# 1. High-Level Architecture

```text
                    User
                     │
                     ▼
        React Frontend (Vite)
                     │
        React Router / Components
                     │
         TanStack Query / Axios
                     │
────────────────────────────────────
          HTTP REST API
────────────────────────────────────
                     │
              Frappe Backend
                     │
        DocTypes + Business Logic
                     │
                MariaDB Database
```

**Key Principle**

* React is responsible for the UI.
* Frappe is responsible for data, authentication, permissions, and business logic.
* React never accesses the database directly.

---

# 2. Project Repositories

We will keep the frontend and backend independent.

For learning and local Frappe Bench development, the backend can live inside the Frappe app workspace and the frontend can live in a dedicated frontend folder or a separate repository. The important rule is that React communicates with Frappe only through APIs.

```text
knowledge-hub/

├── knowledge-hub-frontend/
│
└── knowledge-hub-backend/
```

### Frontend

* React
* TypeScript
* Vite

### Backend

* Frappe
* Custom App

---

# 3. Frontend Architecture

We will use **Feature-Based Architecture**.

```text
src/

├── app/
│
├── assets/
│
├── components/
│   ├── ui/
│   ├── common/
│   └── layout/
│
├── features/
│   ├── auth/
│   ├── dashboard/
│   ├── workspace/
│   ├── notes/
│   ├── tasks/
│   ├── search/
│   ├── profile/
│   └── settings/
│
├── hooks/
│
├── services/
│
├── lib/
│
├── routes/
│
├── types/
│
├── utils/
│
└── main.tsx
```

### Why Feature-Based?

As the application grows, all code related to a feature stays together.

Example:

```text
features/

notes/

    components/

    hooks/

    api/

    pages/

    types/

    utils/
```

---

# 4. Backend Architecture

We'll create a dedicated Frappe app.

```text
knowledge_hub/

doctype/
    knowledge_hub_workspace/
    knowledge_hub_note/
    knowledge_hub_task/
    knowledge_hub_user_preference/
    knowledge_hub_category/
    knowledge_hub_tag/
    knowledge_hub_note_tag/
    knowledge_hub_task_tag/

api/
    auth.py
    dashboard.py
    workspace.py
    note.py
    task.py
    search.py
    profile.py
    settings.py
    taxonomy.py

utils/

patches/

public/

hooks.py
```

The backend exposes only APIs required by the frontend.

The backend owns validation, permission checks, and user-specific data filtering.

---

# 5. Authentication Design

We will use **Frappe Session Authentication**.

Flow:

```text
Login Page

↓

POST /api/method/login

↓

Cookie Stored

↓

React checks session

↓

Dashboard
```

If the session expires:

```text
401

↓

Redirect Login
```

### Session Rules

* Frontend requests must send cookies with API requests.
* State-changing requests must include Frappe's CSRF token when required.
* If the frontend and backend run on different origins during development, CORS must allow only the configured frontend origin.
* Logout clears the session and redirects the user to the login page.

---

# 6. Routing Strategy

```text
/

↓

login

↓

dashboard

↓

workspaces

↓

workspaces/:id

↓

notes

↓

notes/:id

↓

tasks

↓

tasks/:id

↓

search

↓

profile

↓

profile/password

↓

settings
```

### Layout

```text
App

│

├── Public Layout

│     └── Login

│

└── Private Layout

      ├── Sidebar

      ├── Navbar

      └── Pages
```

---

# 7. Data Model

## Workspace

```text
Workspace

name

title

description

owner

archived

created_at

updated_at
```

---

## Note

```text
Note

name

title

content

content_type

workspace

category

tags

favorite

archived

owner

created_at

updated_at
```

---

## Task

```text
Task

name

title

description

status

priority

workspace

category

tags

due_date

completed

owner

created_at

updated_at
```

---

## User

Use Frappe User.

No custom user model initially.

---

## User Preference

```text
Knowledge Hub User Preference

name

user

theme

preferences_json

created_at

updated_at
```

---

## Category

```text
Knowledge Hub Category

name

title

description

color

archived

owner

created_at

updated_at
```

---

## Tag

```text
Knowledge Hub Tag

name

title

color

archived

owner

created_at

updated_at
```

---

## Note Tag

```text
Knowledge Hub Note Tag

tag
```

---

## Task Tag

```text
Knowledge Hub Task Tag

tag
```

---

# 8. Entity Relationships

```text
User

│

├── Workspace (1:N)

│        │

│        ├── Notes (1:N)

│        │

│        └── Tasks (1:N)

├── Categories (1:N)

├── Tags (1:N)

└── User Preference (1:1)
```

One user can own multiple workspaces.

Each workspace contains notes and tasks.

Each note and task can have one category.

Each note and task can have many tags.

Each user has one preferences record for Knowledge Hub-specific settings.

---

# 8.1 Data Ownership and Permissions

All Version 1 data is private to the logged-in user.

Rules:

* Workspace, Note, Task, and User Preference records must include an owner or user reference.
* Category and Tag records must include an owner.
* List APIs return only records owned by the logged-in user.
* Detail, update, delete, archive, favorite, and complete APIs must verify ownership before changing data.
* Note and Task create/update APIs must verify ownership of linked workspace, category, and tags.
* React must never trust hidden form values such as owner; the backend sets ownership from the active session.
* Deleting a workspace must define what happens to child notes and tasks before implementation. Version 1 should use either protected delete when children exist or a soft archive flow.

---

# 9. API Design

Every feature gets its own API layer.

All custom APIs should live under:

```text
/api/method/knowledge_hub.api.<module>.<method>
```

Authentication

```text
POST /api/method/login

POST /api/method/logout

GET /api/method/knowledge_hub.api.auth.current_user
```

Dashboard

```text
GET /api/method/knowledge_hub.api.dashboard.summary
```

Workspace

```text
GET /api/method/knowledge_hub.api.workspace.list_workspaces

GET /api/method/knowledge_hub.api.workspace.get_workspace

POST /api/method/knowledge_hub.api.workspace.create_workspace

POST /api/method/knowledge_hub.api.workspace.update_workspace

POST /api/method/knowledge_hub.api.workspace.delete_workspace

POST /api/method/knowledge_hub.api.workspace.archive_workspace
```

Notes

```text
GET /api/method/knowledge_hub.api.note.list_notes

GET /api/method/knowledge_hub.api.note.get_note

POST /api/method/knowledge_hub.api.note.create_note

POST /api/method/knowledge_hub.api.note.update_note

POST /api/method/knowledge_hub.api.note.delete_note

POST /api/method/knowledge_hub.api.note.archive_note

POST /api/method/knowledge_hub.api.note.favorite_note
```

Tasks

```text
GET /api/method/knowledge_hub.api.task.list_tasks

GET /api/method/knowledge_hub.api.task.get_task

POST /api/method/knowledge_hub.api.task.create_task

POST /api/method/knowledge_hub.api.task.update_task

POST /api/method/knowledge_hub.api.task.delete_task

POST /api/method/knowledge_hub.api.task.complete_task
```

Search

```text
GET /api/method/knowledge_hub.api.search.global_search
```

Profile

```text
GET /api/method/knowledge_hub.api.profile.get_profile

POST /api/method/knowledge_hub.api.profile.update_profile

POST /api/method/knowledge_hub.api.profile.change_password
```

Settings

```text
GET /api/method/knowledge_hub.api.settings.get_preferences

POST /api/method/knowledge_hub.api.settings.update_preferences
```

Taxonomy

```text
GET /api/method/knowledge_hub.api.taxonomy.list_categories

POST /api/method/knowledge_hub.api.taxonomy.create_category

POST /api/method/knowledge_hub.api.taxonomy.update_category

POST /api/method/knowledge_hub.api.taxonomy.archive_category

POST /api/method/knowledge_hub.api.taxonomy.delete_category

GET /api/method/knowledge_hub.api.taxonomy.list_tags

POST /api/method/knowledge_hub.api.taxonomy.create_tag

POST /api/method/knowledge_hub.api.taxonomy.update_tag

POST /api/method/knowledge_hub.api.taxonomy.archive_tag

POST /api/method/knowledge_hub.api.taxonomy.delete_tag
```

---

# 10. React State Strategy

We'll intentionally use different state solutions for different problems.

### Local UI State

Examples:

* Modal open
* Selected tab
* Form values

Tool:

```text
useState
```

---

### Shared UI State

Examples:

* Theme
* Sidebar
* Auth UI flags

Tool:

```text
Context API
```

---

### Server State

Examples:

* Current user
* Notes
* Tasks
* Workspaces
* Dashboard summary
* Search results

Tool:

```text
TanStack Query
```

The current user is fetched as server state and exposed through an AuthProvider for routing and layout decisions.

This separation helps avoid unnecessary complexity.

---

# 11. Error Handling

Every API call must handle:

```text
Loading

Success

Empty

Error
```

Each page will explicitly account for all four states.

---

# 12. UI Component Hierarchy

```text
App

↓

Layout

↓

Page

↓

Feature Component

↓

Shared Component

↓

Primitive UI
```

Example:

```text
Dashboard

↓

WorkspaceGrid

↓

WorkspaceCard

↓

Card

↓

Button
```

We always build from general to specific.

---

# 13. Coding Standards

### Naming

Components

```text
PascalCase
```

Variables

```text
camelCase
```

Constants

```text
UPPER_CASE
```

Hooks

```text
useSomething()
```

Files

```text
Component files: PascalCase.tsx

Examples: Login.tsx, Dashboard.tsx, WorkspaceCard.tsx

Non-component files: kebab-case.ts

Examples: auth-api.ts, date-utils.ts, query-client.ts
```

Types

```text
Workspace

Task

Note
```

Avoid abbreviations unless they are universally understood (e.g., `API`, `URL`).

---

# 14. Component Rules

Each component should have a single responsibility.

Good:

```text
Button

Card

Avatar

SearchInput
```

Avoid large, multi-purpose components that handle unrelated concerns.

---

# 15. Git Strategy

Main branches:

```text
main

develop
```

Feature branches:

```text
feature/auth

feature/workspace

feature/notes

feature/tasks
```

One pull request per feature.

---

# 16. Build Order

```text
1. Project Setup

2. Routing

3. Authentication

4. Layout

5. Workspace

6. Notes

7. Tasks

8. Dashboard

9. Search

10. Profile

11. Settings

12. Performance

13. Deployment
```

Each stage depends on the previous one being complete.

---

# 17. Future Extensions

The architecture should allow us to add:

* Comments
* File uploads
* Rich text editing
* Real-time collaboration
* Notifications
* Team workspaces
* AI assistance

without major restructuring.

---

# Architecture Principles

These principles will guide our decisions throughout the project:

1. **Separation of Concerns** – UI, business logic, and data access remain clearly separated.
2. **Feature First** – Organize code around features rather than file types.
3. **Single Responsibility** – Components, hooks, and APIs each do one job well.
4. **Reusable by Default** – Shared functionality belongs in reusable components or hooks.
5. **Type Safety** – Prefer TypeScript types over `any`.
6. **Backend Owns Business Rules** – Validation and business logic live in Frappe; React focuses on presentation and user interaction.
7. **Introduce Complexity Only When Needed** – We'll start with simple React patterns and add advanced techniques only when they solve real problems.

---
