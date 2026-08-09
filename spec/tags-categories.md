# Tags and Categories Spec

## Purpose

Add lightweight organization tools so users can group and filter notes and tasks beyond workspaces.

Categories give each note or task one primary classification. Tags allow multiple flexible labels.

## Version 2 Scope

- Create, list, update, and archive categories.
- Create, list, update, and archive tags.
- Assign one category to a note.
- Assign one category to a task.
- Assign multiple tags to a note.
- Assign multiple tags to a task.
- Filter notes by workspace, category, and tag.
- Filter tasks by workspace, category, tag, status, and priority.
- Include category and tags in basic search results.

## Out of Scope for This Step

- Nested categories.
- Tag merge tools.
- Bulk edit.
- Shared/team taxonomies.
- Public tags.
- AI-generated tags.

## Frontend

Feature folder:

```text
src/features/taxonomy/
```

Expected files:

- `api/taxonomy-api.ts`
- `hooks/use-categories.ts`
- `hooks/use-tags.ts`
- `hooks/use-create-category.ts`
- `hooks/use-create-tag.ts`
- `hooks/use-update-category.ts`
- `hooks/use-update-tag.ts`
- `components/CategorySelect.tsx`
- `components/TagPicker.tsx`
- `components/CategoryForm.tsx`
- `components/TagForm.tsx`
- `components/CategoryBadge.tsx`
- `components/TagBadge.tsx`
- `schemas/taxonomy-schema.ts`
- `types/taxonomy.ts`

Existing feature updates:

- `NoteForm` should include category and tags.
- `TaskForm` should include category and tags.
- `Notes` should include category/tag filters.
- `Tasks` should include category/tag filters.
- `Search` should include category/tag filters after the base taxonomy flow works.

## Backend

DocTypes:

```text
Knowledge Hub Category
Knowledge Hub Tag
Knowledge Hub Note Tag
Knowledge Hub Task Tag
```

Suggested fields:

`Knowledge Hub Category`

- `title` - Data, required
- `description` - Small Text
- `color` - Data
- `archived` - Check, default 0
- `owner` - Frappe owner

`Knowledge Hub Tag`

- `title` - Data, required
- `color` - Data
- `archived` - Check, default 0
- `owner` - Frappe owner

`Knowledge Hub Note`

- Add `category` - Link to Knowledge Hub Category
- Add `tags` - Table to Knowledge Hub Note Tag

`Knowledge Hub Task`

- Add `category` - Link to Knowledge Hub Category
- Add `tags` - Table to Knowledge Hub Task Tag

`Knowledge Hub Note Tag`

- `tag` - Link to Knowledge Hub Tag

`Knowledge Hub Task Tag`

- `tag` - Link to Knowledge Hub Tag

Custom APIs:

```text
list_categories
create_category
update_category
archive_category
delete_category

list_tags
create_tag
update_tag
archive_tag
delete_tag
```

Existing API updates:

- `create_note` accepts `category` and `tags`.
- `update_note` accepts `category` and `tags`.
- `list_notes` accepts `category` and `tag` filters.
- `get_note` returns category and tags.
- `create_task` accepts `category` and `tags`.
- `update_task` accepts `category` and `tags`.
- `list_tasks` accepts `category` and `tag` filters.
- `get_task` returns category and tags.
- `global_search` can filter by category and tag after note/task filtering is stable.

## Data and Permissions

- Categories and tags belong to the current user.
- Notes and tasks may only reference categories and tags owned by the current user.
- Backend must validate category and tag ownership before create/update.
- List APIs must return only the current user's taxonomy records.
- Archive should be the default safe action for categories/tags already used by notes or tasks.
- Delete should be protected when linked records exist.

## Definition of Done

- Category and tag backend DocTypes exist.
- Taxonomy APIs are covered by integration tests.
- Note and task APIs support category and tags.
- Note and task API tests cover category/tag ownership validation.
- Frontend forms can assign category and tags.
- Notes and tasks pages can filter by category and tag.
- Search can include category/tag filters or clearly defer them to the next checkpoint.
- Backend test suite passes.
- Frontend build passes.

## Learning Focus

- One-to-many versus many-to-many modeling.
- Frappe Link fields and child tables.
- Shared feature modules in React.
- Cross-feature query invalidation.
- Filter state in URL/query params.
- Backend ownership validation for linked records.
