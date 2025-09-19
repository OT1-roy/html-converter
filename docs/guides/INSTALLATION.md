# Installation Guide

![Python](https://img.shields.io/badge/python-3.7%2B-brightgreen)
![Node](https://img.shields.io/badge/node.js-14%2B-green)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-blue)

## Table of Contents

- [System Requirements](#system-requirements)
- [Quick Install](#quick-install)
- [Detailed Installation](#detailed-installation)
  - [Windows](#windows-installation)
  - [macOS](#macos-installation)
  - [Linux](#linux-installation)
- [Docker Installation](#docker-installation)
- [Development Setup](#development-setup)
- [Verification](#verification)
- [Troubleshooting](#troubleshooting-installation)
- [Uninstallation](#uninstallation)

## System Requirements

### Minimum Requirements

| Component | Requirement | Check Command |
|-----------|------------|---------------|
| **Python** | 3.7 or higher | `python --version` |
| **pip** | Latest version | `pip --version` |
| **Memory** | 512 MB RAM | - |
| **Storage** | 100 MB free space | - |

### Engine-Specific Requirements

#### For html-to-text Engine (Default)
| Component | Requirement | Check Command |
|-----------|------------|---------------|
| **Node.js** | 14.0 or higher | `node --version` |
| **npm** | 6.0 or higher | `npm --version` |

#### For Pandoc Engine
| Component | Requirement | Check Command |
|-----------|------------|---------------|
| **Pandoc** | 2.0 or higher | `pandoc --version` |

### Operating System Support

✅ **Windows** 10/11 (64-bit)
✅ **macOS** 10.14+ (Mojave or later)
✅ **Linux** Ubuntu 18.04+, Debian 10+, CentOS 8+, Fedora 32+

## Quick Install

### One-Line Installation (Recommended)

**Windows (PowerShell as Administrator):**
```powershell
# Complete installation script
Set-ExecutionPolicy Bypass -Scope Process -Force; `
iex ((New-Object System.Net.WebClient).DownloadString('https://raw.githubusercontent.com/OT1-roy/html-converter/main/install.ps1'))
```

**macOS/Linux:**
```bash
# Complete installation script
curl -fsSL https://raw.githubusercontent.com/OT1-roy/html-converter/main/install.sh | bash
```

### Manual Quick Install

```bash
# 1. Clone repository
git clone https://github.com/OT1-roy/html-converter.git
cd html-converter

# 2. Install Python dependencies
pip install -r requirements.txt

# 3. Install Node.js dependencies (for html-to-text engine)
npm install -g @html-to/text-cli
npm install -g html-to-md

# 4. Verify installation
python main.py --version
```

## Detailed Installation

### Windows Installation

#### Step 1: Install Python

1. Download Python from [python.org](https://www.python.org/downloads/)
2. Run installer with these options:
   - ✅ Add Python to PATH
   - ✅ Install pip
   - ✅ Install for all users (optional)

3. Verify installation:
```cmd
python --version
pip --version
```

#### Step 2: Install Node.js (for html-to-text engine)

1. Download Node.js from [nodejs.org](https://nodejs.org/)
2. Run the installer (includes npm)
3. Verify installation:
```cmd
node --version
npm --version
```

#### Step 3: Install Pandoc (optional, for Pandoc engine)

**Option A: Using Chocolatey**
```powershell
choco install pandoc
```

**Option B: Manual Installation**
1. Download from [pandoc.org](https://pandoc.org/installing.html#windows)
2. Run the MSI installer
3. Add to PATH if not automatic

#### Step 4: Clone and Setup HTML Converter

```powershell
# Clone repository
git clone https://github.com/OT1-roy/html-converter.git
cd html-converter

# Create virtual environment (recommended)
python -m venv venv
.\venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt

# Install Node.js dependencies
npm install -g @html-to/text-cli
npm install -g html-to-md
```

#### Step 5: Configure Environment Variables (Optional)

```powershell
# Add to system PATH (run as Administrator)
[Environment]::SetEnvironmentVariable("PATH", "$env:PATH;C:\path\to\html-converter", [EnvironmentVariableTarget]::Machine)
```

### macOS Installation

#### Step 1: Install Homebrew (if not installed)

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

#### Step 2: Install Python

```bash
# Install Python
brew install python@3.11

# Verify installation
python3 --version
pip3 --version
```

#### Step 3: Install Node.js (for html-to-text engine)

```bash
# Install Node.js
brew install node

# Verify installation
node --version
npm --version
```

#### Step 4: Install Pandoc (optional, for Pandoc engine)

```bash
brew install pandoc
```

#### Step 5: Clone and Setup HTML Converter

```bash
# Clone repository
git clone https://github.com/OT1-roy/html-converter.git
cd html-converter

# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# Install Node.js dependencies
npm install -g @html-to/text-cli
npm install -g html-to-md
```

### Linux Installation

#### Ubuntu/Debian

```bash
# Update package manager
sudo apt update

# Install Python and pip
sudo apt install python3 python3-pip python3-venv

# Install Node.js
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install nodejs

# Install Pandoc (optional)
sudo apt install pandoc

# Install git
sudo apt install git

# Clone and setup
git clone https://github.com/OT1-roy/html-converter.git
cd html-converter

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
npm install -g @html-to/text-cli
npm install -g html-to-md
```

#### CentOS/RHEL/Fedora

```bash
# Install Python
sudo dnf install python3 python3-pip

# Install Node.js
curl -fsSL https://rpm.nodesource.com/setup_18.x | sudo bash -
sudo dnf install nodejs

# Install Pandoc (optional)
sudo dnf install pandoc

# Install git
sudo dnf install git

# Clone and setup (same as Ubuntu)
git clone https://github.com/OT1-roy/html-converter.git
cd html-converter
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
npm install -g @html-to/text-cli
npm install -g html-to-md
```

## Docker Installation

### Using Pre-built Image

```bash
# Pull the image
docker pull ghcr.io/ot1-roy/html-converter:latest

# Run conversion
docker run -v $(pwd)/input:/input -v $(pwd)/output:/output \
  ghcr.io/ot1-roy/html-converter:latest \
  /input /output --format md
```

### Building from Dockerfile

```dockerfile
# Dockerfile
FROM python:3.11-slim

# Install Node.js
RUN apt-get update && \
    apt-get install -y nodejs npm pandoc && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy files
COPY requirements.txt .
COPY main.py .
COPY html-to-md-cli.js .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install Node dependencies
RUN npm install -g @html-to/text-cli html-to-md

# Set entrypoint
ENTRYPOINT ["python", "main.py"]
```

Build and run:
```bash
# Build image
docker build -t html-converter .

# Run container
docker run -v $(pwd)/input:/input -v $(pwd)/output:/output \
  html-converter /input /output --format md
```

## Development Setup

### Full Development Environment

```bash
# Clone with submodules (if any)
git clone --recursive https://github.com/OT1-roy/html-converter.git
cd html-converter

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate

# Install in development mode
pip install -r requirements.txt
pip install -r requirements-dev.txt  # If available

# Install pre-commit hooks (if using)
pre-commit install

# Install Node.js dependencies locally
npm install

# Run tests
python -m pytest
```

### IDE Setup

#### VS Code
```json
// .vscode/settings.json
{
  "python.defaultInterpreterPath": "./venv/bin/python",
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": true,
  "python.formatting.provider": "black"
}
```

#### PyCharm
1. File → Settings → Project → Python Interpreter
2. Add Interpreter → Existing Environment
3. Select `venv/bin/python`

## Verification

### Complete Installation Check

Run this verification script to ensure everything is installed correctly:

```python
# save as verify_install.py
import sys
import subprocess
import shutil

def check_command(cmd, name):
    if shutil.which(cmd):
        try:
            result = subprocess.run([cmd, "--version"],
                                  capture_output=True, text=True)
            print(f"✅ {name}: Installed")
            return True
        except:
            print(f"⚠️ {name}: Found but error getting version")
            return False
    else:
        print(f"❌ {name}: Not found")
        return False

print("HTML Converter Installation Verification")
print("=" * 40)

# Check Python
print(f"✅ Python: {sys.version}")

# Check pip
check_command("pip", "pip")

# Check Node.js (for html-to-text)
node_ok = check_command("node", "Node.js")
npm_ok = check_command("npm", "npm")

# Check Pandoc (optional)
pandoc_ok = check_command("pandoc", "Pandoc")

# Check html-to-text CLI
if node_ok and npm_ok:
    html_to_text_ok = check_command("html-to-text", "html-to-text CLI")
else:
    print("⚠️ html-to-text CLI: Skipped (Node.js required)")

# Summary
print("\n" + "=" * 40)
if node_ok and npm_ok:
    print("✅ html-to-text engine: Ready")
else:
    print("❌ html-to-text engine: Missing dependencies")

if pandoc_ok:
    print("✅ Pandoc engine: Ready")
else:
    print("⚠️ Pandoc engine: Not installed (optional)")

print("=" * 40)
```

Run verification:
```bash
python verify_install.py
```

### Test Conversion

```bash
# Create test file
echo "<html><body><h1>Test</h1><p>Hello World</p></body></html>" > test.html

# Test with html-to-text engine
python main.py . ./output --format md --engine html-to-text

# Test with Pandoc engine (if installed)
python main.py . ./output --format md --engine pandoc

# Check output
cat output/*
```

## Troubleshooting Installation

### Common Issues and Solutions

#### Python Issues

**Issue: "python" command not found**
```bash
# Try python3 instead
python3 --version

# Create alias (Linux/macOS)
alias python=python3

# Or use py launcher (Windows)
py --version
```

**Issue: pip not found**
```bash
# Install pip
python -m ensurepip --upgrade

# Or download get-pip.py
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python get-pip.py
```

#### Node.js Issues

**Issue: npm command not found after Node.js installation**
```bash
# Reinstall Node.js with npm
# Or install npm separately
curl -L https://www.npmjs.com/install.sh | sh
```

**Issue: Permission denied when installing global npm packages**
```bash
# Option 1: Use npm prefix
npm config set prefix ~/.npm-global
export PATH=$PATH:~/.npm-global/bin

# Option 2: Use sudo (Linux/macOS)
sudo npm install -g @html-to/text-cli

# Option 3: Fix npm permissions
mkdir ~/.npm-global
npm config set prefix '~/.npm-global'
echo 'export PATH=~/.npm-global/bin:$PATH' >> ~/.profile
source ~/.profile
```

#### Pandoc Issues

**Issue: Pandoc not in PATH after installation**
```bash
# Find Pandoc location
which pandoc || where pandoc

# Add to PATH manually
export PATH=$PATH:/usr/local/bin  # Adjust path as needed

# Make permanent (add to ~/.bashrc or ~/.zshrc)
echo 'export PATH=$PATH:/usr/local/bin' >> ~/.bashrc
```

#### Virtual Environment Issues

**Issue: venv activation not working**
```bash
# Windows PowerShell execution policy
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Linux/macOS permission issue
chmod +x venv/bin/activate
```

### Platform-Specific Issues

#### Windows
- **Long path issues**: Enable long path support in Windows
- **Encoding issues**: Set `PYTHONIOENCODING=utf-8` environment variable
- **Git Bash conflicts**: Use CMD or PowerShell for Node.js commands

#### macOS
- **SSL certificate issues**: Update certificates with `brew install ca-certificates`
- **M1/M2 compatibility**: Use arm64 versions of Python and Node.js

#### Linux
- **Missing development tools**: Install `build-essential` (Ubuntu) or `Development Tools` (CentOS)
- **Python headers missing**: Install `python3-dev` or `python3-devel`

## Uninstallation

### Complete Removal

**Windows:**
```powershell
# Remove Python packages
pip uninstall -r requirements.txt

# Remove Node packages
npm uninstall -g @html-to/text-cli html-to-md

# Remove directory
Remove-Item -Recurse -Force html-converter
```

**macOS/Linux:**
```bash
# Deactivate virtual environment
deactivate

# Remove Python packages
pip uninstall -r requirements.txt

# Remove Node packages
npm uninstall -g @html-to/text-cli html-to-md

# Remove directory
rm -rf html-converter
```

### Clean Uninstall Script

```bash
#!/bin/bash
# save as uninstall.sh

echo "Uninstalling HTML Converter..."

# Remove virtual environment
if [ -d "venv" ]; then
    rm -rf venv
    echo "✅ Removed virtual environment"
fi

# Remove node_modules
if [ -d "node_modules" ]; then
    rm -rf node_modules
    echo "✅ Removed node_modules"
fi

# Remove global npm packages
npm uninstall -g @html-to/text-cli html-to-md 2>/dev/null
echo "✅ Removed global npm packages"

# Remove cache files
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
find . -type f -name "*.pyc" -delete 2>/dev/null
echo "✅ Removed cache files"

echo "Uninstallation complete!"
```

## Getting Help

If you encounter issues not covered here:

1. Check [Troubleshooting Guide](TROUBLESHOOTING.md)
2. Search [existing issues](https://github.com/OT1-roy/html-converter/issues)
3. Create a [new issue](https://github.com/OT1-roy/html-converter/issues/new) with:
   - Your operating system
   - Python version
   - Error messages
   - Steps to reproduce

---

[← Back to README](../../README.md) | [Next: Usage Examples →](USAGE_EXAMPLES.md)