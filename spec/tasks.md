# Tasks Spec

## Purpose

Allow users to track work items inside workspaces.

## Version 1 Scope

- List tasks
- Create task
- View task details
- Edit task
- Delete task
- Mark complete/incomplete
- Set status
- Set priority
- Set due date

## Version 2 Scope

- Assign one category to a task
- Assign multiple tags to a task
- Filter tasks by category and tag
- Include category and tags in task detail/list responses

## Frontend

Feature folder:

```text
src/features/tasks/
```

Expected files:

- `pages/Tasks.tsx`
- `pages/TaskDetails.tsx`
- `components/TaskForm.tsx`
- `components/TaskCard.tsx`
- `components/StatusBadge.tsx`
- `components/PriorityBadge.tsx`
- `api/task-api.ts`
- `hooks/use-tasks.ts`
- `hooks/use-task.ts`
- `hooks/use-create-task.ts`
- `hooks/use-update-task.ts`
- `hooks/use-delete-task.ts`
- `hooks/use-complete-task.ts`
- `schemas/task-schema.ts`
- `types/task.ts`

## Backend

DocType:

```text
Knowledge Hub Task
```

Suggested fields:

- `title` - Data, required
- `description` - Small Text or Long Text
- `status` - Select
- `priority` - Select
- `workspace` - Link to Knowledge Hub Workspace
- `category` - Link to Knowledge Hub Category
- `tags` - Table to Knowledge Hub Task Tag
- `due_date` - Date
- `completed` - Check, default 0

Custom APIs:

```text
list_tasks
get_task
create_task
update_task
complete_task
delete_task
```

## Data and Permissions

- Tasks belong to the current user.
- Tasks belong to a workspace.
- Backend must verify ownership of the task, workspace, category, and tags before reads and writes.

## Definition of Done

- Tasks can be created, listed, updated, completed, and deleted.
- Priority and status are visible.
- Due dates render clearly.
- Empty/loading/error states exist.
- Build passes.

## Learning Focus

- Status modeling
- Date fields
- Optimistic or invalidated updates
- Reusable badges and list cards
