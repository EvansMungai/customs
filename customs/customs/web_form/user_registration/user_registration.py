import frappe
from frappe import _

def get_context(context):
    """Add custom context for web form"""
    context.show_sidebar = False
    context.title = _("ASYCUDA World Registration")
    
def validate(doc):
    """Validate web form submission"""
    # Set default values
    doc.application_date = frappe.utils.today()
    doc.approval_status = "Pending"
    
    # Validate number of users
    if len(doc.system_users) > 4:
        frappe.throw(_("Maximum 4 system users are allowed"))
    
    # Validate terms agreement
    if not doc.terms_agreement:
        frappe.throw(_("You must agree to the security terms and conditions"))

def on_submit(doc):
    """Handle web form submission"""
    # Send email notification to customs team
    send_registration_notification(doc)
    
    # Send confirmation email to applicant
    send_confirmation_email(doc)

def send_registration_notification(doc):
    """Send notification to customs team"""
    customs_team_email = frappe.db.get_single_value("Customs Settings", "registration_notification_email")
    if customs_team_email:
        frappe.sendmail(
            recipients=customs_team_email,
            subject=f"New User Registration: {doc.full_name}",
            template="new_registration_notification",
            args={
                "full_name": doc.full_name,
                "business_type": doc.business_type,
                "business_id": doc.business_id,
                "user_count": len(doc.system_users)
            }
        )

def send_confirmation_email(doc):
    """Send confirmation email to applicant"""
    if doc.system_users and doc.system_users[0].email:
        frappe.sendmail(
            recipients=doc.system_users[0].email,
            subject="ASYCUDA World Registration Received",
            template="registration_confirmation",
            args={
                "full_name": doc.full_name,
                "registration_number": doc.name
            }
        )
