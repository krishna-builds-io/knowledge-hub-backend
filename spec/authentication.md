# Authentication Spec

## Purpose

Allow a user to securely access Knowledge Hub using Frappe session authentication.

## Version 1 Scope

- Login
- Logout
- Current user session check
- Protected private routes
- Redirect authenticated users away from login

## Frontend

Feature folder:

```text
src/features/auth/
```

Main files:

- `pages/Login.tsx`
- `api/auth-api.ts`
- `hooks/use-current-user.ts`
- `hooks/use-login.ts`
- `hooks/use-logout.ts`
- `schemas/login-schema.ts`

Expected behavior:

- `/login` shows the login form for guests.
- Successful login redirects to `/`.
- Private pages redirect guests to `/login`.
- Logout clears React Query cache and redirects to `/login`.

## Backend

Backend uses Frappe's built-in session authentication.

Custom API:

```text
GET /api/method/knowledge_hub.api.auth.current_user
```

Built-in APIs:

```text
POST /api/method/login
POST /api/method/logout
```

## Data

Use Frappe `User`.

No custom user DocType in Version 1.

## Definition of Done

- Login works with valid Frappe credentials.
- Invalid login shows an error.
- Private routes are protected.
- Logged-in users cannot stay on `/login`.
- Logout works.
- Current user appears in the sidebar.
- Build passes.

## Learning Focus

- Frappe session auth
- Cookies and `withCredentials`
- React Router guards
- TanStack Query for current user state
- React Hook Form and Zod validation
