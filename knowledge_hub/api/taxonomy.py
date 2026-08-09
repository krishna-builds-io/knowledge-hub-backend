import frappe
from frappe import _


CATEGORY_DOCTYPE = "Knowledge Hub Category"
TAG_DOCTYPE = "Knowledge Hub Tag"
NOTE_DOCTYPE = "Knowledge Hub Note"
TASK_DOCTYPE = "Knowledge Hub Task"
NOTE_TAG_DOCTYPE = "Knowledge Hub Note Tag"
TASK_TAG_DOCTYPE = "Knowledge Hub Task Tag"


def _clean_title(title: str):
	cleaned_title = title.strip()

	if not cleaned_title:
		frappe.throw(_("Title is required"), frappe.ValidationError)

	return cleaned_title


def _get_owned_doc_or_throw(doctype: str, name: str):
	doc = frappe.get_doc(doctype, name)

	if doc.owner != frappe.session.user:
		frappe.throw(_("Not permitted"), frappe.PermissionError)

	return doc


def _serialize_category(doc):
	return {
		"name": doc.name,
		"title": doc.title,
		"description": doc.description,
		"color": doc.color,
		"archived": doc.archived,
		"creation": doc.creation,
		"modified": doc.modified,
	}


def _serialize_tag(doc):
	return {
		"name": doc.name,
		"title": doc.title,
		"color": doc.color,
		"archived": doc.archived,
		"creation": doc.creation,
		"modified": doc.modified,
	}


@frappe.whitelist(methods=["GET"])
def list_categories(include_archived: int = 0):
	filters = {
		"owner": frappe.session.user,
	}

	if not include_archived:
		filters["archived"] = 0

	return frappe.get_all(
		CATEGORY_DOCTYPE,
		filters=filters,
		fields=[
			"name",
			"title",
			"description",
			"color",
			"archived",
			"creation",
			"modified",
		],
		order_by="modified desc",
	)


@frappe.whitelist(methods=["POST"])
def create_category(
	title: str,
	description: str | None = None,
	color: str | None = None,
):
	doc = frappe.get_doc(
		{
			"doctype": CATEGORY_DOCTYPE,
			"title": _clean_title(title),
			"description": description,
			"color": color,
		}
	)
	doc.insert()

	return _serialize_category(doc)


@frappe.whitelist(methods=["POST"])
def update_category(
	name: str,
	title: str,
	description: str | None = None,
	color: str | None = None,
):
	doc = _get_owned_doc_or_throw(CATEGORY_DOCTYPE, name)

	doc.title = _clean_title(title)
	doc.description = description
	doc.color = color
	doc.save()

	return _serialize_category(doc)


@frappe.whitelist(methods=["POST"])
def archive_category(name: str, archived: int = 1):
	doc = _get_owned_doc_or_throw(CATEGORY_DOCTYPE, name)

	doc.archived = archived
	doc.save()

	return {
		"name": doc.name,
		"archived": doc.archived,
	}


@frappe.whitelist(methods=["POST"])
def delete_category(name: str):
	doc = _get_owned_doc_or_throw(CATEGORY_DOCTYPE, name)

	note_count = frappe.db.count(NOTE_DOCTYPE, {"category": name})
	task_count = frappe.db.count(TASK_DOCTYPE, {"category": name})

	if note_count or task_count:
		frappe.throw(
			_("This category is used by notes or tasks. Archive it instead, or remove it from linked records first."),
			frappe.ValidationError,
		)

	doc.delete()

	return {
		"name": name,
		"deleted": True,
	}


@frappe.whitelist(methods=["GET"])
def list_tags(include_archived: int = 0):
	filters = {
		"owner": frappe.session.user,
	}

	if not include_archived:
		filters["archived"] = 0

	return frappe.get_all(
		TAG_DOCTYPE,
		filters=filters,
		fields=[
			"name",
			"title",
			"color",
			"archived",
			"creation",
			"modified",
		],
		order_by="modified desc",
	)


@frappe.whitelist(methods=["POST"])
def create_tag(
	title: str,
	color: str | None = None,
):
	doc = frappe.get_doc(
		{
			"doctype": TAG_DOCTYPE,
			"title": _clean_title(title),
			"color": color,
		}
	)
	doc.insert()

	return _serialize_tag(doc)


@frappe.whitelist(methods=["POST"])
def update_tag(
	name: str,
	title: str,
	color: str | None = None,
):
	doc = _get_owned_doc_or_throw(TAG_DOCTYPE, name)

	doc.title = _clean_title(title)
	doc.color = color
	doc.save()

	return _serialize_tag(doc)


@frappe.whitelist(methods=["POST"])
def archive_tag(name: str, archived: int = 1):
	doc = _get_owned_doc_or_throw(TAG_DOCTYPE, name)

	doc.archived = archived
	doc.save()

	return {
		"name": doc.name,
		"archived": doc.archived,
	}


@frappe.whitelist(methods=["POST"])
def delete_tag(name: str):
	doc = _get_owned_doc_or_throw(TAG_DOCTYPE, name)

	note_tag_count = frappe.db.count(NOTE_TAG_DOCTYPE, {"tag": name})
	task_tag_count = frappe.db.count(TASK_TAG_DOCTYPE, {"tag": name})

	if note_tag_count or task_tag_count:
		frappe.throw(
			_("This tag is used by notes or tasks. Archive it instead, or remove it from linked records first."),
			frappe.ValidationError,
		)

	doc.delete()

	return {
		"name": name,
		"deleted": True,
	}