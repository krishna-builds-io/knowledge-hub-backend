# Progress

Last updated: 2026-08-08

## Current Phase

Notes module checkpoint ready to commit.

Workspace and Notes now have usable module foundations. Notes backend and frontend require the Note `workspace` link, and browser verification with real records passed.

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
- Notes frontend started:
  - notes list
  - create note dialog
  - note details/edit page
  - archive/favorite/delete actions
  - workspace picker in note form
  - required workspace TypeScript payloads
  - workspace filter on notes list
- Notes workspace relationship aligned:
  - Note DocType `workspace` field is required
  - Note API rejects create/update without workspace
  - frontend schema requires workspace
  - frontend build passes after workspace filter change
  - browser verification passed with real workspace-linked notes
- Shared UI components started:
  - button
  - card
  - input
  - label
  - textarea
  - badge
  - dialog
  - select
  - sonner/toaster
- UI primitives migrated from Base UI to Radix UI.

## Next

1. Commit Notes module checkpoint.
2. Start Tasks backend DocType.

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
- Notes module is ready for a checkpoint commit.
- Route-level code splitting can be added later.
- Realtime synchronization can be added later with Frappe realtime events and React Query invalidation.

## Manual Learning Checkpoints

- Explain how private route protection works.
- Explain why hooks must be called before conditional returns.
- Explain why Frappe session auth needs `withCredentials`.
- Explain TanStack Query invalidation after mutations.
- Explain why form default object identity matters.
