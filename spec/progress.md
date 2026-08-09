# Progress

Last updated: 2026-08-09

## Current Phase

Search checkpoint ready to commit.

Workspace, Notes, Tasks, and Search now have usable module foundations. Search page includes debounced querying and is ready for checkpoint commit.

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
- Notes module checkpoint completed.
- Tasks backend started:
  - `Knowledge Hub Task` DocType created
  - task `workspace` field is required
  - task status, priority, due date, and completed fields exist
  - Task API file added
  - task API syntax check passed with `python3 -m py_compile`
  - Task APIs manually verified
- Tasks frontend started:
  - Task TypeScript types added
  - Task API functions added
  - Task React Query hooks added
  - Task mutation hooks include error toasts
  - frontend build passes after Task hooks
  - Tasks list page added
  - Task card added
  - Task status and priority badges added
  - frontend build passes after Tasks list page
  - task form schema added
  - reusable `TaskForm` added
  - `CreateTaskDialog` added
  - `Add Task` button wired into `Tasks.tsx`
  - frontend build passes after create task flow
  - Due Date label association fixed in `TaskForm`
  - `TaskDetails.tsx` added
  - task edit flow added
  - complete/reopen action added
  - frontend build passes after Task details page
  - delete task dialog added
  - delete task action wired into `TaskDetails.tsx`
  - frontend build passes after delete action
  - browser verification passed for task create/list/detail/edit/complete/delete
- Tasks module checkpoint completed.
- Search backend started:
  - `knowledge_hub.api.search.global_search` added
  - global search supports workspaces, notes, tasks, and all types
  - global search is scoped to `frappe.session.user`
  - search API syntax check passed with `python3 -m py_compile`
- Search frontend started:
  - Search TypeScript types added
  - Search API function added
  - Search React Query hook added
  - frontend build passes after Search API/hook
  - Search result card added
  - Search page input and type filter added
  - Search empty/loading/error states added
  - frontend build passes after Search page UI
  - Search browser verification passed
  - reusable debounce hook added
  - Search page uses debounced query input
  - frontend build passes after debounce
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

1. Optionally rename `debounceQuery` to `debouncedQuery` for readability.
2. Commit Search module checkpoint.
3. Start Dashboard module.

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
- Tasks spec currently says workspace is optional, but implementation now uses required workspace for consistency with Notes.
- Required-field `*` indicators are intentionally deferred; validation remains handled by Zod/React Hook Form.
- Route-level code splitting can be added later.
- Realtime synchronization can be added later with Frappe realtime events and React Query invalidation.
- Search API permission behavior was manually verified by user.

## Manual Learning Checkpoints

- Explain how private route protection works.
- Explain why hooks must be called before conditional returns.
- Explain why Frappe session auth needs `withCredentials`.
- Explain TanStack Query invalidation after mutations.
- Explain why form default object identity matters.
