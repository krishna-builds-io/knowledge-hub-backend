# Progress

Last updated: 2026-08-01

## Current Phase

UI primitive migration and Workspace module UI foundation.

Before starting Notes, improve the shared layout and workspace UI so future modules inherit a better page structure.

## Completed

- Product documents aligned:
  - `PRD.md`
  - `FBD.md`
  - `SDD.md`
- Frontend repository separated from backend repository.
- React + TypeScript + Vite frontend created.
- React Router configured.
- Public and private layouts added.
- MVP placeholder routes added.
- API client configured with Axios.
- TanStack Query configured.
- Authentication frontend flow added:
  - login form
  - current user query
  - protected routes
  - public-only login route
  - logout flow
  - current user sidebar display
- Workspace backend started:
  - Workspace DocType
  - Workspace API endpoints
- Workspace frontend started:
  - list workspaces
  - create workspace
  - create workspace dialog
  - workspace cards
  - workspace details
  - edit workspace
  - archive/unarchive workspace
  - delete workspace with dialog
  - toast feedback
- Shared UI components started:
  - button
  - card
  - input
  - label
  - textarea
  - badge
  - dialog
  - sonner/toaster
- UI primitives migrated from Base UI to Radix UI.

## In Progress

- Workspace UI polish:
  - app shell spacing
  - private layout padding
  - page containers
  - Workspaces page form card
  - Workspaces page grid
  - action grouping
  - archived state rendering

## Next

1. Fix archived value rendering so `0` does not appear in React.
2. Polish Workspace Details page with a header, edit card, and action grouping.
3. Review UI in browser at desktop width.
4. Commit workspace module checkpoint.
5. Start Notes backend DocType.

## Pending Modules

- Dashboard
- Notes
- Tasks
- Search
- Profile
- Settings

## Known Issues / Follow-ups

- Vite build shows a bundle-size warning. This is acceptable for now.
- UI components now use Radix UI primitives through shadcn/ui.
- Workspace archived fields may arrive from Frappe as `0` or `1`; normalize or cast before rendering.
- Workspace form reset/default handling should be watched while editing.
- Delete workspace behavior must be revisited when notes/tasks become child records.
- Route-level code splitting can be added later.
- Realtime synchronization can be added later with Frappe realtime events and React Query invalidation.

## Manual Learning Checkpoints

- Explain how private route protection works.
- Explain why hooks must be called before conditional returns.
- Explain why Frappe session auth needs `withCredentials`.
- Explain TanStack Query invalidation after mutations.
- Explain why form default object identity matters.
