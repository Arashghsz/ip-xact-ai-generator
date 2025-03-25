from lxml import etree
import requests
import os
import re
from urllib.parse import urljoin, urlparse

def download_schema_with_dependencies(base_url, schema_dir="schema"):
    """
    Download IP-XACT schema and all its dependencies
    
    Parameters:
    base_url (str): The URL to the main schema file
    schema_dir (str): Directory to store schema files
    
    Returns:
    str: Path to the main schema file
    """
    # Create schema directory if not exists
    if not os.path.exists(schema_dir):
        os.makedirs(schema_dir)
    
    # Extract base directory from URL
    base_dir = "/".join(base_url.split("/")[:-1]) + "/"
    
    # Download main schema file
    main_file_name = os.path.basename(base_url)
    main_schema_file = os.path.join(schema_dir, main_file_name)
    
    downloaded_files = set()
    
    def download_schema(url, local_dir):
        if url in downloaded_files:
            return
            
        downloaded_files.add(url)
        
        file_name = os.path.basename(url)
        local_path = os.path.join(local_dir, file_name)
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(local_path), exist_ok=True)
        
        print(f"Downloading schema file: {url}")
        try:
            response = requests.get(url)
            with open(local_path, 'wb') as f:
                f.write(response.content)
            
            # Find all XSD includes in the schema
            content = response.text
            includes = re.findall(r'<xs:include schemaLocation="([^"]+)"', content)
            imports = re.findall(r'<xs:import schemaLocation="([^"]+)"', content)
            all_refs = includes + imports
            
            # Download all dependencies
            for ref in all_refs:
                if ref.startswith('http'):
                    ref_url = ref
                else:
                    ref_url = urljoin(url, ref)
                
                # Create local path for the dependency
                ref_path = os.path.join(schema_dir, os.path.basename(ref))
                download_schema(ref_url, schema_dir)
                
        except Exception as e:
            print(f"Error downloading {url}: {e}")
    
    # Start the download process
    download_schema(base_url, schema_dir)
    
    return main_schema_file

def validate_ipxact_component(xml_content):
    """
    Validate an IP-XACT component against the IP-XACT schema
    
    Parameters:
    xml_content (str): The IP-XACT XML content
    
    Returns:
    tuple: (is_valid, validation_message)
    """
    # IP-XACT schema location
    schema_url = "http://www.accellera.org/XMLSchema/IPXACT/1685-2014/index.xsd"
    schema_dir = "ipxact_schema"
    
    # Download schema with dependencies
    schema_file = download_schema_with_dependencies(schema_url, schema_dir)
    
    try:
        # Use a direct approach instead of a custom resolver
        # Parse the schema directly with full paths to dependencies
        xmlparser = etree.XMLParser(load_dtd=True, resolve_entities=True)
        
        # Parse the XML to validate
        xml_doc = etree.fromstring(xml_content.encode('utf-8'))
        
        # Process schema files
        schema_doc = None
        try:
            # Try to create schema without resolver first
            schema_tree = etree.parse(schema_file)
            schema_doc = etree.XMLSchema(schema_tree)
        except Exception as schema_error:
            print(f"Failed to load schema directly: {schema_error}")
            print("Using alternate validation method...")
            
            # Use xmllint as a fallback
            # This requires xmllint to be installed on the system
            import subprocess
            import tempfile
            
            with tempfile.NamedTemporaryFile(delete=False, suffix=".xml") as tmp:
                tmp.write(xml_content.encode('utf-8'))
                tmp_path = tmp.name
            
            try:
                # Run xmllint command
                result = subprocess.run(
                    ["xmllint", "--schema", schema_file, tmp_path, "--noout"],
                    capture_output=True,
                    text=True
                )
                if result.returncode == 0:
                    return True, "XML validates against IP-XACT schema"
                else:
                    return False, f"Schema validation error: {result.stderr}"
            except FileNotFoundError:
                return False, "Validation error: xmllint tool not found. Please install libxml2-utils."
            finally:
                os.unlink(tmp_path)
        
        # Validate the document
        schema_doc.assertValid(xml_doc)
        return True, "XML validates against IP-XACT schema"
    
    except etree.DocumentInvalid as e:
        return False, f"Schema validation error: {str(e)}"
    except etree.XMLSyntaxError as e:
        return False, f"XML syntax error: {str(e)}"
    except Exception as e:
        return False, f"Validation error: {str(e)}"