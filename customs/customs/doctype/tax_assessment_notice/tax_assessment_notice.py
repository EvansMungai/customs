import frappe
from frappe.model.document import Document
from frappe.model.naming import make_autoname

class TaxAssessmentNotice(Document):
    def autoname(self):
        """Set name for Tax Assessment Notice"""
        self.name = make_autoname("TAN-.####")
    
    def validate(self):
        """Validate Tax Assessment Notice"""
        self.validate_rates()
        self.validate_declaration()
        self.calculate_total_tax()
    
    def validate_rates(self):
        """Validate tax rates"""
        if self.duty_rate < 0:
            frappe.throw("Import Duty Rate cannot be negative")
        if self.vat_rate < 0:
            frappe.throw("VAT Rate cannot be negative")
        if self.excise_tax and self.excise_tax < 0:
            frappe.throw("Excise Tax Rate cannot be negative")
    
    def validate_declaration(self):
        """Validate linked declaration"""
        if self.declaration_number:
            sad = frappe.get_doc("Single Administrative Document", self.declaration_number)
            if sad.status != "Submitted":
                frappe.throw("Tax Assessment can only be created for Submitted declarations")
    
    def calculate_total_tax(self):
        """Calculate total tax due"""
        if not self.declaration_number:
            return
        
        sad = frappe.get_doc("Single Administrative Document", self.declaration_number)
        
        # Get the customs value from SAD (assuming it's stored in a field called customs_value)
        customs_value = sad.get("customs_value", 0)
        
        # Calculate duties
        duty_amount = (customs_value * self.duty_rate) / 100
        
        # Calculate VAT on (customs value + duty)
        vat_base = customs_value + duty_amount
        vat_amount = (vat_base * self.vat_rate) / 100
        
        # Calculate excise if applicable
        excise_amount = 0
        if self.excise_tax:
            excise_amount = (customs_value * self.excise_tax) / 100
        
        # Set total tax due
        self.total_tax_due = duty_amount + vat_amount + excise_amount
    
    def on_submit(self):
        """Handle submission"""
        self.status = "Generated"
        # Update the linked SAD status
        sad = frappe.get_doc("Single Administrative Document", self.declaration_number)
        sad.status = "Assessed"
        sad.save()
    
    def on_cancel(self):
        """Handle cancellation"""
        self.status = "Cancelled"
