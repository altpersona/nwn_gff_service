# NWN GFF API Documentation

## Overview
The NWN GFF API provides HTTP endpoints for converting between GFF (Game File Format) and JSON formats, with support for SQLite database embedding and extraction.

## Base URL
```
http://localhost:8080/api/v1
```

## Authentication
No authentication is required for this version of the API.

## Endpoints

### Health Check
Check if the API service is running.

**Endpoint:** `GET /api/v1/health`

**Response:**
```json
{
  "status": "ok",
  "service": "nwn-gff-api",
  "version": "0.1.0"
}
```

**Status Codes:**
- `200 OK` - Service is healthy

---

### Convert GFF to JSON
Convert a GFF file to JSON format.

**Endpoint:** `POST /api/v1/convert/gff-to-json`

**Content-Type:** `multipart/form-data`

**Parameters:**
- `file` (required) - GFF file to convert (.gff, .bic, .utc, .utd, .ute, .uti, .utm, .utp, .uts, .utt, .utw)

**Response:**
```json
{
  "converted_data": {
    "field1": "value1",
    "field2": 123,
    "field3": 45.67
  }
}
```

**Status Codes:**
- `200 OK` - Conversion successful
- `400 Bad Request` - Invalid file format or missing file
- `413 Payload Too Large` - File exceeds 10MB limit
- `500 Internal Server Error` - Server error during conversion

**Example (cURL):**
```bash
curl -X POST -F "file=@example.gff" http://localhost:8080/api/v1/convert/gff-to-json
```

---

### Convert JSON to GFF
Convert a JSON file to GFF format.

**Endpoint:** `POST /api/v1/convert/json-to-gff`

**Content-Type:** `multipart/form-data`

**Parameters:**
- `file` (required) - JSON file to convert (.json)

**Response:** Binary GFF file (download)

**Headers:**
- `Content-Disposition: attachment; filename="converted.gff"`
- `Content-Type: application/octet-stream`

**Status Codes:**
- `200 OK` - Conversion successful
- `400 Bad Request` - Invalid JSON format or missing file
- `500 Internal Server Error` - Server error during conversion

**Example (cURL):**
```bash
curl -X POST -F "file=@example.json" http://localhost:8080/api/v1/convert/json-to-gff -o converted.gff
```

---

### Embed SQLite Database
Embed a SQLite database into a GFF file.

**Endpoint:** `POST /api/v1/convert/sqlite-embed`

**Content-Type:** `multipart/form-data`

**Parameters:**
- `gff_file` (required) - GFF file to embed into (.gff, .bic, etc.)
- `sqlite_file` (required) - SQLite database file (.db, .sqlite)

**Response:** Binary GFF file with embedded SQLite (download)

**Status Codes:**
- `200 OK` - Embedding successful
- `400 Bad Request` - Invalid file format or missing files
- `501 Not Implemented` - Feature not yet implemented
- `500 Internal Server Error` - Server error during embedding

**Example (cURL):**
```bash
curl -X POST -F "gff_file=@example.gff" -F "sqlite_file=@data.db" http://localhost:8080/api/v1/convert/sqlite-embed -o embedded.gff
```

---

### Extract SQLite Database
Extract a SQLite database from a GFF file.

**Endpoint:** `POST /api/v1/convert/sqlite-extract`

**Content-Type:** `multipart/form-data`

**Parameters:**
- `file` (required) - GFF file containing embedded SQLite

**Response:** SQLite database file (download)

**Status Codes:**
- `200 OK` - Extraction successful
- `400 Bad Request` - Invalid file format or missing file
- `501 Not Implemented` - Feature not yet implemented
- `500 Internal Server Error` - Server error during extraction

**Example (cURL):**
```bash
curl -X POST -F "file=@embedded.gff" http://localhost:8080/api/v1/convert/sqlite-extract -o extracted.db
```

---

## Error Responses
All endpoints return consistent error responses:

```json
{
  "error": "Error message describing what went wrong",
  "status": 400
}
```

## Rate Limiting
Currently, there are no rate limits implemented. Future versions may include rate limiting.

## File Size Limits
- Maximum file size: 10MB per file
- This limit applies to all uploaded files

## Supported File Formats

### Input Formats
- GFF files: `.gff`, `.bic`, `.utc`, `.utd`, `.ute`, `.uti`, `.utm`, `.utp`, `.uts`, `.utt`, `.utw`
- JSON files: `.json`
- SQLite databases: `.db`, `.sqlite`

### Output Formats
- JSON responses for data conversion
- Binary GFF files for GFF conversion
- Binary SQLite files for database extraction

## Development and Testing

### Running the Server
```bash
# Install Python dependencies
pip install -r requirements.txt

# Run the server
python main.py
```

### Testing with Sample Files
Create a sample JSON file for testing:
```json
{
  "Test": "Hello World",
  "Version": 1,
  "Data": {
    "field1": "value1",
    "field2": 42
  }
}
```

## Known Limitations
- SQLite embedding/extraction is not yet fully implemented (returns 501 Not Implemented)
- GFF reading/writing uses stub implementations for demonstration
- No authentication or authorization
- No rate limiting
- Basic error handling only

## Future Enhancements
- Full SQLite embedding/extraction implementation
- Authentication and API keys
- Rate limiting
- Batch processing endpoints
- WebSocket support for real-time conversions
- Comprehensive logging and monitoring
- Docker containerization