import frappe
from frappe import _

TASK_DOCTYPE = "Knowledge Hub Task"
WORKSPACE_DOCTYPE = "Knowledge Hub Workspace"

VALID_STATUSES = {"Open", "In Progress", "Done", "Blocked"}
VALID_PRIORITIES = {"Low", "Medium", "High", "Urgent"}


def _serialize_task(doc):
	return {
		"name": doc.name,
		"title": doc.title,
		"description": doc.description,
		"workspace": doc.workspace,
		"status": doc.status,
		"priority": doc.priority,
		"due_date": doc.due_date,
		"completed": doc.completed,
		"creation": doc.creation,
		"modified": doc.modified,
	}


def _get_task_or_throw(name: str):
	doc = frappe.get_doc(TASK_DOCTYPE, name)

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


def _validate_task_options(status: str, priority: str):
	if status not in VALID_STATUSES:
		frappe.throw(_("Invalid status"), frappe.ValidationError)

	if priority not in VALID_PRIORITIES:
		frappe.throw(_("Invalid priority"), frappe.ValidationError)



@frappe.whitelist(methods=["GET"])
def list_tasks(workspace: str | None = None):
	filters = {"owner": frappe.session.user}

	if workspace:
		_validate_workspace_owner(workspace)
		filters["workspace"] = workspace

	return frappe.get_all(
		TASK_DOCTYPE,
		filters=filters,
		fields=["name", "title", "description", "workspace", "status", "priority", "due_date", "completed", "creation", "modified"],
		order_by="modified desc",
	)


@frappe.whitelist(methods=["GET"])
def get_task(name: str):
	return _serialize_task(_get_task_or_throw(name))


@frappe.whitelist(methods=["POST"])
def create_task(title: str, workspace: str, description: str | None = None, status: str = "Open", priority: str = "Medium", due_date: str | None = None):
	_validate_workspace_owner(workspace)
	_validate_task_options(status, priority)

	doc = frappe.get_doc({
		"doctype": TASK_DOCTYPE,
		"title": title,
		"description": description,
		"workspace": workspace,
		"status": status,
		"priority": priority,
		"due_date": due_date,
		"completed": 1 if status == "Done" else 0,
	})
	doc.insert()

	return _serialize_task(doc)


@frappe.whitelist(methods=["POST"])
def update_task(name: str, title: str, workspace: str, description: str | None = None, status: str = "Open", priority: str = "Medium", due_date: str | None = None):
	doc = _get_task_or_throw(name)
	_validate_workspace_owner(workspace)
	_validate_task_options(status, priority)

	doc.title = title
	doc.description = description
	doc.workspace = workspace
	doc.status = status
	doc.priority = priority
	doc.due_date = due_date
	doc.completed = 1 if status == "Done" else 0
	doc.save()

	return _serialize_task(doc)


@frappe.whitelist(methods=["POST"])
def complete_task(name: str, completed: int = 1):
	doc = _get_task_or_throw(name)

	doc.completed = completed
	doc.status = "Done" if completed else "Open"
	doc.save()

	return {"name": doc.name, "completed": doc.completed, "status": doc.status}


@frappe.whitelist(methods=["POST"])
def delete_task(name: str):
	doc = _get_task_or_throw(name)
	doc.delete()

	return {"name": name, "deleted": True}