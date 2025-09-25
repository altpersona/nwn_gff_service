import httpclient, json, os, strutils

const BASE_URL = "http://localhost:8080/api/v1"

proc testHealthCheck() =
  echo "Testing health check endpoint..."
  try:
    let client = newHttpClient()
    let response = client.getContent(BASE_URL & "/health")
    let jsonResponse = parseJson(response)
    
    if jsonResponse{"status"}.getStr() == "ok":
      echo "✓ Health check passed"
    else:
      echo "✗ Health check failed: ", response
  except:
    echo "✗ Health check failed: ", getCurrentExceptionMsg()

proc testGffToJson() =
  echo "\nTesting GFF to JSON conversion..."
  
  # Create a test GFF file (using our shared module)
  let testGffContent = """GFF V1.0
Test: Hello World
Version: 1
"""
  
  try:
    # Write test file
    writeFile("test.gff", testGffContent)
    
    let client = newHttpClient()
    let response = client.postContent(
      BASE_URL & "/convert/gff-to-json",
      multipart = {
        "file": ("test.gff", "application/octet-stream", readFile("test.gff"))
      }
    )
    
    let jsonResponse = parseJson(response)
    if jsonResponse.hasKey("error"):
      echo "✗ GFF to JSON conversion failed: ", jsonResponse{"error"}.getStr()
    else:
      echo "✓ GFF to JSON conversion successful"
      echo "  Response: ", response[0..min(100, response.len-1)], "..."
    
    # Clean up
    removeFile("test.gff")
  except:
    echo "✗ GFF to JSON conversion failed: ", getCurrentExceptionMsg()

proc testJsonToGff() =
  echo "\nTesting JSON to GFF conversion..."
  
  # Create a test JSON file
  let testJsonContent = """{
  "Test": "Hello World",
  "Version": 1
}"""
  
  try:
    # Write test file
    writeFile("test.json", testJsonContent)
    
    let client = newHttpClient()
    let response = client.postContent(
      BASE_URL & "/convert/json-to-gff",
      multipart = {
        "file": ("test.json", "application/json", readFile("test.json"))
      }
    )
    
    if response.len > 0:
      echo "✓ JSON to GFF conversion successful"
      echo "  Response size: ", response.len, " bytes"
      # Save the converted file for inspection
      writeFile("converted.gff", response)
      echo "  Converted file saved as: converted.gff"
    else:
      echo "✗ JSON to GFF conversion returned empty response"
    
    # Clean up
    removeFile("test.json")
  except:
    echo "✗ JSON to GFF conversion failed: ", getCurrentExceptionMsg()

proc testErrorHandling() =
  echo "\nTesting error handling..."
  
  try:
    let client = newHttpClient()
    
    # Test with invalid file format
    let response = client.postContent(
      BASE_URL & "/convert/gff-to-json",
      multipart = {
        "file": ("test.txt", "text/plain", "invalid content")
      }
    )
    
    let jsonResponse = parseJson(response)
    if jsonResponse.hasKey("error") and jsonResponse{"status"}.getInt() == 400:
      echo "✓ Invalid file format error handled correctly"
    else:
      echo "✗ Error handling test failed"
  except:
    echo "✗ Error handling test failed: ", getCurrentExceptionMsg()

proc testRootEndpoint() =
  echo "\nTesting root endpoint..."
  try:
    let client = newHttpClient()
    let response = client.getContent("http://localhost:8080/")
    let jsonResponse = parseJson(response)
    
    if jsonResponse{"service"}.getStr() == "nwn-gff-api":
      echo "✓ Root endpoint working"
    else:
      echo "✗ Root endpoint test failed"
  except:
    echo "✗ Root endpoint test failed: ", getCurrentExceptionMsg()

proc runAllTests() =
  echo "=== NWN GFF API Test Suite ==="
  echo "Make sure the API server is running on port 8080"
  echo "Run: nim c -r gff_api.nim"
  echo ""
  
  # Run tests
  testRootEndpoint()
  testHealthCheck()
  testGffToJson()
  testJsonToGff()
  testErrorHandling()
  
  echo "\n=== Test Suite Complete ==="

when isMainModule:
  runAllTests()