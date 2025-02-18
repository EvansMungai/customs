import frappe
from frappe.model.workflow import WorkflowTransition, add_workflow

def get_workflow_states():
    """Define workflow states for customs documents"""
    return [
        {'state': 'Draft', 'doc_status': 0, 'is_active': 1},
        {'state': 'Submitted', 'doc_status': 1, 'is_active': 1},
        {'state': 'Assessed', 'doc_status': 1, 'is_active': 1},
        {'state': 'Paid', 'doc_status': 1, 'is_active': 1},
        {'state': 'Released', 'doc_status': 1, 'is_active': 1},
        {'state': 'Cancelled', 'doc_status': 2, 'is_active': 1}
    ]

def get_workflow_transitions():
    """Define allowed transitions between states"""
    return [
        WorkflowTransition(
            state='Draft', action='Submit', next_state='Submitted',
            allowed='Customs Broker', condition='doc.validate_parties()'
        ),
        WorkflowTransition(
            state='Submitted', action='Assess', next_state='Assessed',
            allowed='Customs Officer', condition='doc.validate_hs_code()'
        ),
        WorkflowTransition(
            state='Assessed', action='Mark Paid', next_state='Paid',
            allowed='Customs Officer', condition='doc.validate_payment()'
        ),
        WorkflowTransition(
            state='Paid', action='Release', next_state='Released',
            allowed='Customs Officer', condition='doc.validate_release()'
        ),
        WorkflowTransition(
            state='Draft', action='Cancel', next_state='Cancelled',
            allowed='Customs Officer'
        )
    ]

def create_customs_workflow():
    """Create the Customs workflow if it doesn't exist"""
    if not frappe.db.exists('Workflow', 'Customs Declaration Process'):
        workflow = {
            'name': 'Customs Declaration Process',
            'document_type': 'Single Administrative Document',
            'workflow_state_field': 'workflow_state',
            'is_active': 1,
            'send_email_alert': 1,
            'states': get_workflow_states(),
            'transitions': get_workflow_transitions()
        }
        add_workflow(workflow)
