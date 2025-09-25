# NWN GFF API Service

An HTTP API service for converting between NWN (Neverwinter Nights) GFF (Game File Format) and JSON formats, with support for SQLite database embedding and extraction.

## Features

- **GFF to JSON Conversion**: Convert GFF files to JSON format
- **JSON to GFF Conversion**: Convert JSON files back to GFF format
- **SQLite Support**: Embed and extract SQLite databases from GFF files
- **RESTful API**: Clean, well-documented HTTP endpoints
- **File Upload/Download**: Support for file uploads and downloads
- **Error Handling**: Comprehensive error responses with proper HTTP status codes
- **CORS Support**: Cross-origin resource sharing enabled

## Quick Start

### Prerequisites

- Nim >= 1.6.0 (the programming language, not the R package)
- Nimble package manager (Nim's package manager)

### Installation

**Important Note**: This project uses the **Nim programming language** (https://nim-lang.org), not the R package called "nimble". These are completely different technologies.

1. Install Nim and Nimble:
   ```bash
   # On Ubuntu/Debian:
   sudo apt install nim
   
   # On macOS:
   brew install nim
   
   # Or download from https://nim-lang.org/install.html
   ```

2. Clone or download the project files
3. Install dependencies:
   ```bash
   nimble install -d
   ```
4. Build and run the API server:
   ```bash
   nim c -r gff_api.nim
   ```

The server will start on port 8080. You can access the API at `http://localhost:8080/api/v1`.

### Testing the API

Run the test suite to verify everything is working:
```bash
nim c -r test_api.nim
```

**Note**: This project requires the Nim programming language runtime to be installed on your system.

## API Endpoints

### Health Check
- `GET /api/v1/health` - Check if the service is running

### Conversion Endpoints
- `POST /api/v1/convert/gff-to-json` - Convert GFF file to JSON
- `POST /api/v1/convert/json-to-gff` - Convert JSON file to GFF
- `POST /api/v1/convert/sqlite-embed` - Embed SQLite into GFF file
- `POST /api/v1/convert/sqlite-extract` - Extract SQLite from GFF file

### Base Endpoint
- `GET /` - API information and available endpoints

## Usage Examples

### Convert GFF to JSON
```bash
curl -X POST -F "file=@example.gff" http://localhost:8080/api/v1/convert/gff-to-json
```

### Convert JSON to GFF
```bash
curl -X POST -F "file=@example.json" http://localhost:8080/api/v1/convert/json-to-gff -o converted.gff
```

### Check API Health
```bash
curl http://localhost:8080/api/v1/health
```

## File Structure

```
.
├── gff_api.nim          # Main API server
├── shared.nim           # GFF functionality module
├── nwn_gff_api.nimble  # Project configuration
├── test_api.nim         # Test suite
├── API_DOCUMENTATION.md # Detailed API documentation
├── VERSION_HISTORY.md   # Version history and changelog
├── NOTES.md            # Development notes
└── README.md           # This file
```

## Configuration

The API server runs on port 8080 by default. You can modify this in the [`gff_api.nim`](gff_api.nim:190) file:

```nim
let settings = newSettings(
  port = 8080,
  debug = true,
  appName = "NWN GFF API"
)
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
Run the server in development mode with hot reload:
```bash
nim c -r --hotReload:on gff_api.nim
```

### Building for Production
```bash
nim c -d:release gff_api.nim
```

### Running Tests
```bash
nim c -r test_api.nim
```

## Architecture

The API is built using:
- **Prologue**: Modern Nim web framework
- **Shared Module**: Contains GFF parsing and conversion logic
- **Async/Await**: Non-blocking request handling
- **Multipart Forms**: File upload support

## Error Handling

All endpoints return consistent error responses:

```json
{
  "error": "Descriptive error message",
  "status": 400
}
```

Common status codes:
- `200 OK` - Success
- `400 Bad Request` - Invalid request or file format
- `413 Payload Too Large` - File exceeds size limit
- `500 Internal Server Error` - Server-side error
- `501 Not Implemented` - Feature not yet implemented

## Known Limitations

- SQLite embedding/extraction is stubbed and returns "Not Implemented"
- GFF parsing uses simplified stub implementations
- No authentication or rate limiting
- Basic error handling only

## Future Enhancements

See [VERSION_HISTORY.md](VERSION_HISTORY.md) for planned features and version roadmap.

## Contributing

1. Fork the project
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For issues and questions, please refer to the API documentation or check the development notes in [NOTES.md](NOTES.md).