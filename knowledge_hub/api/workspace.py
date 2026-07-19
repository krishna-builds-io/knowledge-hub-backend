import frappe
from frappe import _


DOCTYPE = "Knowledge Hub Workspace"


def _get_workspace_or_throw(name: str):
    doc = frappe.get_doc(DOCTYPE, name)

    if doc.owner != frappe.session.user:
        frappe.throw(_("Not permitted"), frappe.PermissionError)

    return doc


@frappe.whitelist()
def list_workspaces():
    return frappe.get_all(
        DOCTYPE,
        filters={
            "owner": frappe.session.user,
        },
        fields=[
            "name",
            "title",
            "description",
            "archived",
            "creation",
            "modified",
        ],
        order_by="modified desc",
    )


@frappe.whitelist()
def get_workspace(name: str):
    doc = _get_workspace_or_throw(name)

    return {
        "name": doc.name,
        "title": doc.title,
        "description": doc.description,
        "archived": doc.archived,
        "creation": doc.creation,
        "modified": doc.modified,
    }


@frappe.whitelist()
def create_workspace(title: str, description: str | None = None):
    doc = frappe.get_doc({
        "doctype": DOCTYPE,
        "title": title,
        "description": description,
    })
    doc.insert()

    return {
        "name": doc.name,
        "title": doc.title,
        "description": doc.description,
        "archived": doc.archived,
        "creation": doc.creation,
        "modified": doc.modified,
    }


@frappe.whitelist()
def update_workspace(name: str, title: str, description: str | None = None):
    doc = _get_workspace_or_throw(name)

    doc.title = title
    doc.description = description
    doc.save()

    return {
        "name": doc.name,
        "title": doc.title,
        "description": doc.description,
        "archived": doc.archived,
        "creation": doc.creation,
        "modified": doc.modified,
    }


@frappe.whitelist()
def delete_workspace(name: str):
    doc = _get_workspace_or_throw(name)
    doc.delete()

    return {
        "name": name,
        "deleted": True,
    }


@frappe.whitelist()
def archive_workspace(name: str, archived: int = 1):
    doc = _get_workspace_or_throw(name)

    doc.archived = archived
    doc.save()

    return {
        "name": doc.name,
        "archived": doc.archived,
    }