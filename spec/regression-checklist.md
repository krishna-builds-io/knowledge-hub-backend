# Regression Checklist

## Auth

- Login with valid credentials
- Login with wrong password shows a useful error
- Logout redirects to login
- Private pages redirect to login when session is missing

## Workspaces

- Create workspace
- Edit workspace
- Archive workspace
- Unarchive workspace
- Delete workspace

## Notes

- Create note with workspace
- Filter notes by workspace
- Edit note
- Favorite/unfavorite note
- Archive note
- Delete note

## Tasks

- Create task with workspace, status, priority, and due date
- Edit task
- Complete task
- Reopen task
- Delete task

## Search

- Search workspaces
- Search notes
- Search tasks
- Empty search state looks correct

## Dashboard

- Workspace count looks correct
- Note count looks correct
- Pending task count looks correct
- Recent notes date format is readable
- Pending tasks show priority and due date

## Profile

- Update profile name
- Wrong current password shows useful error
- Correct password change works
- Session is not cleared after wrong current password

## Settings

- Change theme to Light
- Change theme to Dark
- Change theme to System
- Refresh and theme persists
- Login page looks good in light and dark mode

## Responsive UI

- Mobile top navigation looks clean
- Main pages do not overflow horizontally
- Forms and buttons fit mobile width