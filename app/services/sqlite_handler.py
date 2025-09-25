"""SQLite embedding and extraction functionality"""
import zlib
from typing import Optional


class SqliteHandlerError(Exception):
    """Custom exception for SQLite handling errors"""
    pass


class SqliteHandler:
    """Handles SQLite database embedding and extraction"""
    
    def __init__(self):
        self.magic_sqlite = b"SQL3"
        self.compression_level = 6  # Zstd compression level
    
    def embed_sqlite(self, gff_data: bytes, sqlite_data: bytes) -> bytes:
        """Embed SQLite database into GFF data with compression"""
        try:
            # Compress the SQLite data
            compressed_data = zlib.compress(sqlite_data, self.compression_level)
            
            # Add magic header
            embedded_data = self.magic_sqlite + compressed_data
            
            # For now, return simple concatenation
            # In full implementation, this would modify the GFF structure
            return gff_data + embedded_data
            
        except Exception as e:
            raise SqliteHandlerError(f"Failed to embed SQLite: {e}")
    
    def extract_sqlite(self, gff_data: bytes) -> Optional[bytes]:
        """Extract and decompress SQLite database from GFF data"""
        try:
            # Look for magic header
            magic_pos = gff_data.find(self.magic_sqlite)
            if magic_pos == -1:
                return None
            
            # Extract compressed data (skip magic header)
            compressed_data = gff_data[magic_pos + len(self.magic_sqlite):]
            
            # Decompress
            decompressed_data = zlib.decompress(compressed_data)
            
            return decompressed_data
            
        except Exception as e:
            raise SqliteHandlerError(f"Failed to extract SQLite: {e}")
    
    def compress_data(self, data: bytes) -> bytes:
        """Compress data using zlib (equivalent to Zstd in Nim version)"""
        try:
            return zlib.compress(data, self.compression_level)
        except Exception as e:
            raise SqliteHandlerError(f"Failed to compress data: {e}")
    
    def decompress_data(self, data: bytes) -> bytes:
        """Decompress data using zlib"""
        try:
            return zlib.decompress(data)
        except Exception as e:
            raise SqliteHandlerError(f"Failed to decompress data: {e}")