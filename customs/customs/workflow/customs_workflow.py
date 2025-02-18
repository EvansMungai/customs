import frappe

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
        {
            'state': 'Draft',
            'action': 'Submit',
            'next_state': 'Submitted',
            'allowed': 'Customs Broker',
            'condition': 'doc.validate_parties()'
        },
        {
            'state': 'Submitted',
            'action': 'Assess',
            'next_state': 'Assessed',
            'allowed': 'Customs Officer',
            'condition': 'doc.validate_hs_code()'
        },
        {
            'state': 'Assessed',
            'action': 'Mark Paid',
            'next_state': 'Paid',
            'allowed': 'Customs Officer',
            'condition': 'doc.validate_payment()'
        },
        {
            'state': 'Paid',
            'action': 'Release',
            'next_state': 'Released',
            'allowed': 'Customs Officer',
            'condition': 'doc.validate_release()'
        },
        {
            'state': 'Draft',
            'action': 'Cancel',
            'next_state': 'Cancelled',
            'allowed': 'Customs Officer'
        }
    ]

def create_customs_workflow():
    """Create the Customs workflow if it doesn't exist"""
    # Create required roles if they don't exist
    required_roles = ['Customs Broker', 'Customs Officer']
    for role in required_roles:
        if not frappe.db.exists('Role', role):
            new_role = frappe.new_doc('Role')
            new_role.role_name = role
            new_role.desk_access = 1
            new_role.insert(ignore_permissions=True)

    # Create workflow states if they don't exist
    for state in get_workflow_states():
        state_name = state['state']
        if not frappe.db.exists('Workflow State', state_name):
            ws = frappe.new_doc('Workflow State')
            ws.workflow_state_name = state_name
            ws.style = 'Primary'
            ws.insert(ignore_permissions=True)

    # Create the workflow if it doesn't exist
    if not frappe.db.exists('Workflow', 'Customs Declaration Process'):
        workflow = frappe.new_doc('Workflow')
        workflow.workflow_name = 'Customs Declaration Process'
        workflow.document_type = 'Single Administrative Document'
        workflow.workflow_state_field = 'workflow_state'
        workflow.is_active = 1
        workflow.send_email_alert = 1
        
        # Add states
        for state in get_workflow_states():
            workflow.append('states', {
                'state': state['state'],
                'doc_status': state['doc_status'],
                'allow_edit': 'System Manager'
            })
            
        # Add transitions
        for transition in get_workflow_transitions():
            workflow.append('transitions', {
                'state': transition['state'],
                'action': transition['action'],
                'next_state': transition['next_state'],
                'allowed': transition['allowed'],
                'allow_self_approval': 1,
                'condition': transition.get('condition', '')
            })
            
        try:
            workflow.insert(ignore_permissions=True)
        except Exception as e:
            frappe.log_error("Workflow creation failed", str(e))
            raise
