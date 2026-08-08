import frappe
from frappe import _


NOTE_DOCTYPE = "Knowledge Hub Note"
WORKSPACE_DOCTYPE = "Knowledge Hub Workspace"


def _serialize_note(doc):
	return {
		"name": doc.name,
		"title": doc.title,
		"content": doc.content,
		"content_type": doc.content_type,
		"workspace": doc.workspace,
		"favorite": doc.favorite,
		"archived": doc.archived,
		"creation": doc.creation,
		"modified": doc.modified,
	}


def _get_note_or_throw(name: str):
	doc = frappe.get_doc(NOTE_DOCTYPE, name)

	if doc.owner != frappe.session.user:
		frappe.throw(_("Not permitted"), frappe.PermissionError)

	return doc


def _validate_workspace_owner(workspace: str | None):
	if not workspace:
		return

	workspace_owner = frappe.db.get_value(WORKSPACE_DOCTYPE, workspace, "owner")

	if not workspace_owner:
		frappe.throw(_("Workspace not found"), frappe.DoesNotExistError)

	if workspace_owner != frappe.session.user:
		frappe.throw(_("Not permitted"), frappe.PermissionError)


@frappe.whitelist(methods=["GET"])
def list_notes(workspace: str | None = None):
	filters = {
		"owner": frappe.session.user,
	}

	if workspace:
		_validate_workspace_owner(workspace)
		filters["workspace"] = workspace

	return frappe.get_all(
		NOTE_DOCTYPE,
		filters=filters,
		fields=[
			"name",
			"title",
			"content_type",
			"content",
			"workspace",
			"favorite",
			"archived",
			"creation",
			"modified",
		],
		order_by="modified desc",
	)


@frappe.whitelist(methods=["GET"])
def get_note(name: str):
	doc = _get_note_or_throw(name)
	return _serialize_note(doc)


@frappe.whitelist(methods=["POST"])
def create_note(
	title: str,
	content: str | None = None,
	content_type: str = "Plain Text",
	workspace: str | None = None,
):
	_validate_workspace_owner(workspace)

	doc = frappe.get_doc({
		"doctype": NOTE_DOCTYPE,
		"title": title,
		"content": content,
		"content_type": content_type,
		"workspace": workspace,
	})
	doc.insert()

	return _serialize_note(doc)


@frappe.whitelist(methods=["POST"])
def update_note(
	name: str,
	title: str,
	content: str | None = None,
	content_type: str = "Plain Text",
	workspace: str | None = None,
):
	doc = _get_note_or_throw(name)
	_validate_workspace_owner(workspace)

	doc.title = title
	doc.content = content
	doc.content_type = content_type
	doc.workspace = workspace
	doc.save()

	return _serialize_note(doc)


@frappe.whitelist(methods=["POST"])
def archive_note(name: str, archived: int = 1):
	doc = _get_note_or_throw(name)

	doc.archived = archived
	doc.save()

	return {
		"name": doc.name,
		"archived": doc.archived,
	}


@frappe.whitelist(methods=["POST"])
def favorite_note(name: str, favorite: int = 1):
	doc = _get_note_or_throw(name)

	doc.favorite = favorite
	doc.save()

	return {
		"name": doc.name,
		"favorite": doc.favorite,
	}


@frappe.whitelist(methods=["POST"])
def delete_note(name: str):
	doc = _get_note_or_throw(name)
	doc.delete()

	return {
		"name": name,
		"deleted": True,
	}