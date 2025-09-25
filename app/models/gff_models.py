"""GFF data models based on the Nim implementation"""
from dataclasses import dataclass
from typing import Dict, List, Optional, Union
from enum import Enum


class GffDataType(Enum):
    """GFF data types based on Nim implementation"""
    GFF_BYTE = 0
    GFF_CHAR = 1
    GFF_WORD = 2
    GFF_SHORT = 3
    GFF_DWORD = 4
    GFF_INT = 5
    GFF_FLOAT = 8
    GFF_STRUCT = 13
    GFF_STRING = 14
    GFF_RESREF = 15
    GFF_VOID = 17


@dataclass
class GffField:
    """Represents a single GFF field with its data"""
    kind: GffDataType
    bval: Optional[int] = None      # uint8
    cval: Optional[str] = None      # char
    wval: Optional[int] = None      # uint16
    sval: Optional[int] = None      # int16
    dval: Optional[int] = None      # uint32
    ival: Optional[int] = None      # int32
    fval: Optional[float] = None    # float32
    structval: Optional['GffStruct'] = None  # Nested struct
    strval: Optional[str] = None    # string
    resval: Optional[str] = None    # resref
    voidval: Optional[bytes] = None  # void (binary data)


@dataclass
class GffStruct:
    """Represents a GFF structure containing fields"""
    id: int  # uint32
    fields: Dict[str, GffField]


@dataclass
class GffRoot:
    """Root container for GFF data"""
    structs: List[GffStruct]
    top_level_struct: GffStruct


# Supported file extensions
GFF_EXTENSIONS = [
    "gff", "bic", "utc", "utd", "ute", "uti", "utm", "utp", "uts", "utt", "utw"
]

SUPPORTED_FORMATS = {
    "json": ["json"],
    "gff": GFF_EXTENSIONS
}