# API Reference Documentation

![API Version](https://img.shields.io/badge/API-v2.0.0-blue)
![Python](https://img.shields.io/badge/python-3.7%2B-green)
![Type Hints](https://img.shields.io/badge/type--hints-yes-orange)

## Table of Contents

- [Module Overview](#module-overview)
- [Core Functions](#core-functions)
  - [setup_logging](#setup_logging)
  - [check_dependencies](#check_dependencies)
  - [get_content_score](#get_content_score)
  - [clean_html_for_llm](#clean_html_for_llm)
  - [convert_html_to_output](#convert_html_to_output)
  - [process_html_files](#process_html_files)
- [Engine Functions](#engine-functions)
  - [convert_html_to_output_pandoc](#convert_html_to_output_pandoc)
  - [convert_html_to_output_html_to_text](#convert_html_to_output_html_to_text)
- [Constants and Configuration](#constants-and-configuration)
- [Type Definitions](#type-definitions)
- [Exceptions](#exceptions)
- [Usage Examples](#usage-examples)
- [Extending the API](#extending-the-api)

## Module Overview

The HTML Converter API provides programmatic access to HTML-to-Markdown/Text conversion functionality.

### Module Structure

```python
# main.py structure
├── Configuration Constants
├── Setup Functions
│   ├── setup_logging()
│   └── check_dependencies()
├── Content Processing
│   ├── get_content_score()
│   └── clean_html_for_llm()
├── Conversion Engines
│   ├── convert_html_to_output()
│   ├── convert_html_to_output_pandoc()
│   └── convert_html_to_output_html_to_text()
└── Main Processing
    └── process_html_files()
```

### Importing the Module

```python
# As a module
import main

# Specific imports
from main import process_html_files, get_content_score

# With alias
import main as html_converter
```

## Core Functions

### setup_logging

```python
def setup_logging(output_dir: str, input_folder_name: str) -> None
```

Sets up file and console logging for the conversion process.

#### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `output_dir` | `str` | Directory where log files will be created |
| `input_folder_name` | `str` | Name used for log file naming |

#### Returns

`None`

#### Raises

- `IOError`: If log file cannot be created
- `PermissionError`: If no write permission for output directory

#### Example

```python
import os
from main import setup_logging

# Setup logging for conversion job
output_dir = "/path/to/output"
input_name = "website_archive"

setup_logging(output_dir, input_name)
# Creates: /path/to/output/run_website_archive.log

# Logging is now configured
import logging
logging.info("Conversion started")
```

#### Implementation Details

- Creates log file named `run_{input_folder_name}.log`
- Sets INFO level for file logging
- Sets ERROR level for console output
- Prevents duplicate handlers in interactive environments

---

### check_dependencies

```python
def check_dependencies(engine: str) -> None
```

Verifies that required dependencies for the specified engine are installed.

#### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `engine` | `str` | Conversion engine (`'pandoc'` or `'html-to-text'`) |

#### Returns

`None`

#### Raises

- `SystemExit`: If critical dependencies are missing
- `ValueError`: If unknown engine is specified

#### Example

```python
from main import check_dependencies

# Check Pandoc dependencies
try:
    check_dependencies('pandoc')
    print("Pandoc is ready")
except SystemExit:
    print("Pandoc not installed")

# Check html-to-text dependencies
check_dependencies('html-to-text')
```

#### Engine-Specific Checks

```python
# Pandoc engine checks
- Verifies 'pandoc' command is in PATH
- Tests pandoc --version execution

# html-to-text engine checks
- Verifies Node.js dependencies
- Checks for npm packages (deferred to runtime)
```

---

### get_content_score

```python
def get_content_score(tag: element.Tag) -> int
```

Calculates a content quality score for an HTML element to identify main content.

#### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `tag` | `element.Tag` | BeautifulSoup tag element to score |

#### Returns

| Type | Description |
|------|-------------|
| `int` | Content score (higher = more likely to be main content) |

#### Scoring Algorithm

```python
# Scoring factors:
# Positive signals:
- Length of text content: +1 per character
- Number of paragraphs: +25 per <p> tag
- Content indicators in class/id: +50
- Article tag: +200

# Negative signals:
- High link density (>40%): -100
- Navigation/ad indicators in class/id: -50
```

#### Example

```python
from bs4 import BeautifulSoup
from main import get_content_score

html = """
<article class="main-content">
    <p>This is the main article content.</p>
    <p>It has multiple paragraphs.</p>
</article>
<div class="sidebar advertisement">
    <a href="#">Link 1</a>
    <a href="#">Link 2</a>
</div>
"""

soup = BeautifulSoup(html, 'html5lib')
article = soup.find('article')
sidebar = soup.find('div', class_='sidebar')

print(f"Article score: {get_content_score(article)}")  # High score (250+)
print(f"Sidebar score: {get_content_score(sidebar)}")  # Low/negative score
```

#### Customization

```python
# Modify scoring weights
def custom_content_score(tag):
    score = 0

    # Custom weight for text length
    text = tag.get_text(strip=True)
    score += len(text) * 2  # Double weight

    # Custom paragraph scoring
    score += len(tag.find_all('p')) * 50  # Higher weight

    # Add custom patterns
    class_id = ' '.join(tag.get('class', [])) + ' ' + (tag.get('id', '') or '')
    if re.search('featured|highlight', class_id, re.I):
        score += 100

    return score
```

---

### clean_html_for_llm

```python
def clean_html_for_llm(soup_tag: element.Tag) -> str
```

Surgically cleans HTML by removing unwanted tags while preserving content structure.

#### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `soup_tag` | `element.Tag` | BeautifulSoup tag to clean |

#### Returns

| Type | Description |
|------|-------------|
| `str` | Cleaned HTML string with only allowed tags |

#### Allowed Tags

```python
ALLOWED_TAGS = [
    'p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
    'ul', 'ol', 'li', 'blockquote', 'pre', 'code',
    'table', 'tr', 'td', 'th', 'strong', 'em', 'a'
]
```

#### Example

```python
from bs4 import BeautifulSoup
from main import clean_html_for_llm

html = """
<div>
    <script>alert('removed');</script>
    <p>This paragraph is kept.</p>
    <span style="color:red">This span is unwrapped.</span>
    <strong>This is preserved.</strong>
</div>
"""

soup = BeautifulSoup(html, 'html5lib')
cleaned = clean_html_for_llm(soup.find('div'))

print(cleaned)
# Output: <div><p>This paragraph is kept.</p>This span is unwrapped.<strong>This is preserved.</strong></div>
```

#### Customization

```python
# Use custom allowed tags
def clean_with_custom_tags(soup_tag, allowed_tags):
    clean_tag = BeautifulSoup(str(soup_tag), 'html5lib').find()

    for tag in clean_tag.find_all(True):
        if tag.name not in allowed_tags:
            tag.unwrap()

    return str(clean_tag)

# Allow additional tags
custom_allowed = ALLOWED_TAGS + ['figure', 'figcaption', 'mark']
cleaned = clean_with_custom_tags(soup_tag, custom_allowed)
```

---

### convert_html_to_output

```python
def convert_html_to_output(
    html_string: str,
    output_format: str,
    engine: str
) -> Optional[str]
```

Main dispatcher function that routes conversion to the appropriate engine.

#### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `html_string` | `str` | HTML content to convert |
| `output_format` | `str` | Target format (`'md'` or `'txt'`) |
| `engine` | `str` | Conversion engine (`'pandoc'` or `'html-to-text'`) |

#### Returns

| Type | Description |
|------|-------------|
| `Optional[str]` | Converted text/markdown, or `None` if conversion fails |

#### Example

```python
from main import convert_html_to_output

html = "<h1>Title</h1><p>Content here.</p>"

# Convert to Markdown with html-to-text (Recommended - Superior Output)
markdown = convert_html_to_output(html, 'md', 'html-to-text')
print(markdown)
# # Title
#
# Content here.
# Note: Clean, standard Markdown without artifacts

# Convert to plain text with Pandoc (Legacy option)
text = convert_html_to_output(html, 'txt', 'pandoc')
print(text)
# Title
#
# Content here.
# Note: May include proprietary syntax like ::: divs
```

**💡 Best Practice**: Use `html-to-text` engine for clean, ML-ready output. Our tests show it produces 5/5 quality vs Pandoc's 2/5.

#### Error Handling

```python
result = convert_html_to_output(html, 'md', 'pandoc')
if result is None:
    # Conversion failed - check logs for details
    logging.error("Conversion failed, trying alternative engine")
    result = convert_html_to_output(html, 'md', 'html-to-text')
```

---

### process_html_files

```python
def process_html_files(
    input_dir: str,
    output_dir: str,
    output_format: str,
    engine: str
) -> None
```

Main orchestration function that processes all HTML files in a directory and **automatically combines them into a single output file**.

#### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `input_dir` | `str` | Directory containing HTML files |
| `output_dir` | `str` | Directory for output files |
| `output_format` | `str` | Output format (`'md'` or `'txt'`) |
| `engine` | `str` | Conversion engine to use |

#### Returns

`None`

#### Raises

- `SystemExit`: If input directory not found or critical errors occur
- `KeyboardInterrupt`: Handled gracefully for user cancellation

#### Features

- **Automatic file combining**: All input HTML files merged into single output
- **Automatic file splitting**: If output exceeds 2MB, creates numbered parts
- Progress bar with tqdm
- Comprehensive logging
- Job statistics reporting

#### Default Behavior

**Important**: By default, all HTML files from the input directory are combined into a single output file. This is the standard behavior - no special flags or options needed. If the combined output exceeds 2MB, it automatically splits into numbered parts (output_1.md, output_2.md, etc.)

#### Example

```python
from main import process_html_files

# Basic usage - combines all HTML files into single output
process_html_files(
    input_dir='./html_docs',
    output_dir='./markdown_docs',
    output_format='md',
    engine='html-to-text'
)
# Result: All HTML files combined into markdown_docs/html_docs_output_1.md

# Real-world example: 49 podcast transcriptions
process_html_files(
    input_dir='./podcast_transcriptions',
    output_dir='./output',
    output_format='md',
    engine='html-to-text'
)
# Result: 49 HTML files → single output/podcast_transcriptions_output_1.md

# With error handling
try:
    process_html_files('./input', './output', 'md', 'pandoc')
except SystemExit as e:
    if e.code == 1:
        print("Processing failed - check logs")
```

#### Processing Statistics

```python
# The function tracks and reports:
job_stats = {
    "successful": 0,      # Successfully converted files
    "failed": 0,          # Failed conversions
    "output_files": 1     # Number of output files created
}

# Access via logging
# INFO: Job finished.
# - Total HTML files scanned: 150
# - Successful extractions: 148
# - Failed extractions: 2
# - Total output files created: 3 (.md)
```

## Engine Functions

### convert_html_to_output_pandoc

```python
def convert_html_to_output_pandoc(
    html_string: str,
    output_format: str
) -> Optional[str]
```

Converts HTML using the Pandoc engine.

#### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `html_string` | `str` | HTML content to convert |
| `output_format` | `str` | Target format (`'md'` or `'txt'`) |

#### Returns

| Type | Description |
|------|-------------|
| `Optional[str]` | Converted content or `None` on failure |

#### Pandoc Commands

```python
# Markdown conversion
['pandoc', '-f', 'html', '-t', 'markdown-smart']

# Plain text conversion
['pandoc', '-f', 'html', '-t', 'plain+smart', '--wrap=none', '--columns=9999']
```

#### Example

```python
from main import convert_html_to_output_pandoc

html = "<h1>Test</h1><p>Content with <em>emphasis</em>.</p>"

# Convert to Markdown
md = convert_html_to_output_pandoc(html, 'md')
print(md)
# # Test
#
# Content with *emphasis*.

# Convert to plain text
txt = convert_html_to_output_pandoc(html, 'txt')
print(txt)
# Test
#
# Content with emphasis.
```

---

### convert_html_to_output_html_to_text

```python
def convert_html_to_output_html_to_text(
    html_string: str,
    output_format: str
) -> Optional[str]
```

Converts HTML using the html-to-text engine (Node.js based).

#### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `html_string` | `str` | HTML content to convert |
| `output_format` | `str` | Target format (`'md'` or `'txt'`) |

#### Returns

| Type | Description |
|------|-------------|
| `Optional[str]` | Converted content or `None` on failure |

#### Implementation Details

```python
# For Markdown output:
- Uses custom html-to-md-cli.js wrapper
- Falls back to direct Node.js execution

# For text output:
- Tries global html-to-text command first
- Falls back to node_modules path
```

#### Example

```python
from main import convert_html_to_output_html_to_text

html = """
<h1>Title</h1>
<ul>
  <li>Item 1</li>
  <li>Item 2</li>
</ul>
"""

# Convert to Markdown
md = convert_html_to_output_html_to_text(html, 'md')
print(md)
# # Title
#
# * Item 1
# * Item 2

# Convert to plain text
txt = convert_html_to_output_html_to_text(html, 'txt')
print(txt)
# TITLE
#
# * Item 1
# * Item 2
```

## Constants and Configuration

### Global Constants

```python
# Version information
VERSION: str = "2.0.0"

# File size limits
MAX_FILE_SIZE_BYTES: int = 2 * 1024 * 1024  # 2 MB

# Content extraction
MIN_CONTENT_SCORE: int = 50  # Minimum score for content extraction

# Allowed HTML tags
ALLOWED_TAGS: List[str] = [
    'p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
    'ul', 'ol', 'li', 'blockquote', 'pre', 'code',
    'table', 'tr', 'td', 'th', 'strong', 'em', 'a'
]
```

### Modifying Constants

```python
import main

# Increase file size limit
main.MAX_FILE_SIZE_BYTES = 5 * 1024 * 1024  # 5 MB

# Lower content score threshold
main.MIN_CONTENT_SCORE = 25

# Add allowed tags
main.ALLOWED_TAGS.append('figure')
main.ALLOWED_TAGS.append('figcaption')
```

## Type Definitions

### Type Hints

```python
from typing import Optional, Dict, List
from bs4 import element

# Function signatures with types
def setup_logging(output_dir: str, input_folder_name: str) -> None: ...
def get_content_score(tag: element.Tag) -> int: ...
def clean_html_for_llm(soup_tag: element.Tag) -> str: ...
def convert_html_to_output(html_string: str, output_format: str, engine: str) -> Optional[str]: ...

# Internal types
job_stats: Dict[str, int] = {"successful": 0, "failed": 0, "output_files": 1}
all_files: List[str] = []
candidates: Dict[element.Tag, int] = {}
```

### Custom Type Definitions

```python
from typing import TypedDict, Literal

# Define custom types
class JobStats(TypedDict):
    successful: int
    failed: int
    output_files: int

OutputFormat = Literal['md', 'txt']
Engine = Literal['pandoc', 'html-to-text']

# Use in functions
def typed_convert(
    html: str,
    format: OutputFormat,
    engine: Engine
) -> Optional[str]:
    return convert_html_to_output(html, format, engine)
```

## Exceptions

### Exception Handling

The module handles various exceptions internally but may raise:

```python
# System-level exceptions
SystemExit(1)  # Critical errors, missing dependencies
KeyboardInterrupt  # User cancellation (handled gracefully)

# Common exceptions (logged, not raised)
FileNotFoundError  # Input files/directories not found
PermissionError  # No write access
UnicodeDecodeError  # Encoding issues
subprocess.CalledProcessError  # Engine command failures
MemoryError  # Out of memory
```

### Error Recovery

```python
# Example error recovery pattern
import logging
from main import convert_html_to_output

def safe_convert(html, format='md'):
    """Convert with fallback engines."""

    # Try primary engine
    try:
        result = convert_html_to_output(html, format, 'html-to-text')
        if result:
            return result
    except Exception as e:
        logging.warning(f"html-to-text failed: {e}")

    # Fallback to Pandoc
    try:
        result = convert_html_to_output(html, format, 'pandoc')
        if result:
            return result
    except Exception as e:
        logging.warning(f"Pandoc failed: {e}")

    # Last resort - return raw text
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html, 'html5lib')
    return soup.get_text()
```

## Usage Examples

### Basic Module Usage

```python
#!/usr/bin/env python3
import main

# Simple conversion
main.process_html_files(
    input_dir='./html_files',
    output_dir='./output',
    output_format='md',
    engine='html-to-text'
)
```

### Advanced Integration

```python
#!/usr/bin/env python3
"""Advanced HTML converter integration."""

import os
import logging
from pathlib import Path
from typing import List, Optional
from bs4 import BeautifulSoup

import main

class HTMLConverterWrapper:
    """Wrapper class for HTML converter with enhanced functionality."""

    def __init__(self, engine: str = 'html-to-text', min_score: int = 50):
        self.engine = engine
        main.MIN_CONTENT_SCORE = min_score

    def convert_file(self, file_path: str, output_format: str = 'md') -> Optional[str]:
        """Convert a single HTML file."""
        with open(file_path, 'r', encoding='utf-8') as f:
            html_content = f.read()

        # Parse and extract
        soup = BeautifulSoup(html_content, 'html5lib')

        # Find best content
        candidates = {}
        for elem in soup.find_all(['div', 'article', 'main', 'section']):
            score = main.get_content_score(elem)
            if score >= main.MIN_CONTENT_SCORE:
                candidates[elem] = score

        if not candidates:
            logging.warning(f"No suitable content found in {file_path}")
            return None

        # Get best candidate
        best_elem = max(candidates, key=candidates.get)

        # Clean and convert
        cleaned_html = main.clean_html_for_llm(best_elem)
        result = main.convert_html_to_output(cleaned_html, output_format, self.engine)

        return result

    def batch_convert(self, files: List[str], output_dir: str) -> dict:
        """Convert multiple files with statistics."""
        os.makedirs(output_dir, exist_ok=True)

        stats = {'success': 0, 'failed': 0}

        for file in files:
            try:
                result = self.convert_file(file)
                if result:
                    output_path = Path(output_dir) / f"{Path(file).stem}.md"
                    output_path.write_text(result, encoding='utf-8')
                    stats['success'] += 1
                else:
                    stats['failed'] += 1
            except Exception as e:
                logging.error(f"Error converting {file}: {e}")
                stats['failed'] += 1

        return stats

# Usage
converter = HTMLConverterWrapper(engine='pandoc', min_score=75)

# Convert single file
result = converter.convert_file('document.html', 'md')

# Batch conversion
files = list(Path('./html_docs').glob('*.html'))
stats = converter.batch_convert(files, './markdown_output')
print(f"Converted: {stats['success']}, Failed: {stats['failed']}")
```

### Custom Pipeline Integration

```python
#!/usr/bin/env python3
"""Custom processing pipeline using HTML converter."""

from typing import Optional
import main
from bs4 import BeautifulSoup

class ContentPipeline:
    """Custom content processing pipeline."""

    @staticmethod
    def preprocess(html: str) -> str:
        """Preprocess HTML before conversion."""
        soup = BeautifulSoup(html, 'html5lib')

        # Remove specific elements
        for elem in soup.find_all('div', class_='advertisement'):
            elem.decompose()

        # Add custom processing
        for img in soup.find_all('img'):
            # Replace images with alt text
            alt_text = img.get('alt', 'Image')
            img.replace_with(f"[{alt_text}]")

        return str(soup)

    @staticmethod
    def postprocess(markdown: str) -> str:
        """Postprocess converted markdown."""
        import re

        # Clean up extra newlines
        markdown = re.sub(r'\n{3,}', '\n\n', markdown)

        # Add custom formatting
        markdown = re.sub(r'^#', '##', markdown, flags=re.MULTILINE)

        return markdown

    @classmethod
    def convert(cls, html: str, format: str = 'md') -> Optional[str]:
        """Full pipeline conversion."""
        # Preprocess
        html = cls.preprocess(html)

        # Convert
        result = main.convert_html_to_output(html, format, 'html-to-text')

        if result and format == 'md':
            # Postprocess
            result = cls.postprocess(result)

        return result

# Usage
pipeline = ContentPipeline()
html = "<div class='advertisement'>Ad</div><h1>Title</h1><p>Content</p>"
markdown = pipeline.convert(html)
print(markdown)
```

## Extending the API

### Adding a New Engine

```python
def convert_html_to_output_custom(html_string: str, output_format: str) -> Optional[str]:
    """Custom conversion engine implementation."""

    if not html_string:
        return None

    try:
        # Your custom conversion logic
        if output_format == 'md':
            # Custom markdown conversion
            from markdown import markdown
            result = custom_html_to_markdown(html_string)
        else:
            # Custom text conversion
            from html2text import html2text
            result = html2text(html_string)

        return result
    except Exception as e:
        logging.error(f"Custom engine error: {e}")
        return None

# Register the new engine
def convert_html_to_output_extended(html_string: str, output_format: str, engine: str) -> Optional[str]:
    """Extended dispatcher with custom engine."""

    if engine == 'custom':
        return convert_html_to_output_custom(html_string, output_format)
    else:
        return main.convert_html_to_output(html_string, output_format, engine)
```

### Adding Output Formats

```python
def add_rst_support():
    """Add ReStructuredText output support."""

    # Monkey-patch the Pandoc converter
    original_pandoc = main.convert_html_to_output_pandoc

    def extended_pandoc(html_string: str, output_format: str) -> Optional[str]:
        if output_format == 'rst':
            # ReStructuredText conversion
            command = ['pandoc', '-f', 'html', '-t', 'rst']
            # ... subprocess logic ...
            return result
        else:
            return original_pandoc(html_string, output_format)

    main.convert_html_to_output_pandoc = extended_pandoc

# Use the extended functionality
add_rst_support()
result = main.convert_html_to_output(html, 'rst', 'pandoc')
```

### Creating Plugins

```python
class ConverterPlugin:
    """Base class for converter plugins."""

    def preprocess(self, html: str) -> str:
        """Override to add preprocessing."""
        return html

    def postprocess(self, output: str, format: str) -> str:
        """Override to add postprocessing."""
        return output

    def score_modifier(self, tag, score: int) -> int:
        """Override to modify content scoring."""
        return score

class WikipediaPlugin(ConverterPlugin):
    """Plugin for Wikipedia-specific processing."""

    def preprocess(self, html: str) -> str:
        soup = BeautifulSoup(html, 'html5lib')

        # Remove Wikipedia-specific elements
        for elem in soup.find_all('div', class_=['navbox', 'metadata']):
            elem.decompose()

        return str(soup)

    def score_modifier(self, tag, score: int) -> int:
        # Boost score for Wikipedia content divs
        if tag.get('id') == 'mw-content-text':
            score += 500
        return score

# Apply plugin
plugin = WikipediaPlugin()
html = plugin.preprocess(raw_html)
# ... continue with conversion
```

---

[← Back to Configuration](../guides/CONFIGURATION.md) | [Next: Architecture →](../technical/ARCHITECTURE.md)