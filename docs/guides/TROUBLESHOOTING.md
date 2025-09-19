# Troubleshooting Guide

![Issues](https://img.shields.io/badge/common--issues-25%2B-blue)
![Solutions](https://img.shields.io/badge/solutions-provided-green)
![Debug](https://img.shields.io/badge/debug--tools-included-orange)

## Table of Contents

- [Quick Diagnosis](#quick-diagnosis)
- [Common Issues](#common-issues)
  - [Installation Problems](#installation-problems)
  - [Conversion Errors](#conversion-errors)
  - [Output Issues](#output-issues)
  - [Performance Problems](#performance-problems)
- [Error Messages](#error-messages)
- [Platform-Specific Issues](#platform-specific-issues)
- [Debug Mode](#debug-mode)
- [FAQ](#frequently-asked-questions)
- [Getting Help](#getting-help)

## Quick Diagnosis

### 🚦 System Health Check

Run this diagnostic script to identify issues quickly:

```python
#!/usr/bin/env python3
# save as diagnose.py

import sys
import subprocess
import shutil
import json
from pathlib import Path

def run_diagnosis():
    """Comprehensive system diagnosis."""

    results = {
        'python': {'status': '✅', 'version': sys.version.split()[0]},
        'dependencies': {},
        'engines': {},
        'permissions': {},
        'system': {}
    }

    # Check Python dependencies
    try:
        import bs4
        results['dependencies']['beautifulsoup4'] = '✅'
    except ImportError:
        results['dependencies']['beautifulsoup4'] = '❌'

    try:
        import tqdm
        results['dependencies']['tqdm'] = '✅'
    except ImportError:
        results['dependencies']['tqdm'] = '❌'

    # Check engines
    if shutil.which('node'):
        results['engines']['node'] = '✅'
        if shutil.which('html-to-text'):
            results['engines']['html-to-text'] = '✅'
        else:
            results['engines']['html-to-text'] = '❌'
    else:
        results['engines']['node'] = '❌'
        results['engines']['html-to-text'] = '⚠️ Node required'

    if shutil.which('pandoc'):
        results['engines']['pandoc'] = '✅'
    else:
        results['engines']['pandoc'] = '⚠️ Optional'

    # Check file permissions
    test_file = Path('test_permission.tmp')
    try:
        test_file.write_text('test')
        test_file.unlink()
        results['permissions']['write'] = '✅'
    except:
        results['permissions']['write'] = '❌'

    # Print results
    print("\n🏥 SYSTEM DIAGNOSIS REPORT")
    print("=" * 50)

    for category, items in results.items():
        print(f"\n📍 {category.upper()}")
        if isinstance(items, dict):
            for item, status in items.items():
                print(f"  {item}: {status}")
        else:
            print(f"  {items}")

    # Overall health
    all_critical = [
        results['dependencies']['beautifulsoup4'] == '✅',
        results['dependencies']['tqdm'] == '✅',
        results['permissions']['write'] == '✅'
    ]

    if all(all_critical):
        print("\n✅ SYSTEM READY - All critical components working")
    else:
        print("\n❌ ISSUES FOUND - Please fix red items above")

    return results

if __name__ == "__main__":
    run_diagnosis()
```

### 🔍 Quick Check Commands

```bash
# Check Python installation
python --version

# Check pip
pip list | grep -E "beautifulsoup4|tqdm|html5lib"

# Check Node.js (for html-to-text)
node --version
npm list -g | grep -E "html-to-text|html-to-md"

# Check Pandoc (optional)
pandoc --version

# Test basic conversion
echo "<h1>Test</h1>" > test.html
python main.py . ./test_output --format md
```

## Common Issues

### Installation Problems

#### Issue: "No module named 'bs4'" or similar import error

**Symptoms:**
```
ImportError: No module named 'bs4'
```

**Solutions:**
```bash
# Solution 1: Install missing dependencies
pip install -r requirements.txt

# Solution 2: Use correct Python/pip version
python3 -m pip install beautifulsoup4

# Solution 3: Virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

#### Issue: "command not found: python"

**Symptoms:**
```bash
bash: python: command not found
```

**Solutions:**
```bash
# Solution 1: Use python3
alias python=python3

# Solution 2: Check PATH
echo $PATH
which python3

# Solution 3: Reinstall Python
# See Installation Guide for platform-specific instructions
```

#### Issue: Node.js packages not installing globally

**Symptoms:**
```
npm ERR! Error: EACCES: permission denied
```

**Solutions:**
```bash
# Solution 1: Fix npm permissions
mkdir ~/.npm-global
npm config set prefix '~/.npm-global'
echo 'export PATH=~/.npm-global/bin:$PATH' >> ~/.bashrc
source ~/.bashrc

# Solution 2: Use sudo (not recommended)
sudo npm install -g @html-to/text-cli

# Solution 3: Use npx instead
npx @html-to/text-cli
```

### Conversion Errors

#### Issue: Empty output files

**Symptoms:**
- Output files are created but contain no content
- Log shows "Conversion resulted in empty output"

**Solutions:**

```python
# Debug script to test content extraction
from bs4 import BeautifulSoup

def test_extraction(html_file):
    with open(html_file, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html5lib')

    # Check what's being extracted
    print(f"Title: {soup.title.string if soup.title else 'None'}")
    print(f"Body length: {len(soup.body.get_text()) if soup.body else 0}")
    print(f"Paragraphs: {len(soup.find_all('p'))}")
    print(f"Main content: {soup.find('main') is not None}")
    print(f"Article: {soup.find('article') is not None}")

    # Test content score
    from main import get_content_score
    for element in soup.find_all(['div', 'article', 'main', 'section'])[:5]:
        score = get_content_score(element)
        print(f"Element {element.name}: score = {score}")

test_extraction('problem_file.html')
```

**Root Causes & Fixes:**

1. **Low content score:**
```python
# Edit main.py to lower threshold
MIN_CONTENT_SCORE = 25  # Lower from default 50
```

2. **Non-standard HTML structure:**
```bash
# Force body extraction
# Modify main.py temporarily or use different engine
python main.py input/ output/ --engine pandoc
```

3. **JavaScript-rendered content:**
```python
# HTML might be empty shell for JS app
# Solution: Use browser automation to get rendered HTML first
from selenium import webdriver

driver = webdriver.Chrome()
driver.get('file:///path/to/file.html')
rendered_html = driver.page_source
with open('rendered.html', 'w') as f:
    f.write(rendered_html)
```

#### Issue: "Pandoc Error" or "Pandoc not found"

**Symptoms:**
```
FATAL ERROR: 'pandoc' command not found.
```

**Solutions:**

```bash
# Solution 1: Install Pandoc
# Windows
choco install pandoc

# macOS
brew install pandoc

# Linux
sudo apt install pandoc  # Debian/Ubuntu
sudo dnf install pandoc  # Fedora

# Solution 2: Use html-to-text engine instead
python main.py input/ output/ --engine html-to-text

# Solution 3: Add Pandoc to PATH
export PATH=$PATH:/usr/local/bin
```

#### Issue: Encoding errors with special characters

**Symptoms:**
```
UnicodeDecodeError: 'utf-8' codec can't decode byte
```

**Solutions:**

```python
# Solution 1: Handle encoding in preprocessing
import chardet

def fix_encoding(file_path):
    # Detect encoding
    with open(file_path, 'rb') as f:
        raw = f.read()
        result = chardet.detect(raw)

    # Re-encode to UTF-8
    encoding = result['encoding']
    with open(file_path, 'r', encoding=encoding, errors='ignore') as f:
        content = f.read()

    with open(file_path + '.utf8', 'w', encoding='utf-8') as f:
        f.write(content)

    return file_path + '.utf8'

# Use the fixed file
fixed_file = fix_encoding('problematic.html')
```

```bash
# Solution 2: Force encoding
PYTHONIOENCODING=utf-8 python main.py input/ output/

# Solution 3: Use iconv to convert files
iconv -f ISO-8859-1 -t UTF-8 input.html > input_utf8.html
```

### Output Issues

#### Issue: Broken Markdown formatting

**Symptoms:**
- Tables not rendering correctly
- Links broken
- Code blocks malformed

**Solutions:**

```python
# Post-process Markdown files
import re

def fix_markdown(md_file):
    with open(md_file, 'r') as f:
        content = f.read()

    # Fix common issues
    # Fix broken links
    content = re.sub(r'\[([^\]]+)\]\s+\(([^)]+)\)', r'[\1](\2)', content)

    # Fix code blocks
    content = re.sub(r'```\s*\n', '```\n', content)

    # Fix tables
    lines = content.split('\n')
    fixed_lines = []
    in_table = False

    for line in lines:
        if '|' in line:
            if not in_table:
                in_table = True
                fixed_lines.append(line)
                # Add header separator if missing
                if not lines[lines.index(line) + 1].startswith('|--'):
                    cols = line.count('|') - 1
                    fixed_lines.append('|' + '---|' * cols)
            else:
                fixed_lines.append(line)
        else:
            in_table = False
            fixed_lines.append(line)

    with open(md_file, 'w') as f:
        f.write('\n'.join(fixed_lines))

fix_markdown('output.md')
```

#### Issue: Files too large (exceeding 2MB limit)

**Symptoms:**
- Output split into multiple files unexpectedly
- File naming becomes complex

**Solutions:**

```python
# Solution 1: Adjust file size limit in main.py
MAX_FILE_SIZE_BYTES = 5 * 1024 * 1024  # Increase to 5MB

# Solution 2: Process files individually
import os
for html_file in os.listdir('input'):
    if html_file.endswith('.html'):
        os.system(f'python main.py input/{html_file} output/')
```

### Performance Problems

#### Issue: Conversion running very slowly

**Symptoms:**
- Processing takes hours for moderate datasets
- High CPU/memory usage

**Solutions:**

```bash
# Solution 1: Use faster engine
python main.py input/ output/ --engine html-to-text  # 2x faster than Pandoc

# Solution 2: Process in parallel
pip install joblib

# parallel_process.py
from joblib import Parallel, delayed
import subprocess

def process_file(file):
    subprocess.run(['python', 'main.py', file, 'output/'])

files = glob.glob('input/*.html')
Parallel(n_jobs=4)(delayed(process_file)(f) for f in files)

# Solution 3: Profile and optimize
python -m cProfile -o profile.stats main.py input/ output/
python -m pstats profile.stats
```

#### Issue: Out of memory errors

**Symptoms:**
- MemoryError
- System becomes unresponsive

**Solutions:**

```python
# Solution 1: Process in smaller batches
def batch_process(input_dir, output_dir, batch_size=50):
    files = os.listdir(input_dir)
    for i in range(0, len(files), batch_size):
        batch = files[i:i+batch_size]
        temp_dir = f'temp_batch_{i}'
        os.makedirs(temp_dir, exist_ok=True)

        for f in batch:
            shutil.copy(f'{input_dir}/{f}', f'{temp_dir}/{f}')

        os.system(f'python main.py {temp_dir} {output_dir}')
        shutil.rmtree(temp_dir)

# Solution 2: Increase swap space (Linux)
# sudo fallocate -l 4G /swapfile
# sudo chmod 600 /swapfile
# sudo mkswap /swapfile
# sudo swapon /swapfile
```

## Error Messages

### Complete Error Reference

| Error Message | Cause | Solution |
|--------------|-------|----------|
| `ImportError: No module named 'bs4'` | Missing BeautifulSoup4 | `pip install beautifulsoup4` |
| `ImportError: No module named 'tqdm'` | Missing tqdm | `pip install tqdm` |
| `FileNotFoundError: [Errno 2] No such file or directory` | Input directory doesn't exist | Check path spelling and existence |
| `PermissionError: [Errno 13] Permission denied` | No write permissions | Check directory permissions or run as admin |
| `UnicodeDecodeError` | Encoding issue | Use `--encoding` flag or fix file encoding |
| `subprocess.CalledProcessError` | External command failed | Check engine installation (Pandoc/Node) |
| `MemoryError` | Out of memory | Process smaller batches |
| `KeyboardInterrupt` | User cancelled | Normal - files processed so far are saved |
| `CRITICAL ERROR: 'pandoc' command not found` | Pandoc not installed | Install Pandoc or use html-to-text engine |
| `Error: No input provided` | html-to-md CLI issue | Check Node.js installation |

### Detailed Error Analysis

```python
# error_analyzer.py
import re
from pathlib import Path

def analyze_log_file(log_file):
    """Analyze log file for common issues."""

    with open(log_file, 'r') as f:
        log_content = f.read()

    # Pattern matching for issues
    patterns = {
        'encoding_errors': r'UnicodeDecodeError|codec.*decode',
        'missing_deps': r'ImportError|ModuleNotFoundError',
        'permission_issues': r'Permission denied|EACCES',
        'memory_issues': r'MemoryError|out of memory',
        'pandoc_errors': r'Pandoc Error|pandoc.*not found',
        'empty_output': r'empty output|score.*low',
        'file_not_found': r'FileNotFoundError|No such file'
    }

    issues_found = {}
    for issue_type, pattern in patterns.items():
        matches = re.findall(pattern, log_content, re.IGNORECASE)
        if matches:
            issues_found[issue_type] = len(matches)

    # Generate report
    print("🔍 LOG ANALYSIS REPORT")
    print("=" * 50)

    if issues_found:
        print("\n⚠️ Issues detected:")
        for issue, count in issues_found.items():
            print(f"  - {issue}: {count} occurrences")
            print(f"    Fix: See troubleshooting section for '{issue}'")
    else:
        print("\n✅ No known issues detected in log")

    # Provide specific recommendations
    if 'encoding_errors' in issues_found:
        print("\n💡 Recommendation: Pre-process files to UTF-8")
        print("   Command: iconv -f ISO-8859-1 -t UTF-8 input.html > output.html")

    if 'memory_issues' in issues_found:
        print("\n💡 Recommendation: Use batch processing")
        print("   See: Performance Problems section")

# Usage
analyze_log_file('run_output.log')
```

## Platform-Specific Issues

### Windows Issues

#### PowerShell Execution Policy
```powershell
# Error: "cannot be loaded because running scripts is disabled"
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Or bypass for single session
powershell -ExecutionPolicy Bypass -File script.ps1
```

#### Path Length Limitations
```python
# Enable long paths in Windows
# Run as Administrator:
# reg add HKLM\SYSTEM\CurrentControlSet\Control\FileSystem /v LongPathsEnabled /t REG_DWORD /d 1

# Or use short paths in Python
import os
short_path = os.path.normpath(long_path)
```

#### Git Bash vs CMD Issues
```bash
# Node.js commands may fail in Git Bash
# Solution: Use CMD or PowerShell for Node commands
cmd /c "npm install -g @html-to/text-cli"
```

### macOS Issues

#### SSL Certificate Errors
```bash
# Update certificates
brew install ca-certificates

# Or for Python
pip install --upgrade certifi
```

#### M1/M2 Architecture Issues
```bash
# Install Rosetta 2 for compatibility
softwareupdate --install-rosetta

# Use arch-specific versions
arch -arm64 pip install beautifulsoup4
```

### Linux Issues

#### Missing System Libraries
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install python3-dev python3-pip build-essential

# CentOS/RHEL
sudo yum groupinstall "Development Tools"
sudo yum install python3-devel
```

#### SELinux Permissions
```bash
# Check if SELinux is blocking
ausearch -m avc -ts recent

# Temporary disable (not recommended for production)
sudo setenforce 0

# Better: Set proper context
sudo chcon -R -t httpd_sys_content_t /path/to/files
```

## Debug Mode

### Enable Verbose Logging

```python
# debug_mode.py
import logging
import sys

# Configure detailed logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('debug.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

# Run with debug logging
import main
main.setup_logging = lambda *args: None  # Disable normal logging
logger = logging.getLogger()

# Now run conversion
main.process_html_files('input/', 'output/', 'md', 'html-to-text')
```

### Step-by-Step Debugging

```python
# debug_conversion.py
import pdb
from main import *

def debug_single_file(html_file):
    """Debug conversion of a single file."""

    # Set breakpoint
    pdb.set_trace()

    # Step through conversion
    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()

    soup = BeautifulSoup(html_content, 'html5lib')

    # Examine content extraction
    candidates = {}
    for el in soup.find_all(['div', 'article', 'main']):
        score = get_content_score(el)
        candidates[el] = score
        print(f"Element: {el.name}, Score: {score}")

    # Check what gets selected
    if candidates:
        best = max(candidates, key=candidates.get)
        print(f"Selected: {best.name} with score {candidates[best]}")

        # Test cleaning
        cleaned = clean_html_for_llm(best)
        print(f"Cleaned HTML length: {len(cleaned)}")

        # Test conversion
        output = convert_html_to_output(cleaned, 'md', 'html-to-text')
        print(f"Output length: {len(output) if output else 0}")

        return output

    return None

# Debug specific file
result = debug_single_file('problem_file.html')
```

## Frequently Asked Questions

### General Questions

**Q: Why is my output empty?**
A: The content scoring algorithm might be filtering out your content. Try:
1. Lower the `MIN_CONTENT_SCORE` in main.py
2. Use Pandoc engine which doesn't filter: `--engine pandoc`
3. Check if your HTML has content in `<main>` or `<article>` tags

**Q: Can I convert PDF files?**
A: No, this tool is specifically for HTML. For PDFs, first convert to HTML using:
```bash
pdftohtml input.pdf output.html
python main.py output.html converted/ --format md
```

**Q: How do I handle JavaScript-rendered content?**
A: Pre-render the HTML using a headless browser:
```python
from selenium import webdriver

options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)
driver.get('https://example.com')
html = driver.page_source
with open('rendered.html', 'w') as f:
    f.write(html)
```

**Q: Which engine should I use?**
A:
- Use `html-to-text` for: Speed, large datasets, simple HTML
- Use `pandoc` for: Complex formatting, academic content, tables

**Q: Can I customize the conversion rules?**
A: Yes, modify these in main.py:
- `ALLOWED_TAGS`: HTML tags to preserve
- `MIN_CONTENT_SCORE`: Extraction threshold
- `get_content_score()`: Scoring algorithm

### Technical Questions

**Q: How do I add support for a new output format?**
A: Add a new condition in the conversion functions:
```python
def convert_html_to_output_pandoc(html_string, output_format):
    if output_format == 'rst':  # ReStructuredText
        command = ['pandoc', '-f', 'html', '-t', 'rst']
    # ... rest of the function
```

**Q: Can I use this in a Python script?**
A: Yes, import and use the functions:
```python
from main import process_html_files

process_html_files('input/', 'output/', 'md', 'html-to-text')
```

**Q: How do I process files from URLs?**
A: Download first, then convert:
```python
import requests

response = requests.get('https://example.com/page.html')
with open('temp.html', 'w') as f:
    f.write(response.text)

# Now convert
os.system('python main.py temp.html output/')
```

**Q: Memory usage is too high. How can I optimize?**
A:
1. Process files individually instead of in batches
2. Use `--engine html-to-text` (uses less memory)
3. Reduce `MAX_FILE_SIZE_BYTES` to create smaller output files
4. Clear Python's garbage collector: `import gc; gc.collect()`

**Q: How do I preserve specific HTML attributes?**
A: Modify the `clean_html_for_llm()` function:
```python
def clean_html_for_llm(soup_tag):
    # ... existing code ...
    for tag in clean_tag.find_all(True):
        if tag.name not in ALLOWED_TAGS:
            # Preserve specific attributes
            if tag.name == 'span' and 'data-important' in tag.attrs:
                continue  # Don't unwrap this tag
            tag.unwrap()
```

## Getting Help

### Before Asking for Help

1. **Run the diagnostic script** (see Quick Diagnosis)
2. **Check the log file** for specific errors
3. **Try the solutions** in this guide
4. **Test with a simple file** to isolate the issue
5. **Update to the latest version**

### Information to Provide

When reporting issues, include:

```markdown
## System Information
- OS: [Windows 10/macOS 12/Ubuntu 20.04]
- Python version: [output of `python --version`]
- Node.js version: [output of `node --version`]
- Pandoc version: [output of `pandoc --version`]

## Issue Description
- What I'm trying to do:
- What happens instead:
- Error messages:

## Steps to Reproduce
1. [First step]
2. [Second step]
3. [Error occurs]

## What I've Tried
- [Solution 1]: [Result]
- [Solution 2]: [Result]

## Files
- Sample input file: [attach if possible]
- Log file: [attach relevant parts]
```

### Where to Get Help

1. **GitHub Issues**: [Create an issue](https://github.com/OT1-roy/html-converter/issues)
2. **Discussions**: [GitHub Discussions](https://github.com/OT1-roy/html-converter/discussions)
3. **Stack Overflow**: Tag with `html-converter`
4. **Email Support**: support@example.com (for commercial users)

### Emergency Fixes

If you need a quick workaround:

```bash
# Bypass all processing - direct Pandoc conversion
pandoc input.html -o output.md

# Minimal Python script for basic conversion
from bs4 import BeautifulSoup
with open('input.html', 'r') as f:
    soup = BeautifulSoup(f, 'html.parser')
with open('output.txt', 'w') as f:
    f.write(soup.get_text())
```

---

[← Back to Usage Examples](USAGE_EXAMPLES.md) | [Next: API Documentation →](../api/API.md)