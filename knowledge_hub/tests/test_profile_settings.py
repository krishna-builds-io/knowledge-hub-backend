import frappe
from frappe.tests import IntegrationTestCase

from knowledge_hub.api.profile import change_password, get_profile, update_profile
from knowledge_hub.api.settings import (
	PREFERENCE_DOCTYPE,
	get_preferences,
	update_preferences,
)


def create_test_user(email: str):
	if frappe.db.exists("User", email):
		return frappe.get_doc("User", email)

	user = frappe.get_doc(
		{
			"doctype": "User",
			"email": email,
			"first_name": "Test",
			"last_name": "User",
			"enabled": 1,
		}
	)
	user.insert(ignore_permissions=True)

	return user


def reset_preferences(user):
	frappe.db.delete(PREFERENCE_DOCTYPE, {"user": user.name})


class IntegrationTestProfileSettings(IntegrationTestCase):
	def test_get_profile_returns_current_user(self):
		user = create_test_user("profile.api@example.com")
		frappe.set_user(user.name)

		profile = get_profile()

		self.assertEqual(profile["name"], user.name)
		self.assertEqual(profile["email"], user.email)

	def test_update_profile(self):
		user = create_test_user("profile.update@example.com")
		frappe.set_user(user.name)

		profile = update_profile(first_name="Updated", last_name="Profile")

		self.assertEqual(profile["first_name"], "Updated")
		self.assertEqual(profile["last_name"], "Profile")

	def test_change_password_rejects_short_password(self):
		user = create_test_user("profile.short.password@example.com")
		frappe.set_user(user.name)

		with self.assertRaises(frappe.ValidationError):
			change_password(old_password="wrong-password", new_password="short")

	def test_change_password_rejects_wrong_current_password(self):
		user = create_test_user("profile.wrong.password@example.com")
		frappe.set_user(user.name)

		with self.assertRaises(frappe.ValidationError):
			change_password(
				old_password="definitely-wrong-password",
				new_password="valid-password-123",
			)

	def test_get_preferences_creates_default_preferences(self):
		user = create_test_user("settings.default@example.com")
		reset_preferences(user)
		frappe.set_user(user.name)

		preferences = get_preferences()

		self.assertEqual(preferences["user"], user.name)
		self.assertEqual(preferences["theme"], "System")
		self.assertEqual(preferences["preferences"], {})

	def test_update_preferences(self):
		user = create_test_user("settings.update@example.com")
		reset_preferences(user)
		frappe.set_user(user.name)

		preferences = update_preferences(
			theme="Dark",
			preferences={"compactMode": True},
		)

		self.assertEqual(preferences["theme"], "Dark")
		self.assertEqual(preferences["preferences"], {"compactMode": True})

	def test_update_preferences_rejects_invalid_theme(self):
		user = create_test_user("settings.invalid.theme@example.com")
		frappe.set_user(user.name)

		with self.assertRaises(frappe.ValidationError):
			update_preferences(theme="Blue", preferences={})

	def test_preferences_are_user_scoped(self):
		first_user = create_test_user("settings.scope.one@example.com")
		second_user = create_test_user("settings.scope.two@example.com")
		reset_preferences(first_user)
		reset_preferences(second_user)

		frappe.set_user(first_user.name)
		update_preferences(theme="Light", preferences={"density": "comfortable"})

		frappe.set_user(second_user.name)
		second_preferences = get_preferences()

		self.assertEqual(second_preferences["theme"], "System")
		self.assertEqual(second_preferences["preferences"], {})

		frappe.set_user(first_user.name)
		first_preferences = get_preferences()

		self.assertEqual(first_preferences["theme"], "Light")
		self.assertEqual(first_preferences["preferences"], {"density": "comfortable"})