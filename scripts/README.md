# Data Extraction Scripts

## Overview
This directory contains scripts for extracting and processing data from converted HTML files.

## Scripts

### extract_sections.py
Extracts specific line ranges from combined podcast transcripts based on CSV instructions.

#### Purpose
- Reads line ranges from `data/Extraction.csv`
- Extracts specified sections from `data/Podcast1+2+3+4+5.md`
- Combines all extracted sections into `data/Extracted.md`
- Generates extraction report with statistics

#### Usage
```bash
python scripts/extract_sections.py
```

#### Input Files
- `data/Extraction.csv` - Contains FROM and TO line numbers for extraction
- `data/Podcast1+2+3+4+5.md` - Combined podcast transcripts (source file)

#### Output Files
- `data/Extracted.md` - All extracted sections combined
- `data/extraction_report.txt` - Detailed extraction statistics and validation

#### Features
- Validates line ranges before extraction
- Handles empty rows in CSV gracefully
- Tracks extraction progress
- Generates comprehensive report
- Detects overlapping sections
- Provides extraction statistics

#### Example Output
```
============================================================
PODCAST TRANSCRIPT EXTRACTION TOOL
============================================================

Step 1: Parsing CSV ranges...
Parsed 62 valid ranges from CSV

Step 2: Reading source file...
Read 111,998 lines from source file

Step 3: Extracting sections...
[Progress details...]

Step 4: Writing output file...
Output written to: data/Extracted.md
Output file size: 1,771,836 bytes (1.69 MB)

Step 5: Generating report...
Report generated: data/extraction_report.txt

============================================================
EXTRACTION COMPLETE!
============================================================
```

## Requirements
- Python 3.7+
- Standard library only (csv, os, sys, datetime, pathlib)

## Notes
- The script handles UTF-8 with BOM encoding
- Line numbers in CSV are 1-based (matching text editor line numbers)
- Overlapping sections are detected and reported but still extracted