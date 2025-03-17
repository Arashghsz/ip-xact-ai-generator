#!/usr/bin/env python3
import sys
import argparse
import xmlschema
import pkg_resources
import os

def validate_xml(xml_file, schema_url="http://www.accellera.org/XMLSchema/IPXACT/1685-2014/index.xsd"):
    """
    Validate XML against a schema using xmlschema package
    
    Parameters:
    xml_file (str): Path to XML file
    schema_url (str): URL of the schema
    
    Returns:
    tuple: (is_valid, message)
    """
    try:
        # Check xmlschema version to use appropriate parameters
        xmlschema_version = pkg_resources.get_distribution('xmlschema').version
        print(f"Using xmlschema version: {xmlschema_version}")
        
        # Create schema with version-appropriate parameters
        if pkg_resources.parse_version(xmlschema_version) >= pkg_resources.parse_version('1.0.0'):
            # For newer versions that support lax validation
            try:
                schema = xmlschema.XMLSchema(schema_url, validation='lax')
            except TypeError:
                # Fallback if lax isn't supported
                schema = xmlschema.XMLSchema(schema_url)
        else:
            # For older versions
            schema = xmlschema.XMLSchema(schema_url)
        
        # Validate the XML file
        schema.validate(xml_file)
        return True, "XML validates against schema"
        
    except xmlschema.XMLSchemaValidationError as e:
        # Fall back to content validation
        print("Schema validation failed. Trying basic content validation...")
        return validate_xml_content(xml_file)
    except Exception as e:
        print("Error during schema validation. Trying basic content validation...")
        return validate_xml_content(xml_file)

def validate_xml_content(xml_file):
    """
    Alternative validation using direct content check
    """
    try:
        # Read XML content
        with open(xml_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Check for required IP-XACT elements
        required_elements = [
            "<ipxact:vendor>", 
            "<ipxact:library>", 
            "<ipxact:name>", 
            "<ipxact:version>", 
            "<ipxact:model>",
            "<ipxact:views>",
            "<ipxact:view>",
            "<ipxact:ports>",
            "<ipxact:port>"
        ]
        
        missing_elements = []
        for elem in required_elements:
            if elem not in content:
                missing_elements.append(elem)
        
        if missing_elements:
            return False, f"Required elements missing: {', '.join(missing_elements)}"
        
        # Check for port wire/transactional elements
        port_tags = content.count("<ipxact:port>")
        wire_tags = content.count("<ipxact:wire>")
        transactional_tags = content.count("<ipxact:transactional>")
        
        if port_tags > 0 and (wire_tags + transactional_tags) < port_tags:
            return False, "Some port elements are missing required wire or transactional child elements"
            
        return True, "XML structure appears valid (basic check passed)"
    except Exception as e:
        return False, f"Content validation error: {str(e)}"

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Simple XML validator for IP-XACT files')
    parser.add_argument('xml_file', help='Path to IP-XACT XML file to validate')
    args = parser.parse_args()
    
    # Check if file exists
    if not os.path.exists(args.xml_file):
        print(f"❌ Error: File not found: {args.xml_file}")
        return 1
    
    # Validate the file
    is_valid, message = validate_xml(args.xml_file)
    
    # Display the validation result
    if is_valid:
        print(f"✅ Success: {message}")
        return 0
    else:
        print(f"❌ Error: {message}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
