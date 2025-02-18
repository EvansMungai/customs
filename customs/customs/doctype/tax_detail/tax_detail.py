import frappe
from frappe.model.document import Document

class TaxDetail(Document):
    def validate(self):
        """Calculate tax amount based on rate and base amount"""
        if self.rate and self.base_amount:
            self.tax_amount = (self.base_amount * self.rate) / 100
