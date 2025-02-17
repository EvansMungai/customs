import frappe
from frappe.model.document import Document
from frappe.model.naming import make_autoname

class Waybill(Document):
    def autoname(self):
        """Set name for Waybill"""
        self.name = make_autoname("WB-.####")
    
    def validate(self):
        """Validate Waybill document"""
        self.validate_manifest()
        self.validate_cargo_details()
    
    def validate_manifest(self):
        """Validate manifest reference"""
        if self.manifest:
            manifest = frappe.get_doc("Manifest", self.manifest)
            if manifest.status != "Submitted":
                frappe.throw("Referenced Manifest must be in Submitted status")
    
    def validate_cargo_details(self):
        """Validate cargo details"""
        if self.packages <= 0:
            frappe.throw("Number of packages must be greater than zero")
        if self.weight <= 0:
            frappe.throw("Weight must be greater than zero")
        if not self.description:
            frappe.throw("Cargo description is mandatory")
    
    def on_submit(self):
        """Handle submission"""
        self.status = "Approved"
    
    def on_cancel(self):
        """Handle cancellation"""
        self.status = "Cancelled"
