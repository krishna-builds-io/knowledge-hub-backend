# Copyright (c) 2026, Krishna and Contributors
# See license.txt

import frappe
from frappe.tests import IntegrationTestCase
from knowledge_hub.api.taxonomy import create_category, create_tag

from knowledge_hub.api.note import (
	archive_note,
	create_note,
	delete_note,
	favorite_note,
	get_note,
	list_notes,
	update_note,
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
			"first_name": "Note",
			"last_name": "Tester",
			"enabled": 1,
		}
	)
	user.insert(ignore_permissions=True)

	return user

def create_workspace_for_current_user(title: str):
	doc = frappe.get_doc(
		{
			"doctype": "Knowledge Hub Workspace",
			"title": title,
			"description": "Created from note taxonomy API test",
		}
	)
	doc.insert(ignore_permissions=True)

	return doc


class IntegrationTestKnowledgeHubNote(IntegrationTestCase):
	def setUp(self):
		frappe.set_user("Administrator")
		self.workspace = create_workspace(title="TEST Note API Workspace")

	def test_create_note(self):
		note = create_note(
			title="TEST Note API Create",
			content="Created from API test",
			content_type="Plain Text",
			workspace=self.workspace["name"],
		)

		self.assertEqual(note["title"], "TEST Note API Create")
		self.assertEqual(note["content"], "Created from API test")
		self.assertEqual(note["workspace"], self.workspace["name"])
		self.assertEqual(note["favorite"], 0)
		self.assertEqual(note["archived"], 0)

	def test_create_note_requires_workspace(self):
		with self.assertRaises(frappe.ValidationError):
			create_note(title="TEST Note API Missing Workspace")

	def test_list_notes_returns_current_user_notes(self):
		note = create_note(
			title="TEST Note API List",
			workspace=self.workspace["name"],
		)

		notes = list_notes()
		note_names = [item["name"] for item in notes]

		self.assertIn(note["name"], note_names)

	def test_list_notes_filters_by_workspace(self):
		other_workspace = create_workspace(title="TEST Note API Other Workspace")
		matching_note = create_note(
			title="TEST Note API Matching Workspace",
			workspace=self.workspace["name"],
		)
		other_note = create_note(
			title="TEST Note API Other Workspace",
			workspace=other_workspace["name"],
		)

		notes = list_notes(workspace=self.workspace["name"])
		note_names = [item["name"] for item in notes]

		self.assertIn(matching_note["name"], note_names)
		self.assertNotIn(other_note["name"], note_names)

	def test_get_note(self):
		note = create_note(
			title="TEST Note API Get",
			workspace=self.workspace["name"],
		)

		result = get_note(note["name"])

		self.assertEqual(result["name"], note["name"])
		self.assertEqual(result["title"], "TEST Note API Get")

	def test_update_note(self):
		note = create_note(
			title="TEST Note API Update",
			workspace=self.workspace["name"],
		)

		result = update_note(
			name=note["name"],
			title="TEST Note API Updated",
			content="Updated from API test",
			content_type="Markdown",
			workspace=self.workspace["name"],
		)

		self.assertEqual(result["title"], "TEST Note API Updated")
		self.assertEqual(result["content"], "Updated from API test")
		self.assertEqual(result["content_type"], "Markdown")

	def test_archive_note(self):
		note = create_note(
			title="TEST Note API Archive",
			workspace=self.workspace["name"],
		)

		result = archive_note(name=note["name"], archived=1)

		self.assertEqual(result["name"], note["name"])
		self.assertEqual(result["archived"], 1)

	def test_favorite_note(self):
		note = create_note(
			title="TEST Note API Favorite",
			workspace=self.workspace["name"],
		)

		result = favorite_note(name=note["name"], favorite=1)

		self.assertEqual(result["name"], note["name"])
		self.assertEqual(result["favorite"], 1)

	def test_delete_note(self):
		note = create_note(
			title="TEST Note API Delete",
			workspace=self.workspace["name"],
		)

		result = delete_note(note["name"])

		self.assertEqual(result["name"], note["name"])
		self.assertTrue(result["deleted"])
		self.assertFalse(frappe.db.exists("Knowledge Hub Note", note["name"]))

	def test_get_note_blocks_other_user(self):
		note = create_note(
			title="TEST Note API Permission",
			workspace=self.workspace["name"],
		)
		other_user = create_test_user("note.api.tester@example.com")

		frappe.set_user(other_user.name)

		with self.assertRaises(frappe.PermissionError):
			get_note(note["name"])

	def test_create_note_blocks_other_users_workspace(self):
		other_user = create_test_user("note.workspace.tester@example.com")
		frappe.set_user(other_user.name)

		with self.assertRaises(frappe.PermissionError):
			create_note(
				title="TEST Note API Other Workspace",
				workspace=self.workspace["name"],
			)

	def test_create_note_with_category_and_tags(self):
		category = create_category(title="TEST Note API Category")
		first_tag = create_tag(title="TEST Note API First Tag")
		second_tag = create_tag(title="TEST Note API Second Tag")

		note = create_note(
			title="TEST Note API Taxonomy Create",
			workspace=self.workspace["name"],
			category=category["name"],
			tags=[first_tag["name"], second_tag["name"]],
		)

		self.assertEqual(note["category"], category["name"])
		self.assertEqual(note["tags"], [first_tag["name"], second_tag["name"]])

	def test_update_note_with_category_and_tags(self):
		first_category = create_category(title="TEST Note API Old Category")
		second_category = create_category(title="TEST Note API New Category")
		first_tag = create_tag(title="TEST Note API Old Tag")
		second_tag = create_tag(title="TEST Note API New Tag")

		note = create_note(
			title="TEST Note API Taxonomy Update",
			workspace=self.workspace["name"],
			category=first_category["name"],
			tags=[first_tag["name"]],
		)

		result = update_note(
			name=note["name"],
			title="TEST Note API Taxonomy Updated",
			workspace=self.workspace["name"],
			category=second_category["name"],
			tags=[second_tag["name"]],
		)

		self.assertEqual(result["category"], second_category["name"])
		self.assertEqual(result["tags"], [second_tag["name"]])

	def test_list_notes_filters_by_category(self):
		category = create_category(title="TEST Note API Filter Category")
		other_category = create_category(title="TEST Note API Other Category")

		matching_note = create_note(
			title="TEST Note API Matching Category",
			workspace=self.workspace["name"],
			category=category["name"],
		)
		other_note = create_note(
			title="TEST Note API Other Category",
			workspace=self.workspace["name"],
			category=other_category["name"],
		)

		notes = list_notes(category=category["name"])
		note_names = [item["name"] for item in notes]

		self.assertIn(matching_note["name"], note_names)
		self.assertNotIn(other_note["name"], note_names)

	def test_list_notes_filters_by_tag(self):
		tag = create_tag(title="TEST Note API Filter Tag")
		other_tag = create_tag(title="TEST Note API Other Tag")

		matching_note = create_note(
			title="TEST Note API Matching Tag",
			workspace=self.workspace["name"],
			tags=[tag["name"]],
		)
		other_note = create_note(
			title="TEST Note API Other Tag",
			workspace=self.workspace["name"],
			tags=[other_tag["name"]],
		)

		notes = list_notes(tag=tag["name"])
		note_names = [item["name"] for item in notes]

		self.assertIn(matching_note["name"], note_names)
		self.assertNotIn(other_note["name"], note_names)

	def test_create_note_blocks_other_users_category(self):
		category = create_category(title="TEST Note API Other User Category")
		other_user = create_test_user("note.category.tester@example.com")

		frappe.set_user(other_user.name)
		workspace = create_workspace_for_current_user(
			title="TEST Note API Other User Workspace",
		)

		with self.assertRaises(frappe.PermissionError):
			create_note(
				title="TEST Note API Block Category",
				workspace=workspace.name,
				category=category["name"],
			)

	def test_create_note_blocks_other_users_tag(self):
		tag = create_tag(title="TEST Note API Other User Tag")
		other_user = create_test_user("note.tag.tester@example.com")

		frappe.set_user(other_user.name)
		workspace = create_workspace_for_current_user(
			title="TEST Note API Other User Workspace",
		)

		with self.assertRaises(frappe.PermissionError):
			create_note(
				title="TEST Note API Block Tag",
				workspace=workspace.name,
				tags=[tag["name"]],
			)