# Progress

Last updated: 2026-08-09

## Current Phase

Follow-up prioritization checkpoint.

Workspace, Notes, Tasks, Search, Dashboard, Profile, and Settings now have usable module foundations. Cross-module API error messages surface server details instead of only generic fallbacks. Settings, frontend polish, and regression checklist milestones are committed; the project is ready to prioritize follow-up hardening.

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
- Search module checkpoint completed.
- Dashboard backend started:
  - `knowledge_hub.api.dashboard.summary` added
  - summary includes workspace count, note count, pending task count, recent notes, and pending tasks
  - summary API is scoped to `frappe.session.user`
  - dashboard API syntax check passed with `python3 -m py_compile`
- Dashboard frontend started:
  - Dashboard TypeScript types added
  - Dashboard API function added
  - Dashboard React Query hook added
  - frontend build passes after Dashboard API/hook
  - Dashboard stats cards added
  - Dashboard recent notes section added
  - Dashboard pending tasks section added
  - Dashboard quick navigation actions added
  - frontend build passes after Dashboard page UI
  - reusable date formatting utility added
  - Dashboard recent note and task due dates use formatted dates
  - frontend build passes after date formatting
- Dashboard module checkpoint completed.
- Profile backend started:
  - `knowledge_hub.api.profile.get_profile` added
  - `knowledge_hub.api.profile.update_profile` added
  - `knowledge_hub.api.profile.change_password` added
  - profile API keeps email read-only for v1
  - password change verifies old password before updating
  - wrong current password returns validation error without clearing session
  - profile API syntax check passed with `python3 -m py_compile`
- Profile frontend started:
  - Profile TypeScript types added
  - Profile API functions added
  - Profile React Query hooks added
  - Profile mutation hooks include error toasts
  - frontend build passes after Profile API/hooks
  - Profile form schemas added
  - profile details form added
  - password change form added
  - frontend build passes after Profile forms
  - Profile page wired with account and password forms
  - frontend build passes after Profile page
  - Profile browser verification passed
- Cross-module UX improvements:
  - reusable API error parser added
  - workspace mutation hooks show server error messages
  - note mutation hooks show server error messages
  - task mutation hooks show server error messages
  - profile mutation hooks show server error messages
  - login page shows server error message
  - frontend build passes after API error-message updates
- Settings backend started:
  - `Knowledge Hub User Preference` DocType created
  - user preference DocType uses `user` as unique autoname field
  - theme Select supports System, Light, and Dark
  - preferences JSON storage added as Long Text
  - `knowledge_hub.api.settings.get_preferences` added
  - `knowledge_hub.api.settings.update_preferences` added
  - settings API syntax check passed with `python3 -m py_compile`
- Settings frontend started:
  - Settings TypeScript types added
  - Settings API functions added
  - Settings React Query hooks added
  - frontend build passes after Settings data layer
  - Settings preference form component added
  - frontend build passes after Settings preference form
  - Settings page wired to preferences query and update mutation
  - frontend build passes after Settings page wiring
  - `next-themes` provider added
  - saved Settings theme preference sync added
  - frontend build passes after theme application wiring
  - Settings theme preference verified in browser
  - Settings module checkpoint completed
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
- Frontend polish started:
  - `main.tsx` imports and provider setup formatting cleaned
  - `PrivateLayout.tsx` formatting cleaned
  - sidebar navigation icons and spacing added
  - reusable `PageHeader` component added
  - `PageHeader` applied to Settings, Dashboard, Notes, Search, Profile, Workspaces, and Tasks
  - Dashboard header actions moved into `PageHeader.actions`
  - Dashboard page formatting cleaned
  - Notes import order cleaned
  - Notes extra blank lines cleaned
  - Workspaces page formatting cleaned
  - Tasks page formatting cleaned
  - Search page formatting cleaned
  - Profile page formatting cleaned
  - mobile top navigation layout fixed
  - minor `PrivateLayout.tsx` class array typo fixed
  - Login page polished with shared UI components
  - Login page verified in light/dark modes
  - frontend build passes after Login polish
  - settings API syntax check passes after final review
  - frontend/backend changed-file review completed
  - backend Settings milestone committed
  - frontend Settings/polish milestone committed
- Regression checklist started:
  - `spec/regression-checklist.md` added
  - regression checklist milestone committed

## Next

1. Review and prioritize known follow-ups.
2. Choose the next hardening track.
3. Start the selected follow-up in a small checkpoint.

## Pending Modules

- None for MVP module foundation

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
- Profile v1 should keep email read-only and allow full name/password updates only.

## Manual Learning Checkpoints

- Explain how private route protection works.
- Explain why hooks must be called before conditional returns.
- Explain why Frappe session auth needs `withCredentials`.
- Explain TanStack Query invalidation after mutations.
- Explain why form default object identity matters.
