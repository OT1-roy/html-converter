# HTML to Markdown/Text Converter

A robust, production-ready utility to batch-convert HTML files into clean, readable Markdown or plain text files. Specifically optimized for preparing datasets for Large Language Model (LLM) training.

## Key Features

- **Intelligent Content Extraction:** Uses a scoring heuristic to analyze HTML files and isolate primary article content, automatically discarding boilerplate like headers, footers, and navigation
- **Surgical Cleaning for LLM Data:** Reconstructs core content using a whitelist of semantically valuable tags (`<p>`, `<h1>`, `<ul>`, etc.), removing structural noise while preserving meaning  
- **Dual Output Formats:**
  - **Markdown (`.md`):** Preserves document structure (headings, lists, links)
  - **Plain Text (`.txt`):** Generates pure, unformatted text for foundational language modeling
- **Robust Error Handling:** Intelligent fallback to `<body>` conversion when no high-quality content blocks are found, with comprehensive per-file exception handling
- **High-Quality Conversion:** Uses **Pandoc** for clean, well-formatted output  
- **Automatic File Splitting:** Splits output into manageable files (default 2MB limit)
- **Progress Tracking:** Real-time progress bar with `tqdm`
- **Comprehensive Logging:** Detailed log files for debugging and review
- **Dependency Verification:** Checks for Pandoc installation before processing

## Prerequisites

- **Python 3.7+**: Download from [python.org](https://www.python.org/downloads/)
- **Pandoc**: Required external dependency. Install from [pandoc.org/installing.html](https://pandoc.org/installing.html)
  - Verify installation: `pandoc --version`

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
python main.py INPUT_DIRECTORY OUTPUT_DIRECTORY [--format FORMAT]
```

**Arguments:**
- `INPUT_DIRECTORY`: Path to folder containing HTML files
- `OUTPUT_DIRECTORY`: Path where converted files will be saved  
- `--format`: Output format (`md` for Markdown, `txt` for plain text). Default: `md`

### Examples

**Convert to Markdown (default):**
```bash
python main.py ./html_files ./output
```

**Convert to plain text:**
```bash
python main.py ./html_files ./output --format txt
```

**Cross-platform paths:**
```bash
# Windows
python main.py C:\Data\HTML C:\Data\Output

# macOS/Linux  
python main.py /home/user/html_files /home/user/output
```

### Output

The script creates:
- Converted files in the specified output directory
- A detailed log file (e.g., `run_html_files.log`)
- A summary report showing processing statistics

## How It Works

1. **Content Detection**: Analyzes HTML structure to identify main content areas using a scoring algorithm
2. **Content Extraction**: Extracts the highest-scoring content block (article, main, div, or section)
3. **HTML Cleaning**: Removes unwanted tags while preserving semantic structure
4. **Format Conversion**: Uses Pandoc to convert cleaned HTML to Markdown or plain text
5. **File Management**: Automatically splits large outputs and manages file naming

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