# Notes Spec

## Purpose

Allow users to store knowledge inside workspaces.

## Version 1 Scope

- List notes
- Create note
- View note details
- Edit note
- Delete note
- Archive note
- Favorite note
- Basic search support
- Plain text or markdown-style content

## Future Scope

- Rich text editor
- Tags
- Categories
- File attachments

## Frontend

Feature folder:

```text
src/features/notes/
```

Expected files:

- `pages/Notes.tsx`
- `pages/NoteDetails.tsx`
- `components/NoteForm.tsx`
- `components/NoteCard.tsx`
- `api/note-api.ts`
- `hooks/use-notes.ts`
- `hooks/use-note.ts`
- `hooks/use-create-note.ts`
- `hooks/use-update-note.ts`
- `hooks/use-delete-note.ts`
- `hooks/use-archive-note.ts`
- `hooks/use-favorite-note.ts`
- `schemas/note-schema.ts`
- `types/note.ts`

## Backend

DocType:

```text
Knowledge Hub Note
```

Suggested fields:

- `title` - Data, required
- `content` - Long Text
- `content_type` - Select, default `plain_text`
- `workspace` - Link to Knowledge Hub Workspace
- `favorite` - Check, default 0
- `archived` - Check, default 0

Custom APIs:

```text
list_notes
get_note
create_note
update_note
archive_note
favorite_note
delete_note
```

## Data and Permissions

- Notes belong to the current user.
- Notes may optionally belong to a workspace.
- Backend must verify ownership of the note and workspace.

## Definition of Done

- Notes can be created and listed.
- Note details can be viewed and edited.
- Archive/favorite/delete actions work.
- Empty/loading/error states exist.
- Build passes.

## Learning Focus

- Parent-child data with Workspace
- Text editing forms
- Query invalidation across related entities
- Searchable content model
