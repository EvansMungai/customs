import frappe
from frappe.model.document import Document
from frappe.utils import validate_email_address

class CustomsOffice(Document):
    def validate(self):
        """Validate Customs Office"""
        self.validate_contact_info()
    
    def validate_contact_info(self):
        """Validate contact information"""
        if not validate_email_address(self.email):
            frappe.throw("Invalid email format")
        
        if not self.phone or not self.phone.strip():
            frappe.throw("Phone number is required")
