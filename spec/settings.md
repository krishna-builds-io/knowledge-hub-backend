# Settings Spec

## Purpose

Allow users to control application preferences.

## Version 1 Scope

- Theme setting
- Basic preferences storage

## Future Scope

- Notification preferences
- Advanced preferences
- Workspace defaults

## Frontend

Feature folder:

```text
src/features/settings/
```

Expected files:

- `pages/Settings.tsx`
- `components/ThemeSelector.tsx`
- `components/PreferenceForm.tsx`
- `api/settings-api.ts`
- `hooks/use-preferences.ts`
- `hooks/use-update-preferences.ts`
- `types/settings.ts`

## Backend

DocType:

```text
Knowledge Hub User Preference
```

Suggested fields:

- `user` - Link to User
- `theme` - Select
- `preferences_json` - JSON or Long Text

Custom APIs:

```text
GET /api/method/knowledge_hub.api.settings.get_preferences
POST /api/method/knowledge_hub.api.settings.update_preferences
```

## Data and Permissions

- Each user has one preference record.
- Backend should create defaults when preferences do not exist.
- Users can only access their own preferences.

## Definition of Done

- Theme can be changed.
- Preference changes persist after refresh.
- Loading/error states exist.
- Build passes.

## Learning Focus

- App-level state versus server state
- Theme management
- User-specific settings
