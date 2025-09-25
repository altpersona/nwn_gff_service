#!/usr/bin/env python3
"""
Test script to demonstrate web interface integration with the NWN GFF API service.
This script creates sample files and shows how the web interface would interact with the API.
"""

import json
import requests
import os
from pathlib import Path

# API Configuration
API_BASE_URL = "http://localhost:8000/api/v1"

def create_sample_files():
    """Create sample JSON and GFF files for testing."""
    
    # Create sample JSON data that would be compatible with the API
    sample_json = {
        "Test": "Hello World",
        "Version": 1,
        "Data": {
            "field1": "value1",
            "field2": 42,
            "nested": {
                "item1": "test",
                "item2": 123.45
            }
        }
    }
    
    # Create sample JSON file
    json_file = "test_sample.json"
    with open(json_file, 'w') as f:
        json.dump(sample_json, f, indent=2)
    
    print(f"✅ Created sample JSON file: {json_file}")
    print(f"   File size: {os.path.getsize(json_file)} bytes")
    
    return json_file

def test_api_health():
    """Test the API health endpoint."""
    try:
        response = requests.get(f"{API_BASE_URL}/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API Health Check: {data['status']} - Service: {data['service']}")
            return True
        else:
            print(f"❌ API Health Check Failed: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API service. Make sure it's running on http://localhost:8000")
        return False

def test_json_to_gff_conversion(json_file):
    """Test JSON to GFF conversion."""
    print(f"\n🔄 Testing JSON to GFF conversion with {json_file}...")
    
    try:
        with open(json_file, 'rb') as f:
            files = {'file': f}
            response = requests.post(f"{API_BASE_URL}/convert/json-to-gff", files=files)
        
        if response.status_code == 200:
            # Save the converted GFF file
            gff_filename = json_file.replace('.json', '_converted.gff')
            with open(gff_filename, 'wb') as f:
                f.write(response.content)
            
            print(f"✅ JSON to GFF conversion successful!")
            print(f"   Output file: {gff_filename}")
            print(f"   File size: {os.path.getsize(gff_filename)} bytes")
            return gff_filename
        else:
            error_data = response.json() if response.content else {"detail": "Unknown error"}
            print(f"❌ JSON to GFF conversion failed: {error_data.get('detail', 'Unknown error')}")
            return None
            
    except Exception as e:
        print(f"❌ JSON to GFF conversion error: {e}")
        return None

def test_gff_to_json_conversion(gff_file):
    """Test GFF to JSON conversion."""
    print(f"\n🔄 Testing GFF to JSON conversion with {gff_file}...")
    
    try:
        with open(gff_file, 'rb') as f:
            files = {'file': f}
            response = requests.post(f"{API_BASE_URL}/convert/gff-to-json", files=files)
        
        if response.status_code == 200:
            json_data = response.json()
            
            # Save the converted JSON file
            json_filename = gff_file.replace('_converted.gff', '_back_to.json')
            with open(json_filename, 'w') as f:
                json.dump(json_data, f, indent=2)
            
            print(f"✅ GFF to JSON conversion successful!")
            print(f"   Output file: {json_filename}")
            print(f"   File size: {os.path.getsize(json_filename)} bytes")
            
            # Verify the conversion worked by comparing key data
            print(f"   Sample data: {json.dumps(json_data, indent=2)[:200]}...")
            
            return json_filename
        else:
            error_data = response.json() if response.content else {"detail": "Unknown error"}
            print(f"❌ GFF to JSON conversion failed: {error_data.get('detail', 'Unknown error')}")
            return None
            
    except Exception as e:
        print(f"❌ GFF to JSON conversion error: {e}")
        return None

def demonstrate_web_interface_workflow():
    """Demonstrate the complete web interface workflow."""
    print("=" * 60)
    print("🌐 WEB INTERFACE INTEGRATION DEMONSTRATION")
    print("=" * 60)
    
    # Step 1: Check API health
    print("\n📊 Step 1: Checking API health...")
    if not test_api_health():
        print("❌ Cannot proceed - API service not available")
        return False
    
    # Step 2: Create sample files
    print("\n📁 Step 2: Creating sample files...")
    json_file = create_sample_files()
    
    # Step 3: Test JSON to GFF conversion
    print("\n🔧 Step 3: Testing JSON → GFF conversion...")
    gff_file = test_json_to_gff_conversion(json_file)
    
    if gff_file:
        # Step 4: Test GFF to JSON conversion
        print("\n🔧 Step 4: Testing GFF → JSON conversion...")
        back_to_json = test_gff_to_json_conversion(gff_file)
        
        if back_to_json:
            print(f"\n✅ Round-trip conversion successful!")
            print(f"   Original: {json_file}")
            print(f"   Converted to GFF: {gff_file}")
            print(f"   Converted back to JSON: {back_to_json}")
            return True
    
    return False

def demonstrate_web_interface_code():
    """Show how the web interface JavaScript would call the API."""
    print("\n" + "=" * 60)
    print("💻 WEB INTERFACE JAVASCRIPT EXAMPLES")
    print("=" * 60)
    
    print("""
// Example: Button click handler for JSON to GFF conversion
async function convertJsonToGff() {
    const fileInput = document.getElementById('jsonFile');
    const file = fileInput.files[0];
    
    if (!file) {
        showError('Please select a JSON file');
        return;
    }
    
    // Create FormData (same as our Python test)
    const formData = new FormData();
    formData.append('file', file);
    
    try {
        // API call (same endpoint as our test)
        const response = await fetch('http://localhost:8000/api/v1/convert/json-to-gff', {
            method: 'POST',
            body: formData
        });
        
        if (response.ok) {
            // Handle binary response
            const blob = await response.blob();
            
            // Create download link
            const downloadUrl = URL.createObjectURL(blob);
            const downloadLink = document.createElement('a');
            downloadLink.href = downloadUrl;
            downloadLink.download = file.name.replace('.json', '.gff');
            downloadLink.click();
            
            showSuccess('Conversion complete! File downloaded.');
        } else {
            const error = await response.json();
            showError(error.detail || 'Conversion failed');
        }
    } catch (error) {
        showError('Cannot connect to API service');
    }
}
""")

def main():
    """Main test function."""
    print("🧪 Testing Web Interface Integration with NWN GFF API Service")
    print("This demonstrates how a webpage would interact with the API.")
    
    # Check if API is running
    print(f"\n🎯 API Endpoint: {API_BASE_URL}")
    
    # Run the demonstration
    success = demonstrate_web_interface_workflow()
    
    if success:
        print("\n✅ Web interface integration demonstration completed successfully!")
        demonstrate_web_interface_code()
    else:
        print("\n❌ Demonstration failed. Check that the API service is running.")
    
    # Cleanup
    print("\n🧹 Cleaning up test files...")
    test_files = ['test_sample.json', 'test_sample_converted.gff', 'test_sample_back_to.json']
    for file in test_files:
        if os.path.exists(file):
            os.remove(file)
            print(f"   Removed: {file}")
    
    print("\n✨ Web interface integration test complete!")

if __name__ == "__main__":
    main()