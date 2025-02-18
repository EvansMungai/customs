frappe.ui.form.on('SAD Item', {
    hs_code: function(frm, cdt, cdn) {
        let row = locals[cdt][cdn];
        if (row.hs_code) {
            frappe.call({
                method: 'customs.customs.api.tariff.search_hs_codes',
                args: {
                    'search_text': row.hs_code
                },
                callback: function(r) {
                    if (r.message && r.message.length > 0) {
                        let item = r.message[0];  // Get first match
                        frappe.model.set_value(cdt, cdn, {
                            'description': item.description,
                            'duty_rate': item.duty,
                            'vat_rate': item.vat,
                            'dc_rate': item.dc
                        });
                    }
                }
            });
        }
    }
});

// Add autocomplete to HS Code field
frappe.ui.form.on('Single Administrative Document', {
    refresh: function(frm) {
        frm.fields_dict['items'].grid.get_field('hs_code').get_query = function(doc, cdt, cdn) {
            return {
                query: 'customs.customs.api.tariff.search_hs_codes',
                filters: { search_text: '{% raw %}{{ txt }}{% endraw %}' }
            };
        };
    }
});
