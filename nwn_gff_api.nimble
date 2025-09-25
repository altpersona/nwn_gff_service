# Package

version       = "0.1.0"
author        = "NWN GFF API Developer"
description   = "HTTP API service for NWN GFF file conversion"
license       = "MIT"
srcDir        = "."
bin           = @["gff_api"]


# Dependencies

requires "nim >= 1.6.0"
requires "prologue >= 0.6.0"
requires "zippy >= 0.10.0"

# Task definitions

task test, "Run tests":
  exec "nim c -r tests/test_api.nim"

task dev, "Development mode":
  exec "nim c -r --hotReload:on gff_api.nim"

task release, "Build release version":
  exec "nim c -d:release gff_api.nim"