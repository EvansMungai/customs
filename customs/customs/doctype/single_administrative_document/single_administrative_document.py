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
        self.validate_workflow_state()

    def validate_workflow_state(self):
        """Validate workflow state transitions"""
        if self.workflow_state:
            if self.workflow_state == "Assessed" and not frappe.db.exists(
                "Tax Assessment Notice", {"declaration_number": self.name, "status": "Generated"}
            ):
                frappe.throw("Cannot move to Assessed state without a generated Tax Assessment")
            
            if self.workflow_state == "Paid" and not frappe.db.exists(
                "Tax Assessment Notice", {"declaration_number": self.name, "status": "Paid"}
            ):
                frappe.throw("Cannot move to Paid state without payment confirmation")
            
            if self.workflow_state == "Released" and not frappe.db.exists(
                "Cargo Release Order", {"declaration_number": self.name, "status": "Released"}
            ):
                frappe.throw("Cannot move to Released state without a release order")
    
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
