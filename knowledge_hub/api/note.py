import frappe
from frappe import _


NOTE_DOCTYPE = "Knowledge Hub Note"
WORKSPACE_DOCTYPE = "Knowledge Hub Workspace"
CATEGORY_DOCTYPE = "Knowledge Hub Category"
TAG_DOCTYPE = "Knowledge Hub Tag"
NOTE_TAG_DOCTYPE = "Knowledge Hub Note Tag"


def _serialize_note(doc):
	return {
		"name": doc.name,
		"title": doc.title,
		"content": doc.content,
		"content_type": doc.content_type,
		"workspace": doc.workspace,
		"category": doc.category,
		"tags": _get_note_tag_names(doc.name),
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
		frappe.throw(_("Workspace is required"), frappe.ValidationError)

	workspace_owner = frappe.db.get_value(WORKSPACE_DOCTYPE, workspace, "owner")

	if not workspace_owner:
		frappe.throw(_("Workspace not found"), frappe.DoesNotExistError)

	if workspace_owner != frappe.session.user:
		frappe.throw(_("Not permitted"), frappe.PermissionError)

def _get_note_tag_names(note: str):
	rows = frappe.get_all(
		NOTE_TAG_DOCTYPE,
		filters={"parent": note},
		fields=["tag"],
		order_by="idx asc",
	)

	return [row.tag for row in rows]


def _normalize_tags(tags: list[str] | str | None):
	if not tags:
		return []

	if isinstance(tags, str):
		tags = frappe.parse_json(tags)

		if isinstance(tags, str):
			tags = [tags]

	unique_tags = []

	for tag in tags:
		if tag and tag not in unique_tags:
			unique_tags.append(tag)

	return unique_tags


def _validate_category_owner(category: str | None):
	if not category:
		return

	category_owner = frappe.db.get_value(CATEGORY_DOCTYPE, category, "owner")

	if not category_owner:
		frappe.throw(_("Category not found"), frappe.DoesNotExistError)

	if category_owner != frappe.session.user:
		frappe.throw(_("Not permitted"), frappe.PermissionError)


def _validate_tag_owners(tags: list[str] | None):
	for tag in _normalize_tags(tags):
		tag_owner = frappe.db.get_value(TAG_DOCTYPE, tag, "owner")

		if not tag_owner:
			frappe.throw(_("Tag not found"), frappe.DoesNotExistError)

		if tag_owner != frappe.session.user:
			frappe.throw(_("Not permitted"), frappe.PermissionError)


def _set_note_tags(doc, tags: list[str] | None):
	doc.set("tags", [])

	for tag in _normalize_tags(tags):
		doc.append("tags", {"tag": tag})

@frappe.whitelist(methods=["GET"])
def list_notes(
	workspace: str | None = None,
	category: str | None = None,
	tag: str | None = None,
):
	filters = {
		"owner": frappe.session.user,
	}

	if workspace:
		_validate_workspace_owner(workspace)
		filters["workspace"] = workspace

	if category:
		_validate_category_owner(category)
		filters["category"] = category

	if tag:
		_validate_tag_owners([tag])
		note_names = [
			row.parent
			for row in frappe.get_all(
				NOTE_TAG_DOCTYPE,
				filters={"tag": tag},
				fields=["parent"],
			)
		]

		if not note_names:
			return []

		filters["name"] = ["in", note_names]
	return frappe.get_all(
		NOTE_DOCTYPE,
		filters=filters,
		fields=[
			"name",
			"title",
			"content_type",
			"content",
			"workspace",
			"category",
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
	category: str | None = None,
	tags: list[str] | str | None = None,
):
	_validate_workspace_owner(workspace)
	_validate_category_owner(category)
	_validate_tag_owners(tags)

	doc = frappe.get_doc({
		"doctype": NOTE_DOCTYPE,
		"title": title,
		"content": content,
		"content_type": content_type,
		"workspace": workspace,
		"category": category,
	})

	_set_note_tags(doc, tags)
	doc.insert()

	return _serialize_note(doc)


@frappe.whitelist(methods=["POST"])
def update_note(
	name: str,
	title: str,
	content: str | None = None,
	content_type: str = "Plain Text",
	workspace: str | None = None,
	category: str | None = None,
	tags: list[str] | str | None = None,
):
	doc = _get_note_or_throw(name)
	_validate_workspace_owner(workspace)
	_validate_category_owner(category)
	_validate_tag_owners(tags)

	doc.title = title
	doc.content = content
	doc.content_type = content_type
	doc.workspace = workspace
	doc.category = category
	_set_note_tags(doc, tags)
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
