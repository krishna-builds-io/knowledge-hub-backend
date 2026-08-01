# Dashboard Spec

## Purpose

Give the user a quick overview of their Knowledge Hub activity.

## Version 1 Scope

- Welcome section
- Workspace summary
- Recent notes
- Pending tasks
- Quick navigation actions

## Frontend

Feature folder:

```text
src/features/dashboard/
```

Main files:

- `pages/Dashboard.tsx`
- Future: `api/dashboard-api.ts`
- Future: `hooks/use-dashboard-summary.ts`
- Future: `components/StatsCard.tsx`
- Future: `components/RecentNotes.tsx`
- Future: `components/PendingTasks.tsx`

Expected behavior:

- Dashboard loads after login.
- User sees useful high-level counts and recent items.
- Empty states appear when there are no notes/tasks/workspaces.

## Backend

Custom API:

```text
GET /api/method/knowledge_hub.api.dashboard.summary
```

Expected response should include:

- workspace count
- note count
- pending task count
- recent notes
- pending tasks

## Data

Dashboard summarizes:

- Workspaces
- Notes
- Tasks

All data must be filtered to the logged-in user.

## Definition of Done

- Dashboard route renders inside private layout.
- Summary API exists.
- Loading, error, empty, and success states are handled.
- Cards use shared UI components.
- Build passes.

## Learning Focus

- Aggregated API design
- Server-state loading states
- Reusable dashboard cards
- Empty state design
