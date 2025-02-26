import frappe
import json
import os
from frappe.utils import cstr

@frappe.whitelist()
def search_hs_codes(search_text):
    """Search HS codes and descriptions from tariff data"""
    results = []
    search_text = cstr(search_text).lower()
    
    # Load tariff data
    fixtures_path = os.path.join(os.path.dirname(__file__), '..', '..', 'fixtures', 'tariffs')
    
    # Search through all tariff files
    for filename in os.listdir(fixtures_path):
        if filename.endswith('.json'):
            with open(os.path.join(fixtures_path, filename)) as f:
                section_data = json.load(f)
                
                # Search through chapters
                for chapter in section_data.get('chapters', []):
                    for tariff in chapter.get('tariffs', []):
                        for category in tariff.get('categories', []):
                            for subcategory in category.get('subcategories', []):
                                if (search_text in subcategory['code'].lower() or 
                                    search_text in subcategory['designation'].lower()):
                                    results.append({
                                        'hs_code': subcategory['code'],
                                        'description': subcategory['designation'],
                                        'duty': subcategory['duty'],
                                        'vat': subcategory['vat'],
                                        'dc': subcategory['dc']
                                    })
                                    
                                # Limit results to avoid performance issues
                                if len(results) >= 20:
                                    return results
    
    return results
