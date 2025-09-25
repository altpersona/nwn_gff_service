"""API endpoints for GFF conversion service"""
from typing import Dict, Any
from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from fastapi.responses import JSONResponse, Response
import json
import os

from ..services.gff_parser import GffParser, GffParserError
from ..services.gff_converter import GffConverter, GffConverterError
from ..services.sqlite_handler import SqliteHandler, SqliteHandlerError
from ..models.gff_models import SUPPORTED_FORMATS


router = APIRouter()
gff_parser = GffParser()
gff_converter = GffConverter()
sqlite_handler = SqliteHandler()

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB


@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "ok",
        "service": "nwn-gff-api",
        "version": "0.1.0"
    }


@router.post("/convert/gff-to-json")
async def gff_to_json(file: UploadFile = File(...)):
    """Convert GFF file to JSON format"""
    try:
        # Validate file format
        file_ext = os.path.splitext(file.filename)[1].lower().lstrip('.')
        if file_ext not in SUPPORTED_FORMATS["gff"]:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid file format. Expected GFF file, got: {file_ext}"
            )
        
        # Read file content
        content = await file.read()
        if len(content) > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=413,
                detail="File too large (max 10MB)"
            )
        
        # Parse GFF
        gff_root = gff_parser.read_gff_root(content, validate=True)
        
        # Convert to JSON
        json_data = gff_converter.to_json(gff_root)
        
        # Post-process (sort fields)
        json_data = gff_converter.post_process_json(json_data)
        
        return json_data
        
    except GffParserError as e:
        raise HTTPException(status_code=400, detail=f"Failed to parse GFF file: {str(e)}")
    except GffConverterError as e:
        raise HTTPException(status_code=500, detail=f"Conversion failed: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.post("/convert/json-to-gff")
async def json_to_gff(file: UploadFile = File(...)):
    """Convert JSON file to GFF format"""
    try:
        # Validate file format
        file_ext = os.path.splitext(file.filename)[1].lower().lstrip('.')
        if file_ext != "json":
            raise HTTPException(
                status_code=400,
                detail=f"Invalid file format. Expected JSON file, got: {file_ext}"
            )
        
        # Read and parse JSON
        content = await file.read()
        if len(content) > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=413,
                detail="File too large (max 10MB)"
            )
        
        try:
            json_data = json.loads(content.decode('utf-8'))
        except json.JSONDecodeError as e:
            raise HTTPException(status_code=400, detail="Invalid JSON format")
        
        # Convert to GFF
        gff_root = gff_converter.gff_root_from_json(json_data)
        
        # Write to GFF format
        gff_data = gff_parser.write_gff_root(gff_root)
        
        # Return as downloadable file
        return Response(
            content=gff_data,
            media_type="application/octet-stream",
            headers={
                "Content-Disposition": 'attachment; filename="converted.gff"'
            }
        )
        
    except GffConverterError as e:
        raise HTTPException(status_code=400, detail=f"Conversion failed: {str(e)}")
    except GffParserError as e:
        raise HTTPException(status_code=500, detail=f"Failed to write GFF: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.post("/convert/sqlite-embed")
async def sqlite_embed(
    gff_file: UploadFile = File(...),
    sqlite_file: UploadFile = File(...)
):
    """Embed SQLite database into GFF file"""
    try:
        # Validate file formats
        gff_ext = os.path.splitext(gff_file.filename)[1].lower().lstrip('.')
        if gff_ext not in SUPPORTED_FORMATS["gff"]:
            raise HTTPException(status_code=400, detail="Invalid GFF file format")
        
        sqlite_ext = os.path.splitext(sqlite_file.filename)[1].lower().lstrip('.')
        if sqlite_ext not in ["db", "sqlite"]:
            raise HTTPException(status_code=400, detail="Invalid SQLite file format")
        
        # Read files
        gff_content = await gff_file.read()
        sqlite_content = await sqlite_file.read()
        
        if len(gff_content) > MAX_FILE_SIZE or len(sqlite_content) > MAX_FILE_SIZE:
            raise HTTPException(status_code=413, detail="Files too large (max 10MB each)")
        
        # Embed SQLite
        embedded_data = sqlite_handler.embed_sqlite(gff_content, sqlite_content)
        
        # Return as downloadable file
        return Response(
            content=embedded_data,
            media_type="application/octet-stream",
            headers={
                "Content-Disposition": 'attachment; filename="embedded.gff"'
            }
        )
        
    except SqliteHandlerError as e:
        raise HTTPException(status_code=500, detail=f"SQLite embedding failed: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.post("/convert/sqlite-extract")
async def sqlite_extract(file: UploadFile = File(...)):
    """Extract SQLite database from GFF file"""
    try:
        # Validate file format
        file_ext = os.path.splitext(file.filename)[1].lower().lstrip('.')
        if file_ext not in SUPPORTED_FORMATS["gff"]:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid file format. Expected GFF file, got: {file_ext}"
            )
        
        # Read file
        content = await file.read()
        if len(content) > MAX_FILE_SIZE:
            raise HTTPException(status_code=413, detail="File too large (max 10MB)")
        
        # Extract SQLite
        sqlite_data = sqlite_handler.extract_sqlite(content)
        if sqlite_data is None:
            raise HTTPException(
                status_code=400,
                detail="No SQLite database found in GFF file"
            )
        
        # Return as downloadable file
        return Response(
            content=sqlite_data,
            media_type="application/octet-stream",
            headers={
                "Content-Disposition": 'attachment; filename="extracted.db"'
            }
        )
        
    except SqliteHandlerError as e:
        raise HTTPException(status_code=500, detail=f"SQLite extraction failed: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/")
async def api_info():
    """API information endpoint"""
    return {
        "message": "NWN GFF API Service",
        "version": "0.1.0",
        "endpoints": [
            "GET /api/v1/health",
            "POST /api/v1/convert/gff-to-json",
            "POST /api/v1/convert/json-to-gff",
            "POST /api/v1/convert/sqlite-embed",
            "POST /api/v1/convert/sqlite-extract"
        ]
    }