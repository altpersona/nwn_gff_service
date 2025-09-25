"""API endpoint tests"""
import pytest
from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


def test_health_check():
    """Test health check endpoint"""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["service"] == "nwn-gff-api"
    assert data["version"] == "0.1.0"


def test_api_info():
    """Test API info endpoint"""
    response = client.get("/api/v1/")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "NWN GFF API Service"
    assert data["version"] == "0.1.0"
    assert "endpoints" in data


def test_gff_to_json_invalid_format():
    """Test GFF to JSON with invalid file format"""
    response = client.post(
        "/api/v1/convert/gff-to-json",
        files={"file": ("test.txt", b"invalid content", "text/plain")}
    )
    assert response.status_code == 400
    data = response.json()
    assert "Invalid file format" in data["detail"]


def test_json_to_gff_invalid_format():
    """Test JSON to GFF with invalid file format"""
    response = client.post(
        "/api/v1/convert/json-to-gff",
        files={"file": ("test.txt", b"invalid content", "text/plain")}
    )
    assert response.status_code == 400
    data = response.json()
    assert "Invalid file format" in data["detail"]


def test_sqlite_embed_missing_files():
    """Test SQLite embedding with missing files"""
    response = client.post("/api/v1/convert/sqlite-embed")
    assert response.status_code == 422  # FastAPI validation error


def test_sqlite_extract_invalid_format():
    """Test SQLite extraction with invalid file format"""
    response = client.post(
        "/api/v1/convert/sqlite-extract",
        files={"file": ("test.txt", b"invalid content", "text/plain")}
    )
    assert response.status_code == 400
    data = response.json()
    assert "Invalid file format" in data["detail"]


def test_gff_to_json_valid_gff():
    """Test GFF to JSON conversion with valid GFF-like content"""
    # Create a simple GFF-like content for testing
    gff_content = b"GFF V1.0\nTest: Hello World\nVersion: 1\n"
    
    response = client.post(
        "/api/v1/convert/gff-to-json",
        files={"file": ("test.gff", gff_content, "application/octet-stream")}
    )
    
    # Should succeed with stub implementation
    assert response.status_code == 200
    data = response.json()
    assert "Test" in data
    assert "Version" in data


def test_json_to_gff_valid_json():
    """Test JSON to GFF conversion with valid JSON"""
    json_content = b'{"Test": "Hello World", "Version": 1}'
    
    response = client.post(
        "/api/v1/convert/json-to-gff",
        files={"file": ("test.json", json_content, "application/json")}
    )
    
    # Should succeed and return binary data
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/octet-stream"
    assert "converted.gff" in response.headers["content-disposition"]