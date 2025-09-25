import prologue, json, strutils, os, streams, tables
import shared

# Configuration
const API_VERSION = "/api/v1"
const MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB max file size

# Error response helper
proc errorResponse*(ctx: Context, status: int, message: string) {.async.} =
  resp jsonResponse(%*{
    "error": message,
    "status": status
  }, status)

# Health check endpoint
proc healthCheck*(ctx: Context) {.async.} =
  resp jsonResponse(%*{
    "status": "ok",
    "service": "nwn-gff-api",
    "version": "0.1.0"
  })

# GFF to JSON conversion endpoint
proc gffToJson*(ctx: Context) {.async.} =
  try:
    # Check if file was uploaded
    if not ctx.hasFormData("file"):
      await errorResponse(ctx, 400, "No file uploaded")
      return
    
    let uploadedFile = ctx.getFormData("file")
    if uploadedFile.filename == "":
      await errorResponse(ctx, 400, "No file selected")
      return
    
    # Check file size
    if uploadedFile.content.len > MAX_FILE_SIZE:
      await errorResponse(ctx, 413, "File too large (max 10MB)")
      return
    
    # Check file extension
    let ext = splitFile(uploadedFile.filename).ext.toLower
    if ext notin [".gff", ".bic", ".utc", ".utd", ".ute", ".uti", ".utm", ".utp", ".uts", ".utt", ".utw"]:
      await errorResponse(ctx, 400, "Invalid file format. Expected GFF file")
      return
    
    # Create input stream from uploaded content
    let inputStream = newStringStream(uploadedFile.content)
    if inputStream.isNil:
      await errorResponse(ctx, 500, "Failed to create input stream")
      return
    
    # Read GFF data
    var gffRoot: GffRoot
    try:
      gffRoot = inputStream.readGffRoot(false)
    except:
      await errorResponse(ctx, 400, "Failed to parse GFF file")
      inputStream.close()
      return
    
    inputStream.close()
    
    # Convert to JSON
    let jsonData = gffRoot.toJson()
    
    # Return JSON response
    resp jsonResponse(jsonData)
    
  except:
    await errorResponse(ctx, 500, "Internal server error")

# JSON to GFF conversion endpoint
proc jsonToGff*(ctx: Context) {.async.} =
  try:
    # Check if file was uploaded
    if not ctx.hasFormData("file"):
      await errorResponse(ctx, 400, "No file uploaded")
      return
    
    let uploadedFile = ctx.getFormData("file")
    if uploadedFile.filename == "":
      await errorResponse(ctx, 400, "No file selected")
      return
    
    # Check file extension
    let ext = splitFile(uploadedFile.filename).ext.toLower
    if ext != ".json":
      await errorResponse(ctx, 400, "Invalid file format. Expected JSON file")
      return
    
    # Parse JSON
    var jsonData: JsonNode
    try:
      jsonData = parseJson(uploadedFile.content)
    except:
      await errorResponse(ctx, 400, "Invalid JSON format")
      return
    
    # Convert to GFF
    var gffRoot: GffRoot
    try:
      gffRoot = jsonData.gffRootFromJson()
    except:
      await errorResponse(ctx, 400, "Failed to convert JSON to GFF format")
      return
    
    # Create output stream
    let outputStream = newStringStream()
    if outputStream.isNil:
      await errorResponse(ctx, 500, "Failed to create output stream")
      return
    
    # Write GFF data
    try:
      outputStream.write(gffRoot)
    except:
      await errorResponse(ctx, 500, "Failed to write GFF data")
      outputStream.close()
      return
    
    # Get the GFF content
    let gffContent = outputStream.data
    outputStream.close()
    
    # Return GFF file as download
    ctx.response.setHeader("Content-Disposition", "attachment; filename=\"converted.gff\"")
    ctx.response.setHeader("Content-Type", "application/octet-stream")
    resp gffContent
    
  except:
    await errorResponse(ctx, 500, "Internal server error")

# SQLite embedding endpoint
proc sqliteEmbed*(ctx: Context) {.async.} =
  try:
    # Check if both GFF and SQLite files were uploaded
    if not ctx.hasFormData("gff_file") or not ctx.hasFormData("sqlite_file"):
      await errorResponse(ctx, 400, "Both GFF and SQLite files are required")
      return
    
    let gffFile = ctx.getFormData("gff_file")
    let sqliteFile = ctx.getFormData("sqlite_file")
    
    if gffFile.filename == "" or sqliteFile.filename == "":
      await errorResponse(ctx, 400, "Both files must be selected")
      return
    
    # Check file extensions
    let gffExt = splitFile(gffFile.filename).ext.toLower
    let sqliteExt = splitFile(sqliteFile.filename).ext.toLower
    
    if gffExt notin [".gff", ".bic", ".utc", ".utd", ".ute", ".uti", ".utm", ".utp", ".uts", ".utt", ".utw"]:
      await errorResponse(ctx, 400, "Invalid GFF file format")
      return
    
    if sqliteExt != ".db" and sqliteExt != ".sqlite":
      await errorResponse(ctx, 400, "Invalid SQLite file format")
      return
    
    # This is a stub implementation - would need real SQLite compression logic
    await errorResponse(ctx, 501, "SQLite embedding not yet implemented")
    
  except:
    await errorResponse(ctx, 500, "Internal server error")

# SQLite extraction endpoint
proc sqliteExtract*(ctx: Context) {.async.} =
  try:
    # Check if file was uploaded
    if not ctx.hasFormData("file"):
      await errorResponse(ctx, 400, "No file uploaded")
      return
    
    let uploadedFile = ctx.getFormData("file")
    if uploadedFile.filename == "":
      await errorResponse(ctx, 400, "No file selected")
      return
    
    # Check file extension
    let ext = splitFile(uploadedFile.filename).ext.toLower
    if ext notin [".gff", ".bic", ".utc", ".utd", ".ute", ".uti", ".utm", ".utp", ".uts", ".utt", ".utw"]:
      await errorResponse(ctx, 400, "Invalid file format. Expected GFF file")
      return
    
    # This is a stub implementation - would need real SQLite extraction logic
    await errorResponse(ctx, 501, "SQLite extraction not yet implemented")
    
  except:
    await errorResponse(ctx, 500, "Internal server error")

# Main application
proc main() =
  var app = newApp()
  
  # Note: CORS middleware not available in this Prologue version
  # app.use(cors())
  
  # Define routes
  app.get(API_VERSION & "/health", healthCheck)
  app.post(API_VERSION & "/convert/gff-to-json", gffToJson)
  app.post(API_VERSION & "/convert/json-to-gff", jsonToGff)
  app.post(API_VERSION & "/convert/sqlite-embed", sqliteEmbed)
  app.post(API_VERSION & "/convert/sqlite-extract", sqliteExtract)
  
  # Default route
  app.get("/", proc(ctx: Context) {.async.} =
    resp jsonResponse(%*{
      "message": "NWN GFF API Service",
      "version": "0.1.0",
      "endpoints": [
        "GET /api/v1/health",
        "POST /api/v1/convert/gff-to-json",
        "POST /api/v1/convert/json-to-gff",
        "POST /api/v1/convert/sqlite-embed",
        "POST /api/v1/convert/sqlite-extract"
      ]
    })
  )
  
  # Configure and run server
  let settings = newSettings(
    port = 8080,
    debug = true,
    appName = "NWN GFF API"
  )
  
  echo "Starting NWN GFF API server on port 8080..."
  echo "API documentation available at http://localhost:8080/"
  app.run(settings)

when isMainModule:
  main()