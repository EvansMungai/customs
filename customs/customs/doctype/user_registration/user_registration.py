import frappe
from frappe.model.document import Document
from frappe.utils import validate_email_address, today
import re

class UserRegistration(Document):
    def validate(self):
        """Validate registration form"""
        self.validate_users()
        self.validate_business_id()
        self.validate_telephone()
        self.validate_agreement()
        self.set_dates()
    
    def validate_users(self):
        """Validate system users"""
        if not self.system_users:
            frappe.throw("At least one system user is required")
        
        if len(self.system_users) > 4:
            frappe.throw("Maximum 4 system users are allowed")
        
        for user in self.system_users:
            if not validate_email_address(user.email):
                frappe.throw(f"Invalid email format for user {user.user_full_name}")
            
            if not self.validate_phone_number(user.telephone):
                frappe.throw(f"Invalid phone number format for user {user.user_full_name}")
    
    def validate_business_id(self):
        """Validate business ID/TIN format"""
        if not re.match(r'^[A-Z0-9]{10,12}$', self.business_id):
            frappe.throw("Invalid Business ID/TIN format")
    
    def validate_telephone(self):
        """Validate phone number format"""
        if not self.validate_phone_number(self.telephone):
            frappe.throw("Invalid phone number format")
    
    def validate_agreement(self):
        """Validate terms agreement"""
        if not self.terms_agreement:
            frappe.throw("You must agree to the security terms and conditions")
    
    def validate_phone_number(self, number):
        """Validate phone number format"""
        return bool(re.match(r'^\+?[0-9]{10,15}$', number))
    
    def set_dates(self):
        """Set application date"""
        if not self.application_date:
            self.application_date = today()
    
    def on_submit(self):
        """Handle submission"""
        self.approval_status = "Pending"
    
    def on_update_after_submit(self):
        """Handle post-submission updates"""
        if self.approval_status == "Approved":
            self.create_user_accounts()
    
    def create_user_accounts(self):
        """Create Frappe user accounts for approved registration"""
        for user in self.system_users:
            if not frappe.db.exists("User", user.email):
                new_user = frappe.get_doc({
                    "doctype": "User",
                    "email": user.email,
                    "first_name": user.user_full_name.split()[0],
                    "last_name": " ".join(user.user_full_name.split()[1:]),
                    "send_welcome_email": 1,
                    "role_profile_name": self.get_role_profile()
                })
                new_user.insert()
    
    def get_role_profile(self):
        """Get appropriate role profile based on business type"""
        role_mapping = {
            "Importer/Exporter": "Customs Trader",
            "Clearing Agent/Broker": "Customs Broker",
            "Shipping Agent/Airline Agent/Transporter": "Shipping Agent",
            "Freight Forwarder": "Freight Forwarder"
        }
        return role_mapping.get(self.business_type)
