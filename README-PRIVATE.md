# HTML Converter - Private Development Repository

This is the **private development repository** for the HTML to Markdown/Text Converter project. It contains the complete development environment, internal tools, and full project history.

## Repository Structure

```
html_converter/
├── main.py                 # Main application (public)
├── html-to-md-cli.js      # Node.js wrapper for html-to-md (public)
├── requirements.txt        # Dependencies (public)
├── License                # MIT License (public)
├── README.md              # Public documentation (public)
├── .gitignore.public      # Gitignore for public repo
├── .gitignore.private     # Gitignore for private repo (this one)
├── README-PRIVATE.md      # This file - private development docs
├── REPO-MANAGEMENT.md     # Repository management guide
├── .claude/               # Claude Code settings and development tools
│   └── settings.local.json
├── archive/               # Housekeeping archives  
│   ├── INDEX.md           # Archive documentation
│   └── 2025-01-30/        # Date-stamped archives
└── old/                   # Version history and development iterations
    ├── main_v1.py         # First version
    ├── main_v2.py         # Second iteration  
    └── main_v3.py         # Third iteration

```

## Dual Repository Workflow

### Public Repository
- **URL**: https://github.com/OT1-roy/html-converter
- **Purpose**: Clean, production-ready code for open source community
- **Contains**: Main application, documentation, license, basic requirements
- **Excludes**: Development files, version history, internal tools

### Private Repository  
- **URL**: https://github.com/OT1-roy/html-converter-private
- **Purpose**: Complete development environment and project history
- **Contains**: Everything - all files, development tools, version history
- **Access**: Private - for development team only

## Development Workflow

### Making Changes
1. Work in this private repository with full development environment
2. Test changes thoroughly with all development tools available
3. When ready for public release:
   - Copy relevant changes to public repo
   - Update public documentation
   - Test in public environment
   - Push to both repositories

### Git Remotes Setup
```bash
# Public repository (origin)
git remote add origin https://github.com/OT1-roy/html-converter.git

# Private repository  
git remote add private https://github.com/OT1-roy/html-converter-private.git
```

### Pushing Changes
```bash
# Push to private repo (development)
git push private main

# Push to public repo (releases)
git push origin main
```

## Development Tools

### Claude Code Integration
- `.claude/settings.local.json` - Claude Code project settings
- Development permissions and tool configurations
- AI-assisted development workflow integration

### Version History
- `old/main_v1.py` - Initial prototype (v1.0.0)
- `old/main_v2.py` - Second iteration with improved parsing
- `old/main_v3.py` - Third version with better error handling
- **v2.0.0** - Current version with dual-engine architecture (Pandoc + html-to-text support)

## Architecture Notes (v2.0.0)

### Dual-Engine Implementation
The current version implements a sophisticated dual-engine architecture allowing users to choose between two conversion backends:

#### Engine Functions
- `convert_html_to_output_pandoc()` - Original Pandoc-based conversion (battle-tested)
- `convert_html_to_output_html_to_text()` - New html-to-text engine with enterprise parsing
- `convert_html_to_output()` - Dispatcher function that routes to appropriate engine

#### Dependency Management
- `check_pandoc_dependency()` - Validates Pandoc installation
- `check_html_to_text_dependency()` - Validates html-to-text CLI with fallback paths
- `check_dependencies()` - Engine-specific dependency validation

#### CLI Enhancement
- Added `--engine` parameter with choices: `html-to-text` (default) | `pandoc`
- Maintains full backward compatibility
- Enhanced logging shows engine selection in all outputs

### Development Considerations
- **Dual-Library Architecture**: html-to-text engine uses two specialized libraries:
  - `@html-to/text-cli` for plain text output
  - `html-to-md` for Markdown output (with custom Node.js wrapper)
- **Windows Compatibility**: Uses `cmd /c` explicitly to avoid Git Bash conflicts in subprocess calls
- **Format-Specific Routing**: Engine automatically selects appropriate library based on output format
- **Custom CLI Wrapper**: `html-to-md-cli.js` provides stdin/stdout interface for html-to-md package
- **Cross-Platform Support**: Different subprocess handling for Windows vs Unix systems
- **Error Handling**: Isolated error handling per library to prevent cross-contamination
- **Future Extensibility**: Architecture allows for additional engines and format-specific libraries

## Security Notes

- **Never commit secrets** - Even in private repo, avoid hardcoded credentials
- **Review before public sync** - Always review changes before copying to public repo
- **Keep proprietary info private** - Business logic, internal docs stay here
- **Public repo hygiene** - Maintain clean, professional appearance for public repo

## Development Setup

1. Clone this private repository
2. Install dependencies: `pip install -r requirements.txt`
3. Set up Claude Code with existing `.claude/settings.local.json`
4. Use development tools and full version history as needed
5. Test changes before pushing to public repository

## Release Process

1. Complete development and testing in private repo
2. Update version number in `main.py`
3. Review public documentation in `README.md`
4. Copy changes to public repo (excluding private files)
5. Test in public repo environment
6. Push to both repositories
7. Create release tags in public repo if needed

---
**Note**: This README is for internal development use only and should not be copied to the public repository.