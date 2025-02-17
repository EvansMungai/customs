import frappe
from frappe.model.document import Document
from frappe.utils import getdate

class SADDocument(Document):
    def validate(self):
        """Validate SAD document"""
        self.validate_document_date()
        self.validate_attachment()
    
    def validate_document_date(self):
        """Validate document date"""
        if getdate(self.document_date) > getdate():
            frappe.throw(f"Document date cannot be in the future for {self.document_type}")
    
    def validate_attachment(self):
        """Validate document attachment"""
        if not self.attachment:
            frappe.throw(f"Attachment is mandatory for {self.document_type}")
