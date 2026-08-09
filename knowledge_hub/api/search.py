import frappe

WORKSPACE_DOCTYPE = "Knowledge Hub Workspace"
NOTE_DOCTYPE = "Knowledge Hub Note"
TASK_DOCTYPE = "Knowledge Hub Task"

VALID_TYPES = {"all", "workspace", "note", "task"}


def _like_query(q: str):
	return f"%{q.strip()}%"


def _workspace_result(doc):
	return {
		"type": "workspace",
		"name": doc.name,
		"title": doc.title,
		"description": doc.description,
		"route": f"/workspaces/{doc.name}",
		"modified": doc.modified,
	}


def _note_result(doc):
	return {
		"type": "note",
		"name": doc.name,
		"title": doc.title,
		"description": doc.content,
		"route": f"/notes/{doc.name}",
		"modified": doc.modified,
	}


def _task_result(doc):
	return {
		"type": "task",
		"name": doc.name,
		"title": doc.title,
		"description": doc.description,
		"route": f"/tasks/{doc.name}",
		"modified": doc.modified,
	}


@frappe.whitelist(methods=["GET"])
def global_search(q: str = "", type: str = "all"):
	query = q.strip()
	search_type = type or "all"

	if search_type not in VALID_TYPES:
		frappe.throw("Invalid search type", frappe.ValidationError)

	if len(query) < 2:
		return []

	results = []
	like_query = _like_query(query)

	if search_type in {"all", "workspace"}:
		workspaces = frappe.get_all(
			WORKSPACE_DOCTYPE,
			filters=[
				["owner", "=", frappe.session.user],
				["title", "like", like_query],
			],
			fields=["name", "title", "description", "modified"],
			order_by="modified desc",
			limit=10,
		)
		results.extend(_workspace_result(doc) for doc in workspaces)

	if search_type in {"all", "note"}:
		notes = frappe.get_all(
			NOTE_DOCTYPE,
			filters=[
				["owner", "=", frappe.session.user],
				["title", "like", like_query],
			],
			fields=["name", "title", "content", "modified"],
			order_by="modified desc",
			limit=10,
		)
		results.extend(_note_result(doc) for doc in notes)

	if search_type in {"all", "task"}:
		tasks = frappe.get_all(
			TASK_DOCTYPE,
			filters=[
				["owner", "=", frappe.session.user],
				["title", "like", like_query],
			],
			fields=["name", "title", "description", "modified"],
			order_by="modified desc",
			limit=10,
		)
		results.extend(_task_result(doc) for doc in tasks)

	return sorted(results, key=lambda result: result["modified"], reverse=True)