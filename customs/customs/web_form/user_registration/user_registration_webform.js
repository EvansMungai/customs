frappe.ready(function() {
    // Validate business ID/TIN format
    frappe.web_form.on('business_id', function(field, value) {
        if (value && !value.match(/^[A-Z0-9]{10,12}$/)) {
            frappe.throw(__('Business ID/TIN must be 10-12 alphanumeric characters'));
        }
    });

    // Validate phone numbers
    frappe.web_form.on('telephone', function(field, value) {
        if (value && !value.match(/^\+?[0-9]{10,15}$/)) {
            frappe.throw(__('Invalid phone number format'));
        }
    });

    // Display security terms
    if (frappe.web_form.get_value('terms_agreement') === 0) {
        frappe.web_form.set_df_property('terms_agreement', 'description', 
            frappe.web_form.context.security_terms);
    }
});
