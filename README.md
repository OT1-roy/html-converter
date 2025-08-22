# HTML to Markdown/Text Converter

A robust, production-ready utility to batch-convert HTML files into clean, readable Markdown or plain text files. Specifically optimized for preparing datasets for Large Language Model (LLM) training.

## Key Features

- **Intelligent Content Extraction:** Uses a scoring heuristic to analyze HTML files and isolate primary article content, automatically discarding boilerplate like headers, footers, and navigation
- **Surgical Cleaning for LLM Data:** Reconstructs core content using a whitelist of semantically valuable tags (`<p>`, `<h1>`, `<ul>`, etc.), removing structural noise while preserving meaning  
- **Dual Conversion Engines:**
  - **html-to-text Engine:** Enterprise-grade HTML parser with advanced parsing capabilities (default)
  - **Pandoc Engine:** Battle-tested, reliable conversion with proven output quality
- **Dual Output Formats:**
  - **Markdown (`.md`):** Preserves document structure (headings, lists, links)
  - **Plain Text (`.txt`):** Generates pure, unformatted text for foundational language modeling
- **Robust Error Handling:** Intelligent fallback to `<body>` conversion when no high-quality content blocks are found, with comprehensive per-file exception handling
- **Engine Selection:** Choose between proven reliability (Pandoc) or advanced parsing (html-to-text) based on your needs
- **Automatic File Splitting:** Splits output into manageable files (default 2MB limit)
- **Progress Tracking:** Real-time progress bar with `tqdm`
- **Comprehensive Logging:** Detailed log files for debugging and review with engine selection tracking
- **Smart Dependency Management:** Automatic dependency checking based on selected conversion engine

## Prerequisites

### Required
- **Python 3.7+**: Download from [python.org](https://www.python.org/downloads/)

### Conversion Engines (Choose One or Both)

#### html-to-text Engine (Default)
- **Node.js**: Required for html-to-text packages. Download from [nodejs.org](https://nodejs.org/)
- **Install both packages**:
  ```bash
  npm install -g @html-to/text-cli    # For plain text output
  npm install -g html-to-md           # For Markdown output
  ```
  - Verify installation: `html-to-text --version`
  - **Recommended for**: Advanced HTML parsing, complex document structures
  - **Note**: Uses different libraries optimized for each output format

#### Pandoc Engine (Alternative)
- **Pandoc**: Battle-tested document converter. Install from [pandoc.org/installing.html](https://pandoc.org/installing.html)
  - Verify installation: `pandoc --version`
  - **Recommended for**: Reliable, proven conversion quality

## Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd html_converter
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
    

## Usage

### Basic Command Structure

```bash
python main.py INPUT_DIRECTORY OUTPUT_DIRECTORY [--format FORMAT] [--engine ENGINE]
```

**Arguments:**
- `INPUT_DIRECTORY`: Path to folder containing HTML files
- `OUTPUT_DIRECTORY`: Path where converted files will be saved  
- `--format`: Output format (`md` for Markdown, `txt` for plain text). Default: `md`
- `--engine`: Conversion engine (`html-to-text` or `pandoc`). Default: `html-to-text`

### Examples

#### Basic Usage (Default: html-to-text Engine + Markdown)
```bash
python main.py ./html_files ./output
```

#### Engine Selection
```bash
# Use html-to-text engine (enterprise parsing, default)
python main.py ./html_files ./output --engine html-to-text

# Use Pandoc engine (reliable, battle-tested)
python main.py ./html_files ./output --engine pandoc
```

#### Output Format Selection
```bash
# Convert to plain text with html-to-text
python main.py ./html_files ./output --format txt --engine html-to-text

# Convert to Markdown with Pandoc
python main.py ./html_files ./output --format md --engine pandoc
```

#### Cross-platform Paths
```bash
# Windows
python main.py C:\Data\HTML C:\Data\Output --engine html-to-text

# macOS/Linux  
python main.py /home/user/html_files /home/user/output --engine pandoc
```

### Engine Selection Guide

| Use Case | Recommended Engine | Why |
|----------|-------------------|-----|
| **General ML datasets** | `html-to-text` | Advanced parsing, format-optimized libraries (default) |
| **Complex HTML documents** | `html-to-text` | Enterprise-grade parsing, superior structure handling |
| **Large-scale processing** | `pandoc` | Lower resource usage, faster processing |
| **Scientific/Technical content** | `html-to-text` | Superior table and list processing with proper formatting |
| **Legacy/Simple setups** | `pandoc` | Single dependency, proven reliability |

### Output

The script creates:
- Converted files in the specified output directory
- A detailed log file (e.g., `run_html_files.log`) with engine selection details
- A summary report showing processing statistics including which engine was used

## How It Works

1. **Engine Selection**: Chooses conversion engine based on user preference and dependency availability
2. **Content Detection**: Analyzes HTML structure to identify main content areas using a scoring algorithm
3. **Content Extraction**: Extracts the highest-scoring content block (article, main, div, or section)
4. **HTML Cleaning**: Removes unwanted tags while preserving semantic structure
5. **Format Conversion**: Uses selected engine (Pandoc or html-to-text) to convert cleaned HTML to desired format
6. **File Management**: Automatically splits large outputs and manages file naming

## Configuration

Key settings in `main.py`:
- `MAX_FILE_SIZE_BYTES`: Maximum output file size (default: 2MB)
- `MIN_CONTENT_SCORE`: Minimum score for content to be considered valid (default: 50)
- `ALLOWED_TAGS`: HTML tags preserved during cleaning

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/improvement`)
3. Make your changes
4. Add tests if applicable
5. Commit your changes (`git commit -am 'Add new feature'`)
6. Push to the branch (`git push origin feature/improvement`)
7. Create a Pull Request

## License

This project is licensed under the MIT License - see the [License](License) file for details.

## Acknowledgments

- Built with [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/) for HTML parsing
- Uses [Pandoc](https://pandoc.org/) for format conversion
- Progress tracking with [tqdm](https://github.com/tqdm/tqdm)