# Python FastAPI Conversion Plan for NWN GFF Service

## Overview
Convert the existing Nim GFF service to a Python FastAPI service that can be deployed without requiring Nim runtime dependencies.

## Architecture Decision

### Technology Stack
- **Framework**: FastAPI (Python)
- **Language**: Python 3.8+
- **Binary Parsing**: `struct` module for binary data
- **JSON Handling**: Built-in `json` module
- **SQLite**: `sqlite3` module (standard library)
- **Compression**: `zlib` for compression/decompression
- **Testing**: `pytest` and `httpx` for API testing
- **Deployment**: Docker containerization

### Key Conversions Required

#### 1. GFF Binary Format Analysis
The Nim code shows GFF files have:
- Binary format with specific data types (Byte, Char, Word, Short, Dword, Int, Float, Struct, String, ResRef, Void)
- Header structure
- Field definitions
- SQLite embedding capability

#### 2. Data Structure Mapping
```python
# Nim to Python data structure mapping
Nim GffField -> Python GffField (dataclass)
Nim GffStruct -> Python GffStruct (dataclass) 
Nim GffRoot -> Python GffRoot (dataclass)
Nim Table -> Python dict
```

#### 3. Binary Parsing Logic
- Implement `read_gff_root()` function
- Handle endianness (likely little-endian)
- Parse header and validate format
- Read structs and fields recursively
- Handle different data type sizes

#### 4. JSON Conversion Logic
- Implement `to_json()` method for GffRoot
- Implement `gff_root_from_json()` method
- Handle nested structures
- Maintain field ordering

## Implementation Plan

### Phase 1: Core Structure
1. Set up Python project structure
2. Create GFF data classes
3. Implement basic binary reading utilities
4. Set up FastAPI application skeleton

### Phase 2: GFF Parsing
1. Implement GFF header parsing
2. Create struct parsing logic
3. Handle different data types
4. Add validation and error handling

### Phase 3: JSON Integration
1. Implement GFF to JSON conversion
2. Implement JSON to GFF conversion
3. Add JSON post-processing (sorting)

### Phase 4: SQLite Functionality
1. Implement SQLite embedding
2. Implement SQLite extraction
3. Add compression/decompression

### Phase 5: API Endpoints
1. Create file upload endpoints
2. Implement conversion endpoints
3. Add error handling and validation
4. Create health check endpoint

### Phase 6: Testing & Documentation
1. Write comprehensive tests
2. Create API documentation
3. Add deployment configuration
4. Update Git repository

## File Structure
```
nwn_gff_service/
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
│   │   └── sqlite_handler.py  # SQLite embedding/extraction
│   └── api/
│       ├── __init__.py
│       └── endpoints.py       # API endpoints
├── tests/
│   ├── __init__.py
│   ├── test_gff_parser.py
│   ├── test_conversion.py
│   └── test_api.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── README.md
└── .gitignore
```

## API Endpoints (Same as Nim version)
- `POST /api/v1/convert/gff-to-json`
- `POST /api/v1/convert/json-to-gff`
- `POST /api/v1/convert/sqlite-embed`
- `POST /api/v1/convert/sqlite-extract`
- `GET /api/v1/health`

## Deployment Strategy
1. Docker containerization for easy deployment
2. No external runtime dependencies
3. Self-contained binary parsing
4. Environment variable configuration

## Testing Strategy
1. Unit tests for individual components
2. Integration tests for API endpoints
3. Binary file format validation
4. Round-trip conversion testing

## Risk Mitigation
1. Maintain compatibility with existing GFF files
2. Handle edge cases in binary parsing
3. Validate JSON output format
4. Implement proper error handling
5. Add comprehensive logging

## Success Criteria
1. API works without Nim runtime
2. Maintains same functionality as Nim version
3. Handles all supported file formats
4. Passes comprehensive test suite
5. Ready for production deployment