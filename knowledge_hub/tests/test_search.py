import frappe
from frappe.tests import IntegrationTestCase

from knowledge_hub.api.search import global_search


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
			"first_name": "Search",
			"last_name": "Tester",
			"enabled": 1,
		}
	)
	user.insert(ignore_permissions=True)

	return user


def create_workspace(title: str):
	doc = frappe.get_doc(
		{
			"doctype": WORKSPACE_DOCTYPE,
			"title": title,
			"description": "Search workspace description",
		}
	)
	doc.insert(ignore_permissions=True)
	return doc


def create_note(title: str, workspace: str):
	doc = frappe.get_doc(
		{
			"doctype": NOTE_DOCTYPE,
			"title": title,
			"content": "Search note content",
			"content_type": "Plain Text",
			"workspace": workspace,
		}
	)
	doc.insert(ignore_permissions=True)
	return doc


def create_task(title: str, workspace: str):
	doc = frappe.get_doc(
		{
			"doctype": TASK_DOCTYPE,
			"title": title,
			"description": "Search task description",
			"workspace": workspace,
			"status": "Open",
			"priority": "Medium",
			"completed": 0,
		}
	)
	doc.insert(ignore_permissions=True)
	return doc


class IntegrationTestSearch(IntegrationTestCase):
	def test_global_search_returns_all_matching_types(self):
		user = create_test_user("search.all@example.com")
		frappe.set_user(user.name)

		workspace = create_workspace("Alpha Search Workspace")
		note = create_note("Alpha Search Note", workspace.name)
		task = create_task("Alpha Search Task", workspace.name)

		results = global_search(q="Alpha", type="all")
		result_names = {result["name"] for result in results}
		result_types = {result["type"] for result in results}

		self.assertIn(workspace.name, result_names)
		self.assertIn(note.name, result_names)
		self.assertIn(task.name, result_names)
		self.assertEqual(result_types, {"workspace", "note", "task"})

	def test_global_search_filters_by_workspace_type(self):
		user = create_test_user("search.workspace@example.com")
		frappe.set_user(user.name)

		workspace = create_workspace("Bravo Search Workspace")
		create_note("Bravo Search Note", workspace.name)
		create_task("Bravo Search Task", workspace.name)

		results = global_search(q="Bravo", type="workspace")

		self.assertEqual(len(results), 1)
		self.assertEqual(results[0]["type"], "workspace")
		self.assertEqual(results[0]["name"], workspace.name)

	def test_global_search_filters_by_note_type(self):
		user = create_test_user("search.note@example.com")
		frappe.set_user(user.name)

		workspace = create_workspace("Charlie Search Workspace")
		note = create_note("Charlie Search Note", workspace.name)
		create_task("Charlie Search Task", workspace.name)

		results = global_search(q="Charlie", type="note")

		self.assertEqual(len(results), 1)
		self.assertEqual(results[0]["type"], "note")
		self.assertEqual(results[0]["name"], note.name)

	def test_global_search_filters_by_task_type(self):
		user = create_test_user("search.task@example.com")
		frappe.set_user(user.name)

		workspace = create_workspace("Delta Search Workspace")
		create_note("Delta Search Note", workspace.name)
		task = create_task("Delta Search Task", workspace.name)

		results = global_search(q="Delta", type="task")

		self.assertEqual(len(results), 1)
		self.assertEqual(results[0]["type"], "task")
		self.assertEqual(results[0]["name"], task.name)

	def test_global_search_requires_two_characters(self):
		user = create_test_user("search.short@example.com")
		frappe.set_user(user.name)

		create_workspace("Echo Search Workspace")

		self.assertEqual(global_search(q="E", type="all"), [])

	def test_global_search_rejects_invalid_type(self):
		user = create_test_user("search.invalid@example.com")
		frappe.set_user(user.name)

		with self.assertRaises(frappe.ValidationError):
			global_search(q="Alpha", type="invalid")

	def test_global_search_is_scoped_to_current_user(self):
		first_user = create_test_user("search.owner.one@example.com")
		second_user = create_test_user("search.owner.two@example.com")

		frappe.set_user(first_user.name)
		visible_workspace = create_workspace("Foxtrot Search Workspace")

		frappe.set_user(second_user.name)
		hidden_workspace = create_workspace("Foxtrot Search Workspace")

		results = global_search(q="Foxtrot", type="workspace")
		result_names = {result["name"] for result in results}

		self.assertIn(hidden_workspace.name, result_names)
		self.assertNotIn(visible_workspace.name, result_names)