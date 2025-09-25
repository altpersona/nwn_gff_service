# Git Setup Guide for NWN GFF API Service

## Repository Information
- **GitHub Repository**: https://github.com/altpersona/nwn_gff_service
- **Project**: NWN GFF API Service
- **Language**: Nim (programming language)

## Initial Git Setup

### 1. Initialize Git Repository (if not already done)
```bash
git init
```

### 2. Add Remote Repository
```bash
git remote add origin https://github.com/altpersona/nwn_gff_service.git
```

### 3. Create .gitignore File
Create a `.gitignore` file to exclude build artifacts and temporary files:

```
# Nim build artifacts
nimcache/
*.exe
*.dll
*.so
*.dylib
gff_api

# Test files
test.gff
test.json
converted.gff
extracted.db

# IDE files
.vscode/
.idea/
*.swp
*.swo
*~

# OS files
.DS_Store
Thumbs.db

# Log files
*.log

# Temporary files
*.tmp
*.temp
```

### 4. Initial Commit
```bash
git add .
git commit -m "Initial commit: NWN GFF API Service v0.1.0"
git push -u origin main
```

## Git Workflow

### Feature Development
1. Create a feature branch:
   ```bash
   git checkout -b feature/new-feature-name
   ```

2. Make your changes and commit:
   ```bash
   git add .
   git commit -m "Add new feature: description"
   ```

3. Push to GitHub:
   ```bash
   git push origin feature/new-feature-name
   ```

4. Create a Pull Request on GitHub

### Version Tagging
When releasing new versions:
```bash
git tag -a v0.1.0 -m "Release version 0.1.0"
git push origin v0.1.0
```

## Project Structure for Git
The repository should contain these files:
```
.
├── .gitignore
├── gff_api.nim          # Main API server
├── shared.nim           # GFF functionality module
├── nwn_gff_api.nimble  # Project configuration
├── test_api.nim         # Test suite
├── API_DOCUMENTATION.md # Detailed API documentation
├── VERSION_HISTORY.md   # Version history and changelog
├── NOTES.md            # Development notes
├── README.md           # Setup and usage guide
├── GIT_SETUP.md        # This file
└── nwn_gff.nim         # Original command-line tool
```

## Contributing Guidelines

### Commit Message Format
```
<type>: <subject>

<body>

<footer>
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Test additions or modifications
- `chore`: Build process or auxiliary tool changes

Examples:
```
feat: add SQLite embedding functionality

Implement full SQLite database embedding into GFF files
with compression and proper error handling.

Closes #123
```

```
fix: correct JSON parsing for nested structures

Fixed issue where nested JSON objects were not properly
converted to GFF struct format.
```

### Branch Naming
- `feature/description` - New features
- `bugfix/description` - Bug fixes
- `hotfix/description` - Critical fixes
- `docs/description` - Documentation updates

## Version Management
Follow semantic versioning (SemVer):
- **MAJOR** version for incompatible API changes
- **MINOR** version for backwards-compatible functionality additions
- **PATCH** version for backwards-compatible bug fixes

Current version: **v0.1.0**

## Release Process
1. Update version in [`gff_api.nim`](gff_api.nim:15)
2. Update [`VERSION_HISTORY.md`](VERSION_HISTORY.md)
3. Update [`API_DOCUMENTATION.md`](API_DOCUMENTATION.md) if needed
4. Commit changes
5. Create version tag
6. Push to GitHub

## Continuous Integration (Future)
Consider setting up GitHub Actions for:
- Automated testing on push
- Building and releasing binaries
- Documentation generation
- Code quality checks

## Security Notes
- Never commit sensitive data (API keys, passwords, etc.)
- Keep dependencies updated
- Review code before pushing
- Use secure HTTPS for all Git operations

## Getting Help
For issues or questions about this Git setup, refer to:
- Git documentation: https://git-scm.com/doc
- GitHub help: https://help.github.com
- Project issues: https://github.com/altpersona/nwn_gff_service/issues