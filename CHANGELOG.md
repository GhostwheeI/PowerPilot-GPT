# 📦 Changelog

## [1.1] - 2025-08-04
### Added
- Automatic bearer token generation and storage
- Dynamic `openapi.json` generation using live Ngrok URL
- Log rotation at 30MB per file with `.gz` compression
- Rolling log retention limit (max 50MB total)
- Full stdout/stderr logging of PowerShell execution
- Timeout handling for long-running commands
- Temp script syntax validation (`Set-StrictMode`)
- Endpoint `ping` health check

### Changed
- Improved script cleanup (temp `.ps1` deletion)
- Instructions for GPT include stricter execution behavior
- PowerShell scripts now run via absolute paths
- Switched from static to dynamic schema generation

### Fixed
- "Not recognized as a cmdlet" issue due to relative paths
- Missing output/logs from subprocess
- Error handling when script fails silently
