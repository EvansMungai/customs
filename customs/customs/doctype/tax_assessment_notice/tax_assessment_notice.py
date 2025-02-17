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
        # This is a placeholder for the actual tax calculation logic
        # In a real implementation, this would fetch values from the SAD
        # and apply the appropriate tax rates
        pass
    
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
