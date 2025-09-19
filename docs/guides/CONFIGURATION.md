# Configuration Guide

![Configuration](https://img.shields.io/badge/config--options-15%2B-blue)
![Customizable](https://img.shields.io/badge/customizable-yes-green)
![Formats](https://img.shields.io/badge/formats-YAML%20%7C%20JSON%20%7C%20CLI-orange)

## Table of Contents

- [Configuration Overview](#configuration-overview)
- [Command-Line Arguments](#command-line-arguments)
- [Configuration Files](#configuration-files)
- [Environment Variables](#environment-variables)
- [Engine Configuration](#engine-configuration)
- [Output Configuration](#output-configuration)
- [Content Extraction Settings](#content-extraction-settings)
- [Logging Configuration](#logging-configuration)
- [Advanced Settings](#advanced-settings)
- [Configuration Examples](#configuration-examples)
- [Best Practices](#best-practices)

## Configuration Overview

The HTML Converter can be configured through multiple methods, with the following precedence:

1. **Command-line arguments** (highest priority)
2. **Configuration files** (`.htmlconverter.yaml`, `.htmlconverter.json`)
3. **Environment variables**
4. **Default values** (lowest priority)

### Quick Configuration

```bash
# Basic configuration via CLI
python main.py input/ output/ --format md --engine html-to-text

# Using environment variables
export HTML_CONVERTER_ENGINE=pandoc
export HTML_CONVERTER_FORMAT=txt
python main.py input/ output/

# Using config file
echo "engine: pandoc" > .htmlconverter.yaml
echo "format: md" >> .htmlconverter.yaml
python main.py input/ output/
```

## Command-Line Arguments

### Core Arguments

| Argument | Type | Required | Default | Description |
|----------|------|----------|---------|-------------|
| `input_dir` | string | Yes | - | Directory containing HTML files |
| `output_dir` | string | Yes | - | Directory for output files |
| `--format` | choice | No | `md` | Output format (`md` or `txt`) |
| `--engine` | choice | No | `html-to-text` | Conversion engine |
| `--version` | flag | No | - | Show version and exit |
| `--help` | flag | No | - | Show help message |

### Extended Arguments (Future)

```bash
# These arguments are planned for future releases
--config FILE           # Specify configuration file
--max-size SIZE         # Maximum output file size
--min-score SCORE       # Minimum content score
--tags TAGS             # Comma-separated allowed tags
--encoding ENCODING     # Input file encoding
--parallel N            # Number of parallel workers
--quiet                 # Suppress progress output
--verbose               # Enable verbose logging
--dry-run               # Preview without conversion
```

### Argument Details

#### `--format` Output Format

```bash
# Markdown output (default)
python main.py input/ output/ --format md

# Plain text output
python main.py input/ output/ --format txt

# Format characteristics:
# - md: Preserves structure, links, formatting
# - txt: Pure text, no formatting, ideal for NLP
```

#### `--engine` Conversion Engine

```bash
# html-to-text engine (default) - Fast, modern
python main.py input/ output/ --engine html-to-text

# Pandoc engine - Accurate, comprehensive
python main.py input/ output/ --engine pandoc

# Engine comparison:
# - html-to-text: 2x faster, Node.js required
# - pandoc: More accurate, single binary
```

## Configuration Files

### YAML Configuration

Create `.htmlconverter.yaml` in your project root:

```yaml
# .htmlconverter.yaml
# HTML Converter Configuration

# Conversion settings
engine: html-to-text  # or pandoc
format: md           # or txt

# Output settings
output:
  max_file_size_mb: 2
  file_pattern: "{folder}_output_{number}.{format}"
  split_files: true
  encoding: utf-8

# Content extraction
extraction:
  min_content_score: 50
  allowed_tags:
    - p
    - h1
    - h2
    - h3
    - h4
    - h5
    - h6
    - ul
    - ol
    - li
    - blockquote
    - pre
    - code
    - table
    - tr
    - td
    - th
    - strong
    - em
    - a
  remove_tags:
    - script
    - style
    - nav
    - footer
    - header
    - aside
    - form

# Logging
logging:
  level: INFO  # DEBUG, INFO, WARNING, ERROR, CRITICAL
  file: true
  console: true
  format: "%(asctime)s - %(levelname)s - %(message)s"

# Engine-specific settings
engines:
  pandoc:
    markdown_variant: markdown-smart
    wrap: none
    columns: 9999
    standalone: false
  html_to_text:
    word_wrap: false
    ignore_images: true
    ignore_links: false
    single_new_line: false

# Performance
performance:
  batch_size: 100
  parallel_workers: 4
  memory_limit_mb: 1024
```

### JSON Configuration

Alternative `.htmlconverter.json` format:

```json
{
  "engine": "html-to-text",
  "format": "md",
  "output": {
    "max_file_size_mb": 2,
    "file_pattern": "{folder}_output_{number}.{format}",
    "split_files": true,
    "encoding": "utf-8"
  },
  "extraction": {
    "min_content_score": 50,
    "allowed_tags": ["p", "h1", "h2", "h3", "ul", "ol", "li", "a"],
    "remove_tags": ["script", "style", "nav", "footer"]
  },
  "logging": {
    "level": "INFO",
    "file": true,
    "console": true
  },
  "engines": {
    "pandoc": {
      "markdown_variant": "markdown-smart"
    },
    "html_to_text": {
      "word_wrap": false
    }
  }
}
```

### Loading Configuration

```python
# config_loader.py
import yaml
import json
from pathlib import Path

def load_config(config_file=None):
    """Load configuration from file."""

    # Default configuration
    config = {
        'engine': 'html-to-text',
        'format': 'md',
        'output': {
            'max_file_size_mb': 2,
            'encoding': 'utf-8'
        },
        'extraction': {
            'min_content_score': 50
        }
    }

    # Search for config files
    if not config_file:
        for name in ['.htmlconverter.yaml', '.htmlconverter.yml', '.htmlconverter.json']:
            if Path(name).exists():
                config_file = name
                break

    if config_file:
        with open(config_file, 'r') as f:
            if config_file.endswith('.json'):
                file_config = json.load(f)
            else:
                file_config = yaml.safe_load(f)

        # Merge configurations
        config.update(file_config)

    return config

# Usage
config = load_config()
engine = config['engine']
```

## Environment Variables

### Supported Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `HTML_CONVERTER_ENGINE` | Conversion engine | `pandoc` |
| `HTML_CONVERTER_FORMAT` | Output format | `txt` |
| `HTML_CONVERTER_MAX_SIZE` | Max file size (bytes) | `5242880` |
| `HTML_CONVERTER_MIN_SCORE` | Min content score | `25` |
| `HTML_CONVERTER_LOG_LEVEL` | Logging level | `DEBUG` |
| `HTML_CONVERTER_CONFIG` | Config file path | `/etc/converter.yaml` |
| `HTML_CONVERTER_PARALLEL` | Parallel workers | `4` |
| `HTML_CONVERTER_ENCODING` | File encoding | `utf-8` |

### Setting Environment Variables

```bash
# Linux/macOS
export HTML_CONVERTER_ENGINE=pandoc
export HTML_CONVERTER_FORMAT=txt
export HTML_CONVERTER_LOG_LEVEL=DEBUG

# Windows (Command Prompt)
set HTML_CONVERTER_ENGINE=pandoc
set HTML_CONVERTER_FORMAT=txt

# Windows (PowerShell)
$env:HTML_CONVERTER_ENGINE = "pandoc"
$env:HTML_CONVERTER_FORMAT = "txt"

# In .env file
HTML_CONVERTER_ENGINE=pandoc
HTML_CONVERTER_FORMAT=txt
HTML_CONVERTER_MIN_SCORE=30
```

### Using in Python

```python
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Access configuration
engine = os.getenv('HTML_CONVERTER_ENGINE', 'html-to-text')
format = os.getenv('HTML_CONVERTER_FORMAT', 'md')
min_score = int(os.getenv('HTML_CONVERTER_MIN_SCORE', '50'))
```

## Engine Configuration

### html-to-text Engine

```yaml
# Specific configuration for html-to-text engine
engines:
  html_to_text:
    # Text formatting
    word_wrap: false        # Disable word wrapping
    single_new_line: false  # Use double newlines between paragraphs

    # Content filtering
    ignore_images: true     # Don't include image alt text
    ignore_links: false     # Include link URLs
    ignore_emphasis: false  # Preserve bold/italic

    # Table formatting
    tables: true            # Include tables
    uppercase_headings: false  # Don't uppercase headings

    # List formatting
    list_style: "-"         # Use dash for unordered lists

    # Link formatting
    link_brackets: ["[", "]"]  # Format for links
    hide_link_href: false   # Show link URLs

    # Code blocks
    preserve_code: true     # Preserve code formatting
```

### Pandoc Engine

```yaml
# Specific configuration for Pandoc
engines:
  pandoc:
    # Input settings
    from_format: html       # Source format

    # Markdown output settings
    to_format_md: markdown-smart  # Smart quotes, dashes
    markdown_extensions:
      - +pipe_tables        # Enable pipe tables
      - +backtick_code_blocks  # Enable code blocks
      - +fenced_code_attributes  # Code block attributes
      - -raw_html          # Disable raw HTML

    # Text output settings
    to_format_txt: plain+smart
    wrap: none             # No wrapping
    columns: 9999          # Effectively infinite line width

    # General settings
    standalone: false      # Not standalone document
    preserve_tabs: false   # Convert tabs to spaces
    tab_stop: 4           # Tab width

    # Filters (if needed)
    filters: []           # Pandoc filters to apply
    lua_filters: []       # Lua filters to apply
```

### Engine-Specific Commands

```python
# Custom engine commands
def get_engine_command(engine, format, config):
    """Generate engine-specific command."""

    if engine == 'pandoc':
        cmd = ['pandoc', '-f', 'html']

        if format == 'md':
            cmd.extend(['-t', config['engines']['pandoc']['to_format_md']])
        else:
            cmd.extend(['-t', config['engines']['pandoc']['to_format_txt']])
            cmd.extend(['--wrap', config['engines']['pandoc']['wrap']])

        return cmd

    elif engine == 'html-to-text':
        if format == 'txt':
            return ['html-to-text', '--wordwrap=false']
        else:
            return ['node', 'html-to-md-cli.js']
```

## Output Configuration

### File Naming Patterns

```yaml
output:
  # Naming pattern variables:
  # {folder} - Input folder name
  # {number} - Sequential number
  # {format} - Output format (md/txt)
  # {date} - Current date
  # {time} - Current time
  file_pattern: "{folder}_output_{number}.{format}"

  # Examples:
  # "{folder}_{date}_{number}.{format}" -> docs_2024-01-15_1.md
  # "converted_{folder}_{number}.{format}" -> converted_docs_1.md
  # "{date}/{folder}_{number}.{format}" -> 2024-01-15/docs_1.md
```

### File Splitting

```yaml
output:
  # File splitting configuration
  split_files: true           # Enable file splitting
  max_file_size_mb: 2         # Maximum size per file
  max_file_size_bytes: 2097152  # Alternative: specify in bytes

  # Splitting behavior
  split_strategy: size        # 'size' or 'count'
  files_per_output: 100       # If strategy is 'count'

  # Boundary handling
  preserve_boundaries: true   # Don't split mid-document
  boundary_marker: "---"      # Marker between documents
```

### Encoding Settings

```yaml
output:
  # Output encoding
  encoding: utf-8            # Output file encoding
  bom: false                 # Don't add BOM to UTF-8 files
  normalize_unicode: true    # Normalize Unicode (NFC)

  # Line endings
  line_ending: auto          # auto, lf, crlf, cr
  # auto: Use system default
  # lf: Unix/Linux/macOS (\n)
  # crlf: Windows (\r\n)
  # cr: Classic Mac (\r)
```

## Content Extraction Settings

### Scoring Configuration

```python
# In main.py or config
extraction:
  # Content scoring thresholds
  min_content_score: 50      # Minimum score to extract
  fallback_to_body: true     # Use <body> if no good content

  # Scoring weights
  scoring_weights:
    text_length: 1.0        # Weight for text length
    paragraph_count: 25     # Points per paragraph
    link_density_penalty: -100  # Penalty for high link density

  # Class/ID scoring
  positive_patterns:
    - article
    - content
    - post
    - body
    - main
    - story
    - entry
  negative_patterns:
    - comment
    - sidebar
    - footer
    - menu
    - nav
    - ad
    - promo
```

### Tag Management

```yaml
extraction:
  # Tags to preserve in output
  allowed_tags:
    - p
    - h1
    - h2
    - h3
    - h4
    - h5
    - h6
    - ul
    - ol
    - li
    - blockquote
    - pre
    - code
    - table
    - strong
    - em
    - a

  # Tags to remove before processing
  remove_tags:
    - script
    - style
    - nav
    - footer
    - header
    - aside
    - form
    - iframe
    - object
    - embed

  # Tags to unwrap (keep content, remove tag)
  unwrap_tags:
    - span
    - font
    - center
```

## Logging Configuration

### Log Levels

```yaml
logging:
  # Log level (in order of severity)
  # DEBUG - Detailed diagnostic information
  # INFO - General informational messages
  # WARNING - Warning messages
  # ERROR - Error messages
  # CRITICAL - Critical problems
  level: INFO

  # Output destinations
  file: true                 # Log to file
  console: true              # Log to console

  # File configuration
  file_name: "run_{input_folder}.log"
  file_mode: w              # 'w' for overwrite, 'a' for append
  max_file_size_mb: 10      # Rotate after this size
  backup_count: 3           # Keep this many backup logs

  # Console configuration
  console_level: ERROR      # Console can have different level
  colorize: true            # Colorize console output

  # Format
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
  date_format: "%Y-%m-%d %H:%M:%S"
```

### Custom Logging

```python
import logging
import sys
from logging.handlers import RotatingFileHandler

def setup_custom_logging(config):
    """Setup logging based on configuration."""

    # Create logger
    logger = logging.getLogger('html_converter')
    logger.setLevel(getattr(logging, config['logging']['level']))

    # File handler with rotation
    if config['logging']['file']:
        file_handler = RotatingFileHandler(
            config['logging']['file_name'],
            maxBytes=config['logging']['max_file_size_mb'] * 1024 * 1024,
            backupCount=config['logging']['backup_count']
        )
        file_handler.setLevel(getattr(logging, config['logging']['level']))
        file_formatter = logging.Formatter(
            config['logging']['format'],
            datefmt=config['logging']['date_format']
        )
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

    # Console handler
    if config['logging']['console']:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(
            getattr(logging, config['logging'].get('console_level', 'ERROR'))
        )
        console_formatter = logging.Formatter('%(levelname)s: %(message)s')
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)

    return logger
```

## Advanced Settings

### Performance Tuning

```yaml
performance:
  # Parallel processing
  parallel_processing: true  # Enable parallel processing
  parallel_workers: 4        # Number of workers (0 = auto)
  chunk_size: 50             # Files per chunk

  # Memory management
  memory_limit_mb: 1024      # Maximum memory usage
  gc_threshold: 100          # Run garbage collection after N files
  clear_cache: true          # Clear BeautifulSoup cache

  # I/O optimization
  buffer_size: 8192          # Read buffer size
  use_mmap: false            # Use memory-mapped files (large files)

  # Timeout settings
  conversion_timeout: 300    # Timeout per file (seconds)
  total_timeout: 3600        # Total job timeout (seconds)
```

### Error Handling

```yaml
error_handling:
  # Error behavior
  continue_on_error: true    # Continue processing on errors
  max_retries: 3            # Retry failed conversions
  retry_delay: 1            # Delay between retries (seconds)

  # Error reporting
  detailed_errors: true     # Include stack traces
  save_failed_list: true    # Save list of failed files
  failed_list_file: "failed_files.txt"

  # Recovery
  checkpoint_interval: 100  # Save progress every N files
  resume_from_checkpoint: true  # Resume interrupted jobs
```

### Filtering and Selection

```yaml
filtering:
  # File selection
  include_patterns:
    - "*.html"
    - "*.htm"
    - "*.xhtml"
  exclude_patterns:
    - "*_test.html"
    - "*_backup.html"

  # Size filters
  min_file_size_kb: 1       # Skip files smaller than this
  max_file_size_mb: 100     # Skip files larger than this

  # Content filters
  min_word_count: 50        # Skip if fewer words
  required_elements:        # Skip if missing these
    - p                    # Must have paragraphs

  # Date filters (if dates in filename)
  after_date: "2024-01-01"
  before_date: "2024-12-31"
```

## Configuration Examples

### Example 1: High-Performance Configuration

```yaml
# .htmlconverter.yaml for maximum speed
engine: html-to-text
format: txt

performance:
  parallel_workers: 8
  chunk_size: 100
  memory_limit_mb: 2048

extraction:
  min_content_score: 30  # Lower threshold for speed

logging:
  level: WARNING  # Less logging overhead
  file: false    # No file logging
  console: true

error_handling:
  continue_on_error: true
  max_retries: 1  # Fewer retries
```

### Example 2: High-Quality Configuration

```yaml
# .htmlconverter.yaml for maximum quality
engine: pandoc
format: md

extraction:
  min_content_score: 75  # Higher threshold
  fallback_to_body: false  # No fallback

engines:
  pandoc:
    markdown_variant: markdown-smart+footnotes+pipe_tables

error_handling:
  continue_on_error: false  # Stop on errors
  max_retries: 5

logging:
  level: DEBUG  # Detailed logging
```

### Example 3: Memory-Constrained Configuration

```yaml
# .htmlconverter.yaml for low-memory systems
performance:
  parallel_workers: 1  # Single-threaded
  chunk_size: 10      # Small chunks
  memory_limit_mb: 256
  gc_threshold: 10    # Aggressive garbage collection

output:
  max_file_size_mb: 1  # Smaller output files

error_handling:
  checkpoint_interval: 10  # Frequent checkpoints
```

### Example 4: Batch Processing Configuration

```yaml
# .htmlconverter.yaml for batch processing
performance:
  parallel_workers: 4
  chunk_size: 500

filtering:
  min_file_size_kb: 10
  max_file_size_mb: 50
  min_word_count: 100

output:
  split_strategy: count
  files_per_output: 1000

error_handling:
  continue_on_error: true
  save_failed_list: true
  resume_from_checkpoint: true
```

## Best Practices

### Configuration Management

1. **Use Version Control**
   ```bash
   # Track configuration changes
   git add .htmlconverter.yaml
   git commit -m "Update extraction settings"
   ```

2. **Environment-Specific Configs**
   ```bash
   # Development
   cp .htmlconverter.dev.yaml .htmlconverter.yaml

   # Production
   cp .htmlconverter.prod.yaml .htmlconverter.yaml
   ```

3. **Validate Configuration**
   ```python
   # validate_config.py
   import yaml
   import jsonschema

   def validate_config(config_file):
       with open(config_file) as f:
           config = yaml.safe_load(f)

       schema = {
           "type": "object",
           "properties": {
               "engine": {"enum": ["pandoc", "html-to-text"]},
               "format": {"enum": ["md", "txt"]}
           }
       }

       jsonschema.validate(config, schema)
       print("✅ Configuration valid")
   ```

### Performance Optimization

1. **Profile Before Optimizing**
   ```bash
   # Test different configurations
   time python main.py input/ output1/ --engine html-to-text
   time python main.py input/ output2/ --engine pandoc
   ```

2. **Start Conservative**
   ```yaml
   # Start with safe defaults
   performance:
     parallel_workers: 2
     memory_limit_mb: 512

   # Then increase based on results
   ```

3. **Monitor Resource Usage**
   ```python
   import psutil

   def monitor_resources():
       process = psutil.Process()
       print(f"Memory: {process.memory_info().rss / 1024 / 1024:.2f} MB")
       print(f"CPU: {process.cpu_percent()}%")
   ```

### Security Considerations

1. **Sanitize Configuration**
   ```python
   # Don't allow arbitrary code execution
   def safe_load_config(file):
       with open(file) as f:
           # Use safe_load, not load
           return yaml.safe_load(f)
   ```

2. **Validate Paths**
   ```python
   from pathlib import Path

   def validate_paths(config):
       # Ensure paths are within allowed directories
       output_dir = Path(config['output_dir']).resolve()
       if not output_dir.is_relative_to(Path.cwd()):
           raise ValueError("Output directory must be within current directory")
   ```

3. **Limit Resource Usage**
   ```yaml
   # Prevent resource exhaustion
   performance:
     memory_limit_mb: 1024
     total_timeout: 3600
   ```

---

[← Back to Troubleshooting](TROUBLESHOOTING.md) | [Next: API Documentation →](../api/API.md)