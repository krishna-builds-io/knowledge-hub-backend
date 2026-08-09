import frappe
from frappe.tests import IntegrationTestCase

from knowledge_hub.api.taxonomy import (
	archive_category,
	archive_tag,
	create_category,
	create_tag,
	delete_category,
	delete_tag,
	list_categories,
	list_tags,
	update_category,
	update_tag,
)


CATEGORY_DOCTYPE = "Knowledge Hub Category"
TAG_DOCTYPE = "Knowledge Hub Tag"
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
			"first_name": "Taxonomy",
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
			"description": "Taxonomy workspace",
		}
	)
	doc.insert(ignore_permissions=True)
	return doc


def create_note(title: str, workspace: str, category: str | None = None):
	doc = frappe.get_doc(
		{
			"doctype": NOTE_DOCTYPE,
			"title": title,
			"content": "Taxonomy note",
			"content_type": "Plain Text",
			"workspace": workspace,
			"category": category,
		}
	)
	doc.insert(ignore_permissions=True)
	return doc


def create_task(title: str, workspace: str, category: str | None = None):
	doc = frappe.get_doc(
		{
			"doctype": TASK_DOCTYPE,
			"title": title,
			"description": "Taxonomy task",
			"workspace": workspace,
			"category": category,
			"status": "Open",
			"priority": "Medium",
			"completed": 0,
		}
	)
	doc.insert(ignore_permissions=True)
	return doc


class IntegrationTestTaxonomy(IntegrationTestCase):
	def setUp(self):
		frappe.set_user("Administrator")

	def test_create_category(self):
		category = create_category(
			title="TEST Taxonomy Category Create",
			description="Created from API test",
			color="#2563eb",
		)

		self.assertEqual(category["title"], "TEST Taxonomy Category Create")
		self.assertEqual(category["description"], "Created from API test")
		self.assertEqual(category["color"], "#2563eb")
		self.assertEqual(category["archived"], 0)

	def test_create_category_requires_title(self):
		with self.assertRaises(frappe.ValidationError):
			create_category(title="   ")

	def test_list_categories_returns_current_user_categories(self):
		category = create_category(title="TEST Taxonomy Category List")
		categories = list_categories()

		category_names = {item["name"] for item in categories}

		self.assertIn(category["name"], category_names)

	def test_list_categories_hides_archived_by_default(self):
		category = create_category(title="TEST Taxonomy Category Archived")
		archive_category(category["name"], archived=1)

		active_categories = list_categories()
		all_categories = list_categories(include_archived=1)

		active_names = {item["name"] for item in active_categories}
		all_names = {item["name"] for item in all_categories}

		self.assertNotIn(category["name"], active_names)
		self.assertIn(category["name"], all_names)

	def test_update_category(self):
		category = create_category(title="TEST Taxonomy Category Update")

		updated_category = update_category(
			name=category["name"],
			title="TEST Taxonomy Category Updated",
			description="Updated from API test",
			color="#16a34a",
		)

		self.assertEqual(updated_category["title"], "TEST Taxonomy Category Updated")
		self.assertEqual(updated_category["description"], "Updated from API test")
		self.assertEqual(updated_category["color"], "#16a34a")

	def test_archive_category(self):
		category = create_category(title="TEST Taxonomy Category Archive")

		result = archive_category(name=category["name"], archived=1)

		self.assertEqual(result["name"], category["name"])
		self.assertEqual(result["archived"], 1)

	def test_delete_category(self):
		category = create_category(title="TEST Taxonomy Category Delete")

		result = delete_category(category["name"])

		self.assertEqual(result["name"], category["name"])
		self.assertTrue(result["deleted"])
		self.assertFalse(frappe.db.exists(CATEGORY_DOCTYPE, category["name"]))

	def test_delete_category_blocks_linked_notes(self):
		category = create_category(title="TEST Taxonomy Category Linked Note")
		workspace = create_workspace("TEST Taxonomy Category Note Workspace")
		create_note(
			title="TEST Taxonomy Category Linked Note",
			workspace=workspace.name,
			category=category["name"],
		)

		with self.assertRaises(frappe.ValidationError):
			delete_category(category["name"])

	def test_delete_category_blocks_linked_tasks(self):
		category = create_category(title="TEST Taxonomy Category Linked Task")
		workspace = create_workspace("TEST Taxonomy Category Task Workspace")
		create_task(
			title="TEST Taxonomy Category Linked Task",
			workspace=workspace.name,
			category=category["name"],
		)

		with self.assertRaises(frappe.ValidationError):
			delete_category(category["name"])

	def test_update_category_blocks_other_user(self):
		category = create_category(title="TEST Taxonomy Category Permission")
		other_user = create_test_user("taxonomy.category.permission@example.com")

		frappe.set_user(other_user.name)

		with self.assertRaises(frappe.PermissionError):
			update_category(
				name=category["name"],
				title="Not Allowed",
			)

	def test_create_tag(self):
		tag = create_tag(
			title="TEST Taxonomy Tag Create",
			color="#9333ea",
		)

		self.assertEqual(tag["title"], "TEST Taxonomy Tag Create")
		self.assertEqual(tag["color"], "#9333ea")
		self.assertEqual(tag["archived"], 0)

	def test_create_tag_requires_title(self):
		with self.assertRaises(frappe.ValidationError):
			create_tag(title="   ")

	def test_list_tags_returns_current_user_tags(self):
		tag = create_tag(title="TEST Taxonomy Tag List")
		tags = list_tags()

		tag_names = {item["name"] for item in tags}

		self.assertIn(tag["name"], tag_names)

	def test_list_tags_hides_archived_by_default(self):
		tag = create_tag(title="TEST Taxonomy Tag Archived")
		archive_tag(tag["name"], archived=1)

		active_tags = list_tags()
		all_tags = list_tags(include_archived=1)

		active_names = {item["name"] for item in active_tags}
		all_names = {item["name"] for item in all_tags}

		self.assertNotIn(tag["name"], active_names)
		self.assertIn(tag["name"], all_names)

	def test_update_tag(self):
		tag = create_tag(title="TEST Taxonomy Tag Update")

		updated_tag = update_tag(
			name=tag["name"],
			title="TEST Taxonomy Tag Updated",
			color="#f97316",
		)

		self.assertEqual(updated_tag["title"], "TEST Taxonomy Tag Updated")
		self.assertEqual(updated_tag["color"], "#f97316")

	def test_archive_tag(self):
		tag = create_tag(title="TEST Taxonomy Tag Archive")

		result = archive_tag(name=tag["name"], archived=1)

		self.assertEqual(result["name"], tag["name"])
		self.assertEqual(result["archived"], 1)

	def test_delete_tag(self):
		tag = create_tag(title="TEST Taxonomy Tag Delete")

		result = delete_tag(tag["name"])

		self.assertEqual(result["name"], tag["name"])
		self.assertTrue(result["deleted"])
		self.assertFalse(frappe.db.exists(TAG_DOCTYPE, tag["name"]))

	def test_delete_tag_blocks_linked_notes(self):
		tag = create_tag(title="TEST Taxonomy Tag Linked Note")
		workspace = create_workspace("TEST Taxonomy Tag Note Workspace")
		note = create_note(
			title="TEST Taxonomy Tag Linked Note",
			workspace=workspace.name,
		)

		note_doc = frappe.get_doc(NOTE_DOCTYPE, note.name)
		note_doc.append("tags", {"tag": tag["name"]})
		note_doc.save(ignore_permissions=True)

		with self.assertRaises(frappe.ValidationError):
			delete_tag(tag["name"])

	def test_delete_tag_blocks_linked_tasks(self):
		tag = create_tag(title="TEST Taxonomy Tag Linked Task")
		workspace = create_workspace("TEST Taxonomy Tag Task Workspace")
		task = create_task(
			title="TEST Taxonomy Tag Linked Task",
			workspace=workspace.name,
		)

		task_doc = frappe.get_doc(TASK_DOCTYPE, task.name)
		task_doc.append("tags", {"tag": tag["name"]})
		task_doc.save(ignore_permissions=True)

		with self.assertRaises(frappe.ValidationError):
			delete_tag(tag["name"])

	def test_update_tag_blocks_other_user(self):
		tag = create_tag(title="TEST Taxonomy Tag Permission")
		other_user = create_test_user("taxonomy.tag.permission@example.com")

		frappe.set_user(other_user.name)

		with self.assertRaises(frappe.PermissionError):
			update_tag(
				name=tag["name"],
				title="Not Allowed",
			)