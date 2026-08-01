# Profile Spec

## Purpose

Allow users to view and update basic account information.

## Version 1 Scope

- View profile
- Update profile fields supported by Frappe
- Change password

## Future Scope

- Avatar upload
- Account preferences
- Profile activity summary

## Frontend

Feature folder:

```text
src/features/profile/
```

Expected files:

- `pages/Profile.tsx`
- `components/ProfileForm.tsx`
- `components/PasswordForm.tsx`
- `api/profile-api.ts`
- `hooks/use-profile.ts`
- `hooks/use-update-profile.ts`
- `hooks/use-change-password.ts`
- `schemas/profile-schema.ts`
- `types/profile.ts`

## Backend

Use Frappe `User`.

Custom APIs:

```text
GET /api/method/knowledge_hub.api.profile.get_profile
POST /api/method/knowledge_hub.api.profile.update_profile
POST /api/method/knowledge_hub.api.profile.change_password
```

## Data and Permissions

- User can only read and update their own profile.
- Password changes must require the old password or use Frappe's supported flow.

## Definition of Done

- Profile page displays current user data.
- Supported profile fields can be updated.
- Password can be changed safely.
- Success/error feedback exists.
- Build passes.

## Learning Focus

- Updating Frappe User safely
- Sensitive form handling
- Separate forms on one page
