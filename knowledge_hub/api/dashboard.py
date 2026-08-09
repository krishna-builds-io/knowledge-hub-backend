import frappe

WORKSPACE_DOCTYPE = "Knowledge Hub Workspace"
NOTE_DOCTYPE = "Knowledge Hub Note"
TASK_DOCTYPE = "Knowledge Hub Task"


def _recent_note_result(doc):
	return {
		"name": doc.name,
		"title": doc.title,
		"workspace": doc.workspace,
		"modified": doc.modified,
		"route": f"/notes/{doc.name}",
	}


def _pending_task_result(doc):
	return {
		"name": doc.name,
		"title": doc.title,
		"workspace": doc.workspace,
		"priority": doc.priority,
		"due_date": doc.due_date,
		"modified": doc.modified,
		"route": f"/tasks/{doc.name}",
	}


@frappe.whitelist(methods=["GET"])
def summary():
	user = frappe.session.user

	workspace_count = frappe.db.count(
		WORKSPACE_DOCTYPE,
		{"owner": user},
	)

	note_count = frappe.db.count(
		NOTE_DOCTYPE,
		{"owner": user},
	)

	pending_task_count = frappe.db.count(
		TASK_DOCTYPE,
		{
			"owner": user,
			"completed": 0,
		},
	)

	recent_notes = frappe.get_all(
		NOTE_DOCTYPE,
		filters={"owner": user},
		fields=["name", "title", "workspace", "modified"],
		order_by="modified desc",
		limit=5,
	)

	pending_tasks = frappe.get_all(
		TASK_DOCTYPE,
		filters={
			"owner": user,
			"completed": 0,
		},
		fields=["name", "title", "workspace", "priority", "due_date", "modified"],
		order_by="modified desc",
		limit=5,
	)

	return {
		"workspace_count": workspace_count,
		"note_count": note_count,
		"pending_task_count": pending_task_count,
		"recent_notes": [_recent_note_result(note) for note in recent_notes],
		"pending_tasks": [_pending_task_result(task) for task in pending_tasks],
	}