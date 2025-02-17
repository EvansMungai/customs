import frappe
import json
import os
from pathlib import Path

def load_tariffs():
    """Load all tariff files from fixtures/tariffs directory"""
    cache_key = "customs_tariff_data"
    tariff_data = frappe.cache().get_value(cache_key)
    
    if not tariff_data:
        base_path = frappe.get_app_path("customs", "fixtures", "tariffs")
        tariff_data = {}
        
        for file_path in Path(base_path).glob("*.json"):
            with open(file_path, 'r', encoding='utf-8') as file:
                section_data = json.load(file)
                tariff_data[section_data['section_code']] = section_data
        
        frappe.cache().set_value(cache_key, tariff_data)
    
    return tariff_data

def get_tariff_rates(hs_code):
    """Get duty and tax rates for a specific HS code"""
    if not hasattr(frappe.local, 'tariff_data'):
        frappe.local.tariff_data = load_tariffs()
    
    section_code = hs_code[:2]
    chapter_code = hs_code[:2]
    position_code = hs_code[:5]
    full_code = hs_code
    
    section = frappe.local.tariff_data.get(section_code)
    if not section:
        return None
        
    for chapter in section['chapters']:
        if chapter['chapter_code'] == chapter_code:
            for tariff in chapter['tariffs']:
                if tariff['tariff_position'] == position_code:
                    for category in tariff['categories']:
                        for subcat in category['subcategories']:
                            if subcat['code'] == full_code:
                                return {
                                    'duty_rate': subcat['duty'],
                                    'vat_rate': subcat['vat'],
                                    'dc_rate': subcat['dc']
                                }
    return None
