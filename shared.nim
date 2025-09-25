import json, strutils, tables, streams, algorithm, sequtils, os

# GFF Data Types
type
  GffDataType* = enum
    GffByte = 0
    GffChar = 1
    GffWord = 2
    GffShort = 3
    GffDword = 4
    GffInt = 5
    GffFloat = 8
    GffStruct = 13
    GffString = 14
    GffResRef = 15
    GffVoid = 17

  GffField* = object
    case kind*: GffDataType
    of GffByte: bval*: uint8
    of GffChar: cval*: char
    of GffWord: wval*: uint16
    of GffShort: sval*: int16
    of GffDword: dval*: uint32
    of GffInt: ival*: int32
    of GffFloat: fval*: float32
    of GffStruct: structval*: GffStruct
    of GffString: strval*: string
    of GffResRef: resval*: string
    of GffVoid: voidval*: string


  GffRoot* = object
    structs*: seq[GffStruct]
    topLevelStruct*: GffStruct

# Constants
const GffExtensions* = @["gff", "bic", "utc", "utd", "ute", "uti", "utm", "utp", "uts", "utt", "utw"]

# Helper functions for creating GFF fields
proc GffByte*(val: uint8): GffField = GffField(kind: GffByte, bval: val)
proc GffChar*(val: char): GffField = GffField(kind: GffChar, cval: val)
proc GffWord*(val: uint16): GffField = GffField(kind: GffWord, wval: val)
proc GffShort*(val: int16): GffField = GffField(kind: GffShort, sval: val)
proc GffDword*(val: uint32): GffField = GffField(kind: GffDword, dval: val)
proc GffInt*(val: int32): GffField = GffField(kind: GffInt, ival: val)
proc GffFloat*(val: float32): GffField = GffField(kind: GffFloat, fval: val)
proc GffStruct*(val: GffStruct): GffField = GffField(kind: GffStruct, structval: val)
proc GffString*(val: string): GffField = GffField(kind: GffString, strval: val)
proc GffResRef*(val: string): GffField = GffField(kind: GffResRef, resval: val)
proc GffVoid*(val: string): GffField = GffField(kind: GffVoid, voidval: val)

# Helper functions for creating GFF structs
proc newGffStruct*(id: uint32 = 0): GffStruct =
  result = GffStruct(id: id, fields: initTable[string, GffField]())

# GffRoot field access
proc hasField*(root: GffRoot, name: string, kind: GffDataType): bool =
  result = root.topLevelStruct.fields.hasKey(name) and root.topLevelStruct.fields[name].kind == kind

proc `[]`*(root: GffRoot, name: string, kind: GffDataType): GffField =
  if not root.hasField(name, kind):
    raise newException(KeyError, "Field not found: " & name)
  result = root.topLevelStruct.fields[name]

proc `[]=`*(root: var GffRoot, name: string, kind: GffDataType, value: GffField) =
  root.topLevelStruct.fields[name] = value

# GffStruct field access
proc hasField*(struct: GffStruct, name: string, kind: GffDataType): bool =
  result = struct.fields.hasKey(name) and struct.fields[name].kind == kind

proc `[]`*(struct: GffStruct, name: string, kind: GffDataType): GffField =
  if not struct.hasField(name, kind):
    raise newException(KeyError, "Field not found: " & name)
  result = struct.fields[name]

proc `[]=`*(struct: var GffStruct, name: string, kind: GffDataType, value: GffField) =
  struct.fields[name] = value

# Format validation
proc ensureValidFormat*(format: string, filename: string, supportedFormats: Table[string, seq[string]]): string =
  if format == "autodetect":
    let ext = splitFile(filename).ext.toLower
    if ext.len > 0 and ext[0] == '.':
      let extWithoutDot = ext[1..^1]
      for fmt, exts in supportedFormats:
        if extWithoutDot in exts:
          return fmt
    return "gff"  # default
  else:
    if format in supportedFormats:
      return format
    else:
      raise newException(ValueError, "Unsupported format: " & format)

# JSON conversion helpers
proc gffRootFromJson*(jsonNode: JsonNode): GffRoot =
  ## Stub implementation - would parse JSON and create GffRoot
  result = GffRoot(
    structs: @[],
    topLevelStruct: newGffStruct()
  )
  
  if jsonNode.kind == JObject:
    for key, value in jsonNode.fields:
      # This is a simplified implementation
      # In reality, this would need to handle all GFF data types
      case value.kind
      of JString:
        result.topLevelStruct.fields[key] = GffString(value.str)
      of JInt:
        result.topLevelStruct.fields[key] = GffInt(value.num.int32)
      of JFloat:
        result.topLevelStruct.fields[key] = GffFloat(value.fnum.float32)
      of JBool:
        result.topLevelStruct.fields[key] = GffByte(if value.bval: 1'u8 else: 0'u8)
      else:
        discard

proc toJson*(root: GffRoot): JsonNode =
  ## Convert GffRoot to JSON
  result = newJObject()
  
  # Convert top-level struct to JSON
  for key, field in root.topLevelStruct.fields:
    case field.kind
    of GffString:
      result[key] = %field.strval
    of GffInt:
      result[key] = %field.ival
    of GffFloat:
      result[key] = %field.fval
    of GffByte:
      result[key] = %field.bval
    of GffDword:
      result[key] = %field.dval
    else:
      result[key] = %""  # Default for unsupported types

# GFF reading (stub implementation)
proc readGffRoot*(stream: Stream, validate: bool): GffRoot =
  ## Read GFF data from stream
  ## This is a stub implementation - real implementation would parse binary GFF format
  result = GffRoot(
    structs: @[],
    topLevelStruct: newGffStruct()
  )
  
  # Add some dummy data for testing
  result.topLevelStruct.fields["Test"] = GffString("Hello World")
  result.topLevelStruct.fields["Version"] = GffInt(1)

# GFF writing (stub implementation)
proc write*(stream: Stream, root: GffRoot) =
  ## Write GFF data to stream
  ## This is a stub implementation - real implementation would write binary GFF format
  stream.write("GFF V1.0\n")  # Dummy header
  for key, field in root.topLevelStruct.fields:
    case field.kind
    of GffString:
      stream.write(key & ": " & field.strval & "\n")
    of GffInt:
      stream.write(key & ": " & $field.ival & "\n")
    else:
      stream.write(key & ": [unsupported type]\n")

# Utility functions
proc cmpIgnoreCase*(a, b: string): int =
  cmpIgnoreCase(a, b)

proc makeMagic*(magic: string): string =
  result = magic