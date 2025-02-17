import frappe
from frappe.model.document import Document

class SADItem(Document):
    def validate(self):
        """Validate SAD item"""
        self.validate_hs_code()
        self.validate_values()
        self.calculate_customs_value()
    
    def validate_hs_code(self):
        """Validate HS code format"""
        if not self.hs_code or len(self.hs_code) < 6:
            frappe.throw(f"HS Code must be at least 6 digits for item {self.item_number}")
    
    def validate_values(self):
        """Validate numeric values"""
        if self.quantity <= 0:
            frappe.throw(f"Quantity must be greater than zero for item {self.item_number}")
        if self.unit_price <= 0:
            frappe.throw(f"Unit price must be greater than zero for item {self.item_number}")
        if self.weight <= 0:
            frappe.throw(f"Weight must be greater than zero for item {self.item_number}")
    
    def calculate_customs_value(self):
        """Calculate customs value based on quantity and unit price"""
        self.customs_value = self.quantity * self.unit_price
