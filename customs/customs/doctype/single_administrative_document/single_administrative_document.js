frappe.ui.form.on('Single Administrative Document', {
    refresh: function (frm) {
        frm.set_df_property('hs_code_search', 'description', 'Type to search, then click an item to add it to the list below');
        // Add a custom HTML field to handle search and dropdown dynamically
        frm.fields_dict.hs_code_search.$wrapper.html(`
            <div class="frappe-control input-max-width">
                <div class="form-group d-flex align-items-start">
                    <!-- Label on the Left -->
                    <label class="control-label" style="flex: 0 0 25%; margin-right: 50px;">
                        ${frm.fields_dict.hs_code_search.df.label}
                    </label>
                    
                    <!-- Input, Description, and Results on the Right -->
                    <div style="flex: 1;">
                        <div class="control-input-wrapper">
                            <input type="text" id="custom_hs_code_search" 
                                   class="form-control" 
                                   placeholder="${frm.fields_dict.hs_code_search.df.placeholder || 'Type to search HS Codes...'}">
                        </div>
                        <!-- Description -->
                        <div class="help-box" id="description-box" style="margin-top: 8px;">
                            ${frm.fields_dict.hs_code_search.df.description || 'Type to search and select from results.'}
                        </div>
                        <!-- Results Dropdown -->
                        <div id="custom_hs_code_results" 
                             style="display: none; max-height: 200px; overflow-y: auto; 
                                    border: 1px solid #ccc; border-radius: 8px; 
                                    box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1); 
                                    margin-top: 8px; background: #ffffff; z-index: 1000; position: absolute; width: 100%; padding: 8px 0;">
                        </div>
                    </div>
                </div>
            </div>
        `);

        // Attach the input event listener to the custom input field
        $('#custom_hs_code_search').on('input', frappe.utils.debounce(function () {
            let search_text = $(this).val();
            if (search_text.length > 1) { 
                $('#description-box').hide();
                frappe.call({
                    method: 'customs.customs.api.tariff.search_hs_codes', // API to fetch matching results
                    args: { search_text: search_text },
                    callback: function (r) {
                        if (r.message && r.message.length > 0) {
                            // Populate dropdown with results
                            let results_html = r.message.map(item => `
                                <div class="custom-hs-code-item" 
                                    data-item='${JSON.stringify(item)}' 
                                    style="padding: 12px; cursor: pointer; 
                                           border-bottom: 1px solid #ddd; 
                                           font-size: 14px; 
                                           color: #333; background: #fff; 
                                           transition: background 0.2s ease, border-left-color 0.2s ease; 
                                           border-left: 4px solid transparent;">
                                    <strong>${item.hs_code}</strong> - ${item.description} - ${item.duty} - ${item.vat} - ${item.dc}
                                </div>
                            `).join('');

                            $('#custom_hs_code_results').html(results_html).show();

                            // Attach click event to each item
                            $('.custom-hs-code-item').on('click', function () {
                                let item = JSON.parse($(this).attr('data-item'));

                                // Check if the items table is empty or only has a blank row
                                if (!frm.doc.items || frm.doc.items.length === 0 || (frm.doc.items.length === 1 && !frm.doc.items[0].hs_code)) {
                                    // Update the first row if the table is empty or has only a blank row
                                    let first_row = frm.doc.items[0] || frappe.model.add_child(frm.doc, 'SAD Item', 'items');
                                    frappe.model.set_value(first_row.doctype, first_row.name, {
                                        hs_code: item.hs_code,
                                        description: item.description,
                                        duty_rate: item.duty,
                                        vat_rate: item.vat,
                                        dc_rate: item.dc
                                    });
                                } else {
                                    // Add a new row if the table already has valid data
                                    let new_row = frappe.model.add_child(frm.doc, 'SAD Item', 'items');
                                    frappe.model.set_value(new_row.doctype, new_row.name, {
                                        hs_code: item.hs_code,
                                        description: item.description,
                                        duty_rate: item.duty,
                                        vat_rate: item.vat,
                                        dc_rate: item.dc
                                    });
                                }

                                // Refresh the items table
                                frm.refresh_field('items');

                                // Clear the search field and hide results
                                $('#custom_hs_code_search').val('');
                                $('#custom_hs_code_results').hide();
                                $('#description-box').show();
                            });
                        } else {
                            $('#custom_hs_code_results').html('<div style="padding: 8px;">No matching HS Codes found.</div>').show();
                        }
                    }
                });
            } else {
                $('#custom_hs_code_results').hide(); // Hide dropdown if input is cleared
            }
        }, 300)); // Debounce for smoother interactions
    }
});