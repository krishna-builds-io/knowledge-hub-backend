# Copyright (c) 2026, Krishna and Contributors
# See license.txt

import frappe
from frappe.tests import IntegrationTestCase

from knowledge_hub.api.workspace import (
	archive_workspace,
	create_workspace,
	delete_workspace,
	get_workspace,
	list_workspaces,
	update_workspace,
)

EXTRA_TEST_RECORD_DEPENDENCIES = []
IGNORE_TEST_RECORD_DEPENDENCIES = []

def create_test_user(email: str):
	if frappe.db.exists("User", email):
		return frappe.get_doc("User", email)

	user = frappe.get_doc(
		{
			"doctype": "User",
			"email": email,
			"first_name": "Workspace",
			"last_name": "Tester",
			"enabled": 1,
		}
	)
	user.insert(ignore_permissions=True)

	return user

class IntegrationTestKnowledgeHubWorkspace(IntegrationTestCase):
	def setUp(self):
		frappe.set_user("Administrator")

	def test_create_workspace(self):
		workspace = create_workspace(
			title="TEST Workspace API Create",
			description="Created from API test",
		)

		self.assertEqual(workspace["title"], "TEST Workspace API Create")
		self.assertEqual(workspace["description"], "Created from API test")
		self.assertEqual(workspace["archived"], 0)

	def test_list_workspaces_returns_current_user_workspaces(self):
		workspace = create_workspace(title="TEST Workspace API List")

		workspaces = list_workspaces()
		workspace_names = [item["name"] for item in workspaces]

		self.assertIn(workspace["name"], workspace_names)

	def test_get_workspace(self):
		workspace = create_workspace(title="TEST Workspace API Get")

		result = get_workspace(workspace["name"])

		self.assertEqual(result["name"], workspace["name"])
		self.assertEqual(result["title"], "TEST Workspace API Get")

	def test_update_workspace(self):
		workspace = create_workspace(title="TEST Workspace API Update")

		result = update_workspace(
			name=workspace["name"],
			title="TEST Workspace API Updated",
			description="Updated from API test",
		)

		self.assertEqual(result["title"], "TEST Workspace API Updated")
		self.assertEqual(result["description"], "Updated from API test")

	def test_archive_workspace(self):
		workspace = create_workspace(title="TEST Workspace API Archive")

		result = archive_workspace(name=workspace["name"], archived=1)

		self.assertEqual(result["name"], workspace["name"])
		self.assertEqual(result["archived"], 1)

	def test_delete_workspace(self):
		workspace = create_workspace(title="TEST Workspace API Delete")

		result = delete_workspace(workspace["name"])

		self.assertEqual(result["name"], workspace["name"])
		self.assertTrue(result["deleted"])
		self.assertFalse(frappe.db.exists("Knowledge Hub Workspace", workspace["name"]))

	def test_get_workspace_blocks_other_user(self):
		workspace = create_workspace(title="TEST Workspace API Permission")
		other_user = create_test_user("workspace.api.tester@example.com")

		frappe.set_user(other_user.name)

		with self.assertRaises(frappe.PermissionError):
			get_workspace(workspace["name"])