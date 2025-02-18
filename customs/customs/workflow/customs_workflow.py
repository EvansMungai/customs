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
    if not frappe.db.exists('Workflow', 'Customs Declaration Process'):
        # First create workflow states
        states = []
        for state_data in get_workflow_states():
            state = frappe.new_doc('Workflow Document State')
            state.update(state_data)
            state.insert(ignore_permissions=True)
            states.append(state)

        # Create workflow transitions
        transitions = []
        for transition_data in get_workflow_transitions():
            transition = frappe.new_doc('Workflow Transition')
            transition.update(transition_data)
            transition.insert(ignore_permissions=True)
            transitions.append(transition)

        # Create the workflow
        workflow = frappe.new_doc('Workflow')
        workflow.name = 'Customs Declaration Process'
        workflow.document_type = 'Single Administrative Document'
        workflow.workflow_state_field = 'workflow_state'
        workflow.is_active = 1
        workflow.send_email_alert = 1
        
        # Link states and transitions
        for state in states:
            workflow.append('states', {'state': state.name, 'doc_status': state.doc_status})
            
        for transition in transitions:
            workflow.append('transitions', {
                'state': transition.state,
                'action': transition.action,
                'next_state': transition.next_state,
                'allowed': transition.allowed
            })
            
        workflow.insert(ignore_permissions=True)
