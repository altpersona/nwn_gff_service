# Version History

## Repository Information
- **GitHub Repository**: https://github.com/altpersona/nwn_gff_service
- **Current Version**: v0.1.0

## v0.1.0 (2025-09-25)
### Initial API Implementation
- Created basic HTTP API server using Prologue framework
- Implemented shared module with GFF functionality stubs
- Added `/api/v1/convert/gff-to-json` endpoint
- Added `/api/v1/convert/json-to-gff` endpoint
- Basic error handling and validation
- Support for file uploads and downloads

### API Endpoints
- `POST /api/v1/convert/gff-to-json` - Convert GFF file to JSON
- `POST /api/v1/convert/json-to-gff` - Convert JSON to GFF file

### Technical Details
- Framework: Prologue (Nim web framework)
- Port: 8080
- Content-Type: multipart/form-data for file uploads
- Response format: JSON with converted data or error messages

### Known Limitations
- SQLite embedding/extraction not yet implemented
- Limited file size validation
- Basic error messages
- No authentication or rate limiting

---

## Planned Features for v0.2.0
- SQLite embedding functionality
- SQLite extraction functionality
- Enhanced error handling
- File size validation
- Better error messages with specific error codes

## Planned Features for v0.3.0
- API documentation with Swagger/OpenAPI
- Health check endpoint
- Configuration file support
- Logging system
- Performance optimizations