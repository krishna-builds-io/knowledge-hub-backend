# Copyright (c) 2026, Krishna and Contributors
# See license.txt

import frappe
from frappe.tests import IntegrationTestCase

from knowledge_hub.api.task import (
	complete_task,
	create_task,
	delete_task,
	get_task,
	list_tasks,
	update_task,
)
from knowledge_hub.api.workspace import create_workspace


EXTRA_TEST_RECORD_DEPENDENCIES = []
IGNORE_TEST_RECORD_DEPENDENCIES = []


def create_test_user(email: str):
	if frappe.db.exists("User", email):
		return frappe.get_doc("User", email)

	user = frappe.get_doc(
		{
			"doctype": "User",
			"email": email,
			"first_name": "Task",
			"last_name": "Tester",
			"enabled": 1,
		}
	)
	user.insert(ignore_permissions=True)

	return user


class IntegrationTestKnowledgeHubTask(IntegrationTestCase):
	def setUp(self):
		frappe.set_user("Administrator")
		self.workspace = create_workspace(title="TEST Task API Workspace")

	def test_create_task(self):
		task = create_task(
			title="TEST Task API Create",
			description="Created from API test",
			workspace=self.workspace["name"],
			status="Open",
			priority="High",
			due_date="2026-08-31",
		)

		self.assertEqual(task["title"], "TEST Task API Create")
		self.assertEqual(task["description"], "Created from API test")
		self.assertEqual(task["workspace"], self.workspace["name"])
		self.assertEqual(task["status"], "Open")
		self.assertEqual(task["priority"], "High")
		self.assertEqual(str(task["due_date"]), "2026-08-31")
		self.assertEqual(task["completed"], 0)

	def test_create_done_task_sets_completed(self):
		task = create_task(
			title="TEST Task API Done",
			workspace=self.workspace["name"],
			status="Done",
			priority="Medium",
		)

		self.assertEqual(task["status"], "Done")
		self.assertEqual(task["completed"], 1)

	def test_create_task_requires_workspace(self):
		with self.assertRaises(frappe.ValidationError):
			create_task(
				title="TEST Task API Missing Workspace",
				workspace=None,
			)

	def test_create_task_rejects_invalid_status(self):
		with self.assertRaises(frappe.ValidationError):
			create_task(
				title="TEST Task API Invalid Status",
				workspace=self.workspace["name"],
				status="Invalid",
			)

	def test_create_task_rejects_invalid_priority(self):
		with self.assertRaises(frappe.ValidationError):
			create_task(
				title="TEST Task API Invalid Priority",
				workspace=self.workspace["name"],
				priority="Invalid",
			)

	def test_list_tasks_returns_current_user_tasks(self):
		task = create_task(
			title="TEST Task API List",
			workspace=self.workspace["name"],
		)

		tasks = list_tasks()
		task_names = [item["name"] for item in tasks]

		self.assertIn(task["name"], task_names)

	def test_list_tasks_filters_by_workspace(self):
		other_workspace = create_workspace(title="TEST Task API Other Workspace")
		matching_task = create_task(
			title="TEST Task API Matching Workspace",
			workspace=self.workspace["name"],
		)
		other_task = create_task(
			title="TEST Task API Other Workspace",
			workspace=other_workspace["name"],
		)

		tasks = list_tasks(workspace=self.workspace["name"])
		task_names = [item["name"] for item in tasks]

		self.assertIn(matching_task["name"], task_names)
		self.assertNotIn(other_task["name"], task_names)

	def test_get_task(self):
		task = create_task(
			title="TEST Task API Get",
			workspace=self.workspace["name"],
		)

		result = get_task(task["name"])

		self.assertEqual(result["name"], task["name"])
		self.assertEqual(result["title"], "TEST Task API Get")

	def test_update_task(self):
		task = create_task(
			title="TEST Task API Update",
			workspace=self.workspace["name"],
		)

		result = update_task(
			name=task["name"],
			title="TEST Task API Updated",
			description="Updated from API test",
			workspace=self.workspace["name"],
			status="In Progress",
			priority="Urgent",
			due_date="2026-09-15",
		)

		self.assertEqual(result["title"], "TEST Task API Updated")
		self.assertEqual(result["description"], "Updated from API test")
		self.assertEqual(result["status"], "In Progress")
		self.assertEqual(result["priority"], "Urgent")
		self.assertEqual(str(result["due_date"]), "2026-09-15")
		self.assertEqual(result["completed"], 0)

	def test_update_done_task_sets_completed(self):
		task = create_task(
			title="TEST Task API Update Done",
			workspace=self.workspace["name"],
		)

		result = update_task(
			name=task["name"],
			title="TEST Task API Update Done",
			workspace=self.workspace["name"],
			status="Done",
			priority="Medium",
		)

		self.assertEqual(result["status"], "Done")
		self.assertEqual(result["completed"], 1)

	def test_complete_task(self):
		task = create_task(
			title="TEST Task API Complete",
			workspace=self.workspace["name"],
		)

		result = complete_task(name=task["name"], completed=1)

		self.assertEqual(result["name"], task["name"])
		self.assertEqual(result["completed"], 1)
		self.assertEqual(result["status"], "Done")

	def test_reopen_task(self):
		task = create_task(
			title="TEST Task API Reopen",
			workspace=self.workspace["name"],
			status="Done",
		)

		result = complete_task(name=task["name"], completed=0)

		self.assertEqual(result["name"], task["name"])
		self.assertEqual(result["completed"], 0)
		self.assertEqual(result["status"], "Open")

	def test_delete_task(self):
		task = create_task(
			title="TEST Task API Delete",
			workspace=self.workspace["name"],
		)

		result = delete_task(task["name"])

		self.assertEqual(result["name"], task["name"])
		self.assertTrue(result["deleted"])
		self.assertFalse(frappe.db.exists("Knowledge Hub Task", task["name"]))

	def test_get_task_blocks_other_user(self):
		task = create_task(
			title="TEST Task API Permission",
			workspace=self.workspace["name"],
		)
		other_user = create_test_user("task.api.tester@example.com")

		frappe.set_user(other_user.name)

		with self.assertRaises(frappe.PermissionError):
			get_task(task["name"])

	def test_create_task_blocks_other_users_workspace(self):
		other_user = create_test_user("task.workspace.tester@example.com")
		frappe.set_user(other_user.name)

		with self.assertRaises(frappe.PermissionError):
			create_task(
				title="TEST Task API Other Workspace",
				workspace=self.workspace["name"],
			)