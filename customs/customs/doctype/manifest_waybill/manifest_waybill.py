import frappe
from frappe.model.document import Document

class ManifestWaybill(Document):
    def validate(self):
        """Validate waybill details"""
        if self.packages <= 0:
            frappe.throw("Number of packages must be greater than zero")
        if self.weight <= 0:
            frappe.throw("Weight must be greater than zero")
