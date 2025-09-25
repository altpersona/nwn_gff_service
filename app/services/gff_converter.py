"""GFF to JSON conversion logic based on the Nim implementation"""
import json
from typing import Any, Dict, List
from ..models.gff_models import GffDataType, GffField, GffStruct, GffRoot


class GffConverterError(Exception):
    """Custom exception for GFF conversion errors"""
    pass


class GffConverter:
    """Handles conversion between GFF and JSON formats"""
    
    def to_json(self, root: GffRoot) -> Dict[str, Any]:
        """Convert GffRoot to JSON-compatible dictionary"""
        try:
            result = {}
            
            # Convert top-level struct to JSON
            for key, field in root.top_level_struct.fields.items():
                result[key] = self._field_to_json(field)
            
            return result
            
        except Exception as e:
            raise GffConverterError(f"Failed to convert GFF to JSON: {e}")
    
    def _field_to_json(self, field: GffField) -> Any:
        """Convert a single GFF field to JSON value"""
        try:
            if field.kind == GffDataType.GFF_STRING:
                return field.strval or ""
            elif field.kind == GffDataType.GFF_INT:
                return field.ival or 0
            elif field.kind == GffDataType.GFF_FLOAT:
                return field.fval or 0.0
            elif field.kind == GffDataType.GFF_BYTE:
                return field.bval or 0
            elif field.kind == GffDataType.GFF_DWORD:
                return field.dval or 0
            elif field.kind == GffDataType.GFF_STRUCT:
                if field.structval:
                    result = {}
                    for k, v in field.structval.fields.items():
                        result[k] = self._field_to_json(v)
                    return result
                return {}
            elif field.kind == GffDataType.GFF_VOID:
                return field.voidval.decode('latin-1') if field.voidval else ""
            else:
                return ""  # Default for unsupported types
                
        except Exception as e:
            raise GffConverterError(f"Failed to convert field {field}: {e}")
    
    def gff_root_from_json(self, json_data: Dict[str, Any]) -> GffRoot:
        """Create GffRoot from JSON data"""
        try:
            root = GffRoot(
                structs=[],
                top_level_struct=GffStruct(id=0, fields={})
            )
            
            for key, value in json_data.items():
                root.top_level_struct.fields[key] = self._json_to_field(key, value)
            
            return root
            
        except Exception as e:
            raise GffConverterError(f"Failed to convert JSON to GFF: {e}")
    
    def _json_to_field(self, key: str, value: Any) -> GffField:
        """Convert JSON value to GFF field"""
        try:
            if isinstance(value, str):
                return GffField(kind=GffDataType.GFF_STRING, strval=value)
            elif isinstance(value, int):
                return GffField(kind=GffDataType.GFF_INT, ival=value)
            elif isinstance(value, float):
                return GffField(kind=GffDataType.GFF_FLOAT, fval=value)
            elif isinstance(value, bool):
                return GffField(kind=GffDataType.GFF_BYTE, bval=1 if value else 0)
            elif isinstance(value, dict):
                struct = GffStruct(id=0, fields={})
                for k, v in value.items():
                    struct.fields[k] = self._json_to_field(k, v)
                return GffField(kind=GffDataType.GFF_STRUCT, structval=struct)
            else:
                return GffField(kind=GffDataType.GFF_STRING, strval=str(value))
                
        except Exception as e:
            raise GffConverterError(f"Failed to convert JSON field {key}: {e}")
    
    def post_process_json(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Post-process JSON data - sort fields recursively"""
        try:
            if isinstance(data, dict):
                result = {}
                # Sort keys case-insensitively
                for key in sorted(data.keys(), key=str.lower):
                    result[key] = self.post_process_json(data[key])
                return result
            elif isinstance(data, list):
                return [self.post_process_json(item) for item in data]
            else:
                return data
                
        except Exception as e:
            raise GffConverterError(f"Failed to post-process JSON: {e}")