import json

import frappe
from frappe import _


PREFERENCE_DOCTYPE = "Knowledge Hub User Preference"
ALLOWED_THEMES = {"System", "Light", "Dark"}


def _get_current_user():
	if frappe.session.user == "Guest":
		frappe.throw(_("Authentication required"), frappe.AuthenticationError)

	return frappe.session.user


def _parse_preferences(preferences_json):
	if not preferences_json:
		return {}

	try:
		return json.loads(preferences_json)
	except json.JSONDecodeError:
		return {}


def _serialize_preference(doc):
	return {
		"name": doc.name,
		"user": doc.user,
		"theme": doc.theme,
		"preferences": _parse_preferences(doc.preferences_json),
	}


def _get_or_create_preference(user):
	name = frappe.db.exists(PREFERENCE_DOCTYPE, {"user": user})

	if name:
		return frappe.get_doc(PREFERENCE_DOCTYPE, name)

	doc = frappe.get_doc(
		{
			"doctype": PREFERENCE_DOCTYPE,
			"user": user,
			"theme": "System",
			"preferences_json": "{}",
		}
	)
	doc.insert(ignore_permissions=True)

	return doc


@frappe.whitelist(methods=["GET"])
def get_preferences():
	user = _get_current_user()
	doc = _get_or_create_preference(user)

	return _serialize_preference(doc)


@frappe.whitelist(methods=["POST"])
def update_preferences(theme: str, preferences: dict | None = None):
	user = _get_current_user()

	if theme not in ALLOWED_THEMES:
		frappe.throw(_("Invalid theme"), frappe.ValidationError)

	doc = _get_or_create_preference(user)
	doc.theme = theme
	doc.preferences_json = json.dumps(preferences or {})
	doc.save(ignore_permissions=True)

	return _serialize_preference(doc)