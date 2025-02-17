import frappe
from frappe.model.document import Document
from frappe.model.naming import make_autoname
from frappe.utils import now_datetime

class CargoReleaseOrder(Document):
    def autoname(self):
        """Set name for Cargo Release Order"""
        self.name = make_autoname("CRO-.####")
    
    def validate(self):
        """Validate Cargo Release Order"""
        self.validate_declaration()
        self.validate_release_date()
    
    def validate_declaration(self):
        """Validate linked declaration"""
        if self.declaration_number:
            sad = frappe.get_doc("Single Administrative Document", self.declaration_number)
            if sad.status != "Paid":
                frappe.throw("Cargo Release Order can only be created for Paid declarations")
    
    def validate_release_date(self):
        """Validate release date"""
        if not self.release_date:
            self.release_date = now_datetime()
    
    def on_submit(self):
        """Handle submission"""
        self.status = "Released"
        # Update the linked SAD status
        sad = frappe.get_doc("Single Administrative Document", self.declaration_number)
        sad.status = "Released"
        sad.save()
    
    def on_cancel(self):
        """Handle cancellation"""
        self.status = "Cancelled"
