import frappe
from customs.customs.utils.tariff_loader import load_tariffs

@frappe.whitelist()
def search_hs_codes(search_text):
    """Search HS codes and descriptions"""
    tariff_data = load_tariffs()
    results = []
    
    for section in tariff_data.values():
        for chapter in section['chapters']:
            for tariff in chapter['tariffs']:
                for category in tariff['categories']:
                    for subcat in category['subcategories']:
                        if (search_text.lower() in subcat['code'].lower() or 
                            search_text.lower() in subcat['designation'].lower()):
                            results.append({
                                'hs_code': subcat['code'],
                                'description': subcat['designation'],
                                'duty': subcat['duty'],
                                'vat': subcat['vat'],
                                'dc': subcat['dc']
                            })
    
    return results[:10]  # Limit to 10 results
