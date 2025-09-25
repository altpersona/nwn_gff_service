# NWN GFF API Service Development Notes

## Project Overview
Converting the existing command-line NWN GFF tool to an HTTP API service.

## Architecture Decisions

### 1. Framework Choice
- **Decision**: Use Prologue framework for HTTP API
- **Rationale**: Prologue is a modern, lightweight web framework for Nim with good async support and JSON handling

### 2. API Design
- **Base URL**: `http://localhost:8080/api/v1`
- **Endpoints**:
  - `POST /convert/gff-to-json` - Convert GFF to JSON
  - `POST /convert/json-to-gff` - Convert JSON to GFF
  - `POST /convert/sqlite-embed` - Embed SQLite data into GFF
  - `POST /convert/sqlite-extract` - Extract SQLite from GFF

### 3. Missing Shared Module Analysis
Based on the original code, the `shared` module likely contains:
- `ensureValidFormat` - Validates input/output format based on file extension
- `GffRoot` type - Main data structure for GFF files
- `GffExtensions` - Array of supported GFF file extensions
- `readGffRoot` - Function to read GFF from stream
- `gffRootFromJson` - Function to create GffRoot from JSON
- `toJson` - Function to convert GffRoot to JSON
- GFF data type definitions (GffStruct, GffVoid, GffDword, etc.)

### 4. Data Flow
1. Client sends file/data via POST request
2. Server validates format and processes conversion
3. Server returns converted data or error message

### 5. Error Handling Strategy
- Return appropriate HTTP status codes (400 for bad requests, 500 for server errors)
- Provide detailed error messages in JSON format
- Validate file formats and sizes

### 6. Version History
- v0.1.0: Initial API implementation with basic conversion endpoints
- v0.2.0: Added SQLite embedding/extraction functionality
- v0.3.0: Enhanced error handling and validation

## Development Steps
1. Create shared module with GFF functionality
2. Implement HTTP server with Prologue
3. Add conversion endpoints
4. Add SQLite functionality
5. Add comprehensive error handling
6. Create API documentation