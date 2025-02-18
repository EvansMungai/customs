frappe.ui.form.on('Single Administrative Document', {
    hs_code_search: function(frm) {
        if (frm.doc.hs_code_search) {
            frappe.call({
                method: 'customs.customs.api.tariff.search_hs_codes',
                args: {
                    'search_text': frm.doc.hs_code_search
                },
                callback: function(r) {
                    if (r.message && r.message.length > 0) {
                        // Show search results in a dialog
                        let d = new frappe.ui.Dialog({
                            title: 'Select HS Code',
                            fields: [{
                                fieldtype: 'HTML',
                                fieldname: 'results',
                                options: `
                                    <div style="max-height: 300px; overflow-y: auto;">
                                        <table class="table table-bordered">
                                            <thead>
                                                <tr>
                                                    <th>HS Code</th>
                                                    <th>Description</th>
                                                    <th>Duty</th>
                                                    <th>VAT</th>
                                                </tr>
                                            </thead>
                                            <tbody>
                                                ${r.message.map(item => `
                                                    <tr class="hs-code-row" data-item='${JSON.stringify(item)}'>
                                                        <td>${item.hs_code}</td>
                                                        <td>${item.description}</td>
                                                        <td>${item.duty}%</td>
                                                        <td>${item.vat}%</td>
                                                    </tr>
                                                `).join('')}
                                            </tbody>
                                        </table>
                                    </div>
                                `
                            }]
                        });
                        
                        // Handle row click
                        d.$wrapper.find('.hs-code-row').click(function() {
                            let item = JSON.parse($(this).attr('data-item'));
                            // Add a new row to the items table
                            let new_row = frappe.model.add_child(frm.doc, 'SAD Item', 'items');
                            frappe.model.set_value(new_row.doctype, new_row.name, {
                                'hs_code': item.hs_code,
                                'description': item.description,
                                'duty_rate': item.duty,
                                'vat_rate': item.vat,
                                'dc_rate': item.dc
                            });
                            frm.refresh_field('items');
                            // Clear the search field
                            frm.set_value('hs_code_search', '');
                            d.hide();
                        });
                        
                        d.show();
                    }
                }
            });
        }
    },
    refresh: function(frm) {
        // Set focus to search box
        frm.set_df_property('hs_code_search', 'description', 'Type to search, then click an item to add it to the list below');
    }
});
