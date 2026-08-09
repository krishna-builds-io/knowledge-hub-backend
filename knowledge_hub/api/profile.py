import frappe
from frappe import _
from frappe.utils.password import check_password, update_password
from frappe.exceptions import AuthenticationError


def _serialize_user(user):
	return {
		"name": user.name,
		"email": user.email,
		"full_name": user.full_name,
		"first_name": user.first_name,
		"last_name": user.last_name,
	}


def _get_current_user_doc():
	if frappe.session.user == "Guest":
		frappe.throw(_("Authentication required"), frappe.AuthenticationError)

	return frappe.get_doc("User", frappe.session.user)


@frappe.whitelist(methods=["GET"])
def get_profile():
	user = _get_current_user_doc()
	return _serialize_user(user)


@frappe.whitelist(methods=["POST"])
def update_profile(first_name: str, last_name: str | None = None):
	user = _get_current_user_doc()

	user.first_name = first_name
	user.last_name = last_name
	user.save(ignore_permissions=True)

	return _serialize_user(user)


@frappe.whitelist(methods=["POST"])
def change_password(old_password: str, new_password: str):
	user = _get_current_user_doc()

	if len(new_password) < 8:
		frappe.throw(_("New password must be at least 8 characters"), frappe.ValidationError)
	try:
		check_password(user.name, old_password)
	except AuthenticationError:
		frappe.throw(_("Current password is incorrect"), frappe.ValidationError)

	update_password(user.name, new_password, logout_all_sessions=False)

	return {
		"changed": True,
	}