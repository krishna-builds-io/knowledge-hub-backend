import frappe
from frappe import _

@frappe.whitelist()
def current_user():
    if frappe.session.user == "Guest":
        frappe.throw(_("Authentication required"), frappe.AuthenticationError)
    
    user = frappe.get_doc("User", frappe.session.user)

    return {
        "name": user.name,
        "email": user.email,
        "full_name": user.full_name,
    }