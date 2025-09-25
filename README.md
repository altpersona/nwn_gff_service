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
