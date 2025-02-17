import frappe
from frappe.model.document import Document

class CustomsRole(Document):
    def validate(self):
        """Validate role configuration"""
        self.validate_role_type()
        self.validate_permissions()
    
    def validate_role_type(self):
        """Validate role type specific permissions"""
        if self.role_type == "External":
            # External users cannot have certain permissions
            if self.can_assess_duties or self.can_approve_release or self.can_override_decisions:
                frappe.throw("External users cannot have assessment, approval, or override permissions")
        
        if self.role_type == "Internal":
            # Internal users must have at least one permission
            if not (self.can_assess_duties or self.can_approve_release or 
                   self.can_inspect_cargo or self.can_override_decisions):
                frappe.throw("Internal users must have at least one customs officer permission")
    
    def validate_permissions(self):
        """Validate permission combinations"""
        # Only supervisors can override decisions
        if self.can_override_decisions and not (
            self.can_assess_duties and self.can_approve_release
        ):
            frappe.throw("Override permission requires assessment and approval permissions")
