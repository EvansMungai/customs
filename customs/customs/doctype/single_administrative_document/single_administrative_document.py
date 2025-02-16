import frappe
from frappe.model.document import Document
from frappe.model.naming import make_autoname

class SingleAdministrativeDocument(Document):
    def autoname(self):
        """Set name for SAD"""
        self.name = make_autoname("SAD-.####")
    
    def validate(self):
        """Validate SAD document"""
        self.validate_parties()
        self.validate_hs_code()
    
    def validate_parties(self):
        """Validate importer and exporter"""
        if not self.importer:
            frappe.throw("Importer is mandatory")
        if not self.exporter:
            frappe.throw("Exporter is mandatory")
    
    def validate_hs_code(self):
        """Validate HS code format"""
        if self.hs_code and not len(self.hs_code) >= 6:
            frappe.throw("HS Code must be at least 6 digits")
    
    def on_submit(self):
        """Handle submission"""
        self.status = "Submitted"
    
    def on_cancel(self):
        """Handle cancellation"""
        self.status = "Cancelled"
