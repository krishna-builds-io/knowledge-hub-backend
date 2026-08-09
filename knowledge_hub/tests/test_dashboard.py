import frappe
from frappe.tests import IntegrationTestCase

from knowledge_hub.api.dashboard import summary


WORKSPACE_DOCTYPE = "Knowledge Hub Workspace"
NOTE_DOCTYPE = "Knowledge Hub Note"
TASK_DOCTYPE = "Knowledge Hub Task"


def create_test_user(email: str):
	if frappe.db.exists("User", email):
		return frappe.get_doc("User", email)

	user = frappe.get_doc(
		{
			"doctype": "User",
			"email": email,
			"first_name": "Dashboard",
			"last_name": "Tester",
			"enabled": 1,
		}
	)
	user.insert(ignore_permissions=True)

	return user


def reset_user_records(user):
	frappe.db.delete(TASK_DOCTYPE, {"owner": user.name})
	frappe.db.delete(NOTE_DOCTYPE, {"owner": user.name})
	frappe.db.delete(WORKSPACE_DOCTYPE, {"owner": user.name})


def create_workspace(title: str):
	doc = frappe.get_doc(
		{
			"doctype": WORKSPACE_DOCTYPE,
			"title": title,
			"description": "Dashboard workspace",
		}
	)
	doc.insert(ignore_permissions=True)
	return doc


def create_note(title: str, workspace: str):
	doc = frappe.get_doc(
		{
			"doctype": NOTE_DOCTYPE,
			"title": title,
			"content": "Dashboard note",
			"content_type": "Plain Text",
			"workspace": workspace,
		}
	)
	doc.insert(ignore_permissions=True)
	return doc


def create_task(title: str, workspace: str, completed: int = 0):
	doc = frappe.get_doc(
		{
			"doctype": TASK_DOCTYPE,
			"title": title,
			"description": "Dashboard task",
			"workspace": workspace,
			"status": "Done" if completed else "Open",
			"priority": "Medium",
			"completed": completed,
		}
	)
	doc.insert(ignore_permissions=True)
	return doc


class IntegrationTestDashboard(IntegrationTestCase):
	def test_summary_counts_current_user_records(self):
		user = create_test_user("dashboard.counts@example.com")
		reset_user_records(user)
		frappe.set_user(user.name)

		first_workspace = create_workspace("Dashboard First Workspace")
		second_workspace = create_workspace("Dashboard Second Workspace")

		create_note("Dashboard First Note", first_workspace.name)
		create_note("Dashboard Second Note", first_workspace.name)
		create_note("Dashboard Third Note", second_workspace.name)

		create_task("Dashboard Pending Task", first_workspace.name)
		create_task("Dashboard Done Task", second_workspace.name, completed=1)

		result = summary()

		self.assertEqual(result["workspace_count"], 2)
		self.assertEqual(result["note_count"], 3)
		self.assertEqual(result["pending_task_count"], 1)

	def test_summary_returns_recent_notes(self):
		user = create_test_user("dashboard.notes@example.com")
		reset_user_records(user)
		frappe.set_user(user.name)

		workspace = create_workspace("Dashboard Notes Workspace")
		note = create_note("Dashboard Recent Note", workspace.name)

		result = summary()
		recent_note_names = {item["name"] for item in result["recent_notes"]}

		self.assertIn(note.name, recent_note_names)
		self.assertEqual(result["recent_notes"][0]["route"], f"/notes/{note.name}")

	def test_summary_returns_only_pending_tasks(self):
		user = create_test_user("dashboard.tasks@example.com")
		reset_user_records(user)
		frappe.set_user(user.name)

		workspace = create_workspace("Dashboard Tasks Workspace")
		pending_task = create_task("Dashboard Pending Task", workspace.name)
		done_task = create_task("Dashboard Done Task", workspace.name, completed=1)

		result = summary()
		pending_task_names = {item["name"] for item in result["pending_tasks"]}

		self.assertIn(pending_task.name, pending_task_names)
		self.assertNotIn(done_task.name, pending_task_names)
		self.assertEqual(result["pending_tasks"][0]["route"], f"/tasks/{pending_task.name}")

	def test_summary_is_scoped_to_current_user(self):
		first_user = create_test_user("dashboard.owner.one@example.com")
		second_user = create_test_user("dashboard.owner.two@example.com")
		reset_user_records(first_user)
		reset_user_records(second_user)

		frappe.set_user(first_user.name)
		first_workspace = create_workspace("First User Workspace")
		create_note("First User Note", first_workspace.name)
		create_task("First User Task", first_workspace.name)

		frappe.set_user(second_user.name)
		second_workspace = create_workspace("Second User Workspace")

		result = summary()

		self.assertEqual(result["workspace_count"], 1)
		self.assertEqual(result["note_count"], 0)
		self.assertEqual(result["pending_task_count"], 0)
		self.assertEqual(result["recent_notes"], [])
		self.assertEqual(result["pending_tasks"], [])