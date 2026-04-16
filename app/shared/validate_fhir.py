import requests
import json
import argparse
import sys

# Official HL7 FHIR Validator API wrapper
VALIDATOR_URL = "https://validator.fhir.org/validate"

def validate_resource(filepath_or_json):
    headers = {"Content-Type": "application/json"}
    
    if filepath_or_json.endswith('.json'):
        with open(filepath_or_json, 'r') as f:
            data = f.read()
    else:
        data = filepath_or_json

    print(f"Submitting to {VALIDATOR_URL}...")
    response = requests.post(VALIDATOR_URL, data=data, headers=headers)
    
    if response.status_code != 200:
        print(f"Error communicating with validator: {response.text}")
        return
        
    result = response.json()
    issues = result.get('issue', [])
    
    errors = [i for i in issues if i['severity'] == 'error']
    warnings = [i for i in issues if i['severity'] == 'warning']
    
    print("\n--- Validation Results ---")
    if not errors and not warnings:
        print("✅ SUCCESS! No errors or warnings found.")
    else:
        if errors:
            print(f"❌ ERRORS FOUND ({len(errors)}):")
            for e in errors:
                print(f"  - {e.get('diagnostics', e.get('details', {}).get('text'))}")
        else:
            print("✅ SUCCESS! (No errors found)")
            
        if warnings:
            print(f"\n⚠️ WARNINGS ({len(warnings)}):")
            for w in warnings:
                print(f"  - {w.get('diagnostics', w.get('details', {}).get('text'))}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python validate_fhir.py <path_to_resource.json>")
        sys.exit(1)
    
    validate_resource(sys.argv[1])
