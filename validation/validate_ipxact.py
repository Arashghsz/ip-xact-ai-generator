#!/usr/bin/env python3
import sys
import argparse
from validation import validate_ipxact_component

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Validate IP-XACT XML files against the schema')
    parser.add_argument('xml_file', help='Path to IP-XACT XML file to validate')
    args = parser.parse_args()
    
    # Read the XML file
    try:
        with open(args.xml_file, 'r', encoding='utf-8') as file:
            xml_content = file.read()
    except IOError as e:
        print(f"Error reading file: {e}")
        return 1
    
    # Validate the XML content
    is_valid, message = validate_ipxact_component(xml_content)
    
    # Display the validation result
    if is_valid:
        print(f"✅ Success: {message}")
        return 0
    else:
        print(f"❌ Error: {message}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
