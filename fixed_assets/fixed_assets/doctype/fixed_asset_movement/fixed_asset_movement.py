# Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

# import frappe
import frappe
from frappe.model.document import Document
class FixedAssetMovement(Document):
	def on_submit(self):
			self.set_latest_location_and_custodian_in_asset()

	def on_cancel(self):
			self.set_latest_location_and_custodian_in_asset()

	def set_latest_location_and_custodian_in_asset(self):
			current_location, current_employee = "", ""
			cond = "1=1"

			for d in self.assets:
				args = {"asset": d.asset, "company": self.company}

				# latest entry corresponds to current document's location, employee when transaction date > previous dates
				# In case of cancellation it corresponds to previous latest document's location, employee
				latest_movement_entry = frappe.db.sql(
					"""
					SELECT asm_item.target_location, asm_item.to_employee
					FROM `tabFixed Asset Movement Item` asm_item, `tabFixed Asset Movement` asm
					WHERE
						asm_item.parent=asm.name and
						asm_item.asset=%(asset)s and
						asm.company=%(company)s and
						asm.docstatus=1 and {0}
					ORDER BY
						asm.transaction_date desc limit 1
					""".format(
						cond
					),
					args,
				)
				if latest_movement_entry:
					current_location = latest_movement_entry[0][0]
					current_employee = latest_movement_entry[0][1]

				frappe.db.set_value("Fixed Assets", d.asset, "location", current_location)
				frappe.db.set_value("Fixed Assets", d.asset, "custodian", current_employee)