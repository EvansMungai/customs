import frappe
from frappe.model.document import Document
from frappe.model.naming import make_autoname

class Manifest(Document):
    def autoname(self):
        """Set name for Manifest"""
        self.name = make_autoname("MAN-.####")
    
    def validate(self):
        """Validate Manifest document"""
        self.validate_ports()
        self.validate_waybills()
    
    def validate_ports(self):
        """Validate port information"""
        if self.port_of_loading == self.port_of_discharge:
            frappe.throw("Port of Loading and Discharge cannot be the same")
    
    def validate_waybills(self):
        """Validate waybills"""
        if not self.waybills:
            frappe.throw("At least one waybill is required")
    
    def on_submit(self):
        """Handle submission"""
        self.status = "Submitted"
    
    def on_cancel(self):
        """Handle cancellation"""
        self.status = "Cancelled"
