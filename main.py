#!/usr/bin/env python3
"""Entry point for the NWN GFF API Service"""
import uvicorn
from app.main import app


if __name__ == "__main__":
    print("Starting NWN GFF API Service on port 8000...")
    print("API documentation available at: http://localhost:8000/docs")
    print("Health check: http://localhost:8000/api/v1/health")
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )