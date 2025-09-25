# NWN GFF API Service - Python FastAPI Implementation

A Python FastAPI service for converting between NWN (Neverwinter Nights) GFF (Game File Format) and JSON formats, with support for SQLite database embedding and extraction.

## Features

- **GFF to JSON Conversion**: Convert GFF files to JSON format
- **JSON to GFF Conversion**: Convert JSON files back to GFF format
- **SQLite Support**: Embed and extract SQLite databases from GFF files
- **RESTful API**: Clean, well-documented HTTP endpoints
- **File Upload/Download**: Support for file uploads and downloads
- **Error Handling**: Comprehensive error responses with proper HTTP status codes
- **CORS Support**: Cross-origin resource sharing enabled
- **Docker Support**: Containerized deployment ready

## Requirements

- Python 3.8+
- No external runtime dependencies (all included in requirements.txt)

## Quick Start

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/altpersona/nwn_gff_service.git
   cd nwn_gff_service
   ```

2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the API server:
   ```bash
   python main.py
   ```

The server will start on port 8000. You can access the API at `http://localhost:8000`.

### Testing with Docker

1. Build and run with Docker:
   ```bash
   docker-compose up --build
   ```

2. Or build manually:
   ```bash
   docker build -t nwn-gff-api .
   docker run -p 8000:8000 nwn-gff-api
   ```

## API Endpoints

### Health Check
- `GET /api/v1/health` - Check if the service is running

### Conversion Endpoints
- `POST /api/v1/convert/gff-to-json` - Convert GFF file to JSON
- `POST /api/v1/convert/json-to-gff` - Convert JSON file to GFF
- `POST /api/v1/convert/sqlite-embed` - Embed SQLite into GFF file
- `POST /api/v1/convert/sqlite-extract` - Extract SQLite from GFF file

### Base Endpoint
- `GET /api/v1/` - API information and available endpoints

## Usage Examples

### Convert GFF to JSON
```bash
curl -X POST -F "file=@example.gff" http://localhost:8000/api/v1/convert/gff-to-json
```

### Convert JSON to GFF
```bash
curl -X POST -F "file=@example.json" http://localhost:8000/api/v1/convert/json-to-gff -o converted.gff
```

### Check API Health
```bash
curl http://localhost:8000/api/v1/health
```

## Testing

Run the test suite:
```bash
pytest tests/
```

Run with coverage:
```bash
pytest tests/ --cov=app --cov-report=html
```

Test web interface integration:
```bash
python3 test_web_integration.py
```

## File Structure

```
.
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application
│   ├── models/
│   │   ├── __init__.py
│   │   └── gff_models.py      # GFF data structures
│   ├── services/
│   │   ├── __init__.py
│   │   ├── gff_parser.py      # GFF binary parsing
│   │   ├── gff_converter.py   # GFF/JSON conversion
│   │   └── sqlite_handler.py  # SQLite handling
│   └── api/
│       ├── __init__.py
│       └── endpoints.py       # API endpoints
├── tests/
│   ├── __init__.py
│   └── test_api.py           # API tests
├── Dockerfile
├── docker-compose.yml
├── main.py                   # Entry point
├── requirements.txt          # Python dependencies
├── web_interface.html        # HTML/JavaScript web interface
├── WEB_INTERFACE_GUIDE.md    # Web interface integration guide
├── test_web_integration.py   # Web interface testing script
```

## Configuration

The API server runs on port 8000 by default. You can modify this by setting the `PORT` environment variable:

```bash
PORT=8080 python main.py
```

## Supported File Formats

### Input Formats
- GFF files: `.gff`, `.bic`, `.utc`, `.utd`, `.ute`, `.uti`, `.utm`, `.utp`, `.uts`, `.utt`, `.utw`
- JSON files: `.json`
- SQLite databases: `.db`, `.sqlite`

### File Size Limits
- Maximum file size: 10MB per file

## Development

### Development Mode
Run the server in development mode with auto-reload:
```bash
python main.py
```

### Building for Production
```bash
docker build -t nwn-gff-api .
```

## Web Interface Integration

This service includes a complete HTML/JavaScript web interface (`web_interface.html`) that demonstrates how a webpage can interact with the API for file conversions.

### Features:
- **Drag-and-drop file selection**
- **Real-time conversion status**
- **Automatic file downloads**
- **API health monitoring**
- **Responsive design**

### Using the Web Interface:

1. **Open the web interface**:
   ```bash
   # The API service must be running
   python main.py
   
   # Open in browser
   # On macOS:
   open web_interface.html
   
   # On Linux:
   xdg-open web_interface.html
   
   # On Windows:
   start web_interface.html
   ```

2. **Use the interface**:
   - Select a file using the file picker or drag-and-drop
   - Click conversion buttons (GFF→JSON or JSON→GFF)
   - Download converted files automatically

### Web Interface Documentation:
- **Complete guide**: See `WEB_INTERFACE_GUIDE.md` for detailed integration instructions
- **JavaScript examples**: Full code examples for button handlers, error handling, and API interaction
- **CORS configuration**: Pre-configured to work with any origin for easy integration

### Example JavaScript Integration:
```javascript
// Convert JSON to GFF
async function convertJsonToGff() {
    const fileInput = document.getElementById('jsonFile');
    const file = fileInput.files[0];
    
    const formData = new FormData();
    formData.append('file', file);
    
    const response = await fetch('http://localhost:8000/api/v1/convert/json-to-gff', {
        method: 'POST',
        body: formData
    });
    
    if (response.ok) {
        const blob = await response.blob();
        // Create download link and trigger download
        const downloadUrl = URL.createObjectURL(blob);
        const downloadLink = document.createElement('a');
        downloadLink.href = downloadUrl;
        downloadLink.download = file.name.replace('.json', '.gff');
        downloadLink.click();
    }
}
```

### Testing the Web Interface:
```bash
# Run the web interface test
python3 test_web_integration.py
```

## Error Handling

All endpoints return consistent error responses:

```json
{
  "detail": "Descriptive error message"
}
```

Common status codes:
- `200 OK` - Success
- `400 Bad Request` - Invalid request or file format
- `413 Payload Too Large` - File exceeds size limit
- `500 Internal Server Error` - Server-side error

## Known Limitations

- GFF binary parsing uses simplified stub implementation
- Full binary format implementation would require complete reverse engineering
- SQLite functionality uses zlib compression instead of Zstd
- Basic error handling only

## Development Notes

This is a Python rewrite of the original Nim implementation. The binary parsing logic is simplified but maintains the same API interface. For production use, the full GFF binary format specification would need to be implemented.

## Contributing

1. Fork the project
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## Support

For issues and questions, please refer to the API documentation or check the main repository.

# I do not own any of the core code, that is all https://github.com/niv and some unknowable group of contributors.
