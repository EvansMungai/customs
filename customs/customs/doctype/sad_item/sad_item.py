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
        """Calculate customs value and taxes based on quantity and unit price"""
        from customs.customs.utils.tariff_loader import get_tariff_rates
        
        # Calculate base customs value
        self.customs_value = self.quantity * self.unit_price
        
        # Get and apply tariff rates
        rates = get_tariff_rates(self.hs_code)
        if rates:
            duty_amount = (self.customs_value * rates['duty_rate']) / 100
            vat_base = self.customs_value + duty_amount
            vat_amount = (vat_base * rates['vat_rate']) / 100
            dc_amount = (self.customs_value * rates['dc_rate']) / 100
            
            # Store calculated values
            self.duty_amount = duty_amount
            self.vat_amount = vat_amount
            self.dc_amount = dc_amount
            self.total_tax = duty_amount + vat_amount + dc_amount
