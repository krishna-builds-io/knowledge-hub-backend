# Search Spec

## Purpose

Allow users to quickly find workspaces, notes, and tasks.

## Version 1 Scope

- Global search route
- Search workspaces
- Search notes
- Search tasks
- Basic result cards

## Future Scope

- Advanced filters
- Saved searches
- Full-text ranking
- Highlighted matches

## Frontend

Feature folder:

```text
src/features/search/
```

Expected files:

- `pages/Search.tsx`
- `components/SearchInput.tsx`
- `components/SearchResultCard.tsx`
- `components/SearchFilters.tsx`
- `api/search-api.ts`
- `hooks/use-search.ts`
- `types/search.ts`

## Backend

Custom API:

```text
GET /api/method/knowledge_hub.api.search.global_search
```

Suggested query params:

- `q`
- `type`

Result types:

- `workspace`
- `note`
- `task`

## Data and Permissions

- Search must only return records owned by the logged-in user.
- Results should include enough data to navigate to the detail page.

## Definition of Done

- Search page accepts a query.
- Results are grouped or labeled by type.
- Empty/loading/error states exist.
- Search does not expose another user's data.
- Build passes.

## Learning Focus

- Query params
- Debounced input
- Cross-entity API design
- Search result modeling
