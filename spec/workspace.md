# Workspace Spec

## Purpose

Allow users to create top-level containers for notes and tasks.

## Version 1 Scope

- List workspaces
- Create workspace
- View workspace details
- Edit workspace
- Archive and unarchive workspace
- Delete workspace

## Frontend

Feature folder:

```text
src/features/workspace/
```

Main files:

- `pages/Workspaces.tsx`
- `pages/WorkspaceDetails.tsx`
- `components/WorkspaceForm.tsx`
- `components/WorkspaceCard.tsx`
- `components/DeleteWorkspaceDialog.tsx`
- `api/workspace-api.ts`
- `hooks/use-workspaces.ts`
- `hooks/use-workspace.ts`
- `hooks/use-create-workspace.ts`
- `hooks/use-update-workspace.ts`
- `hooks/use-archive-workspace.ts`
- `hooks/use-delete-workspace.ts`
- `schemas/workspace-schema.ts`
- `types/workspace.ts`

Expected behavior:

- `/workspaces` shows create form and workspace list.
- Empty state still allows creating the first workspace.
- Workspace cards link to `/workspaces/:id`.
- Details page allows edit, archive/unarchive, and delete.
- Mutations show toast feedback.

## Backend

DocType:

```text
Knowledge Hub Workspace
```

Fields:

- `title` - Data, required
- `description` - Small Text
- `archived` - Check, default 0

Custom APIs:

```text
GET /api/method/knowledge_hub.api.workspace.list_workspaces
GET /api/method/knowledge_hub.api.workspace.get_workspace
POST /api/method/knowledge_hub.api.workspace.create_workspace
POST /api/method/knowledge_hub.api.workspace.update_workspace
POST /api/method/knowledge_hub.api.workspace.archive_workspace
POST /api/method/knowledge_hub.api.workspace.delete_workspace
```

## Data and Permissions

- Use Frappe's built-in `owner`.
- List APIs return only current user's workspaces.
- Detail/update/archive/delete must verify ownership.
- Delete behavior must account for future child records.

## Definition of Done

- Workspace CRUD works end to end.
- Archive status is shown correctly.
- Delete requires confirmation.
- Forms validate title.
- Toasts appear for success and failure.
- Build passes.

## Learning Focus

- First complete full-stack module
- Frappe DocType and whitelisted APIs
- TanStack Query queries and mutations
- Shared forms with React Hook Form
- UI feedback with dialogs and toasts
