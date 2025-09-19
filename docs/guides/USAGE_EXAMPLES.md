# Usage Examples

![Examples](https://img.shields.io/badge/examples-20%2B-blue)
![Scenarios](https://img.shields.io/badge/scenarios-real--world-green)
![Best Practices](https://img.shields.io/badge/best--practices-included-orange)

## Table of Contents

- [Quick Start](#quick-start)
- [Basic Examples](#basic-examples)
- [Advanced Scenarios](#advanced-scenarios)
- [Real-World Use Cases](#real-world-use-cases)
- [Batch Processing](#batch-processing)
- [Pipeline Integration](#pipeline-integration)
- [Performance Optimization](#performance-optimization)
- [Best Practices](#best-practices)
- [Common Patterns](#common-patterns)
- [Troubleshooting Examples](#troubleshooting-examples)

## Quick Start

### Your First Conversion

```bash
# Simple conversion with default settings
python main.py ./sample_html ./output

# What happens:
# 1. Scans all HTML files in ./sample_html
# 2. Extracts main content using intelligent scoring
# 3. Combines all HTML files into single output
# 4. Converts to Markdown using html-to-text engine
# 5. Saves as single clean file to ./output directory
```

### Important Default Behavior

**The converter automatically combines all input HTML files into a single output file.** This is the default behavior - no special flags needed!

### Essential Commands

```bash
# Convert to Markdown (default)
python main.py input/ output/

# Convert to plain text
python main.py input/ output/ --format txt

# Use Pandoc engine
python main.py input/ output/ --engine pandoc

# Show version
python main.py --version
```

## Basic Examples

### Example 1: Converting a Blog Archive

**Scenario**: You have a directory of blog posts exported as HTML files.

```bash
# Directory structure:
# blog_archive/
# ├── 2024-01-post1.html
# ├── 2024-01-post2.html
# └── 2024-02-post1.html

# Convert to Markdown for migration
python main.py ./blog_archive ./clean_blog --format md

# Result structure:
# clean_blog/
# └── blog_archive_output_1.md  # All posts in one file (if < 2MB)
```

**Sample Output**:
```markdown
---
source: 2024-01-post1.html
title: "My First Blog Post"
---

# My First Blog Post

This is the content of my blog post...

---
source: 2024-01-post2.html
title: "Another Great Post"
---

# Another Great Post

More content here...
```

### Example 2: Extracting Text for NLP

**Scenario**: Preparing text data for natural language processing.

```bash
# Extract plain text without formatting
python main.py ./web_scrape ./nlp_data --format txt --engine html-to-text

# Process specific file types
find ./web_scrape -name "*.htm" -o -name "*.html" | \
  xargs -I {} cp {} ./temp/
python main.py ./temp ./nlp_data --format txt
```

**Output characteristics**:
- No HTML tags or Markdown formatting
- Clean, readable text
- Preserved paragraph structure
- Ready for tokenization

### Example 3: Documentation Migration

**Scenario**: Converting HTML documentation to Markdown for GitHub.

```bash
# Convert documentation with Pandoc for accuracy
python main.py ./html_docs ./markdown_docs --format md --engine pandoc

# Result: GitHub-compatible Markdown files
```

## Advanced Scenarios

### Scenario 1: Processing News Archives

**Challenge**: Convert thousands of news articles while preserving metadata.

```bash
# Step 1: Organize by date
for file in news_archive/*.html; do
  date=$(grep -oP 'date-published="\K[^"]+' "$file" | head -1)
  year=$(echo $date | cut -d'-' -f1)
  mkdir -p organized/$year
  cp "$file" organized/$year/
done

# Step 2: Convert by year
for year in organized/*/; do
  python main.py "$year" "output/$(basename $year)" --format md
done
```

### Scenario 2: Academic Paper Conversion

**Challenge**: Convert research papers with complex formatting.

```python
#!/usr/bin/env python3
# convert_papers.py

import os
import subprocess
from pathlib import Path

def convert_academic_papers(input_dir, output_dir):
    """
    Convert academic HTML papers with special handling
    for citations, figures, and tables.
    """
    # Use Pandoc for better academic formatting
    cmd = [
        'python', 'main.py',
        input_dir, output_dir,
        '--format', 'md',
        '--engine', 'pandoc'
    ]

    # Run conversion
    result = subprocess.run(cmd, capture_output=True, text=True)

    # Post-process for citations
    for md_file in Path(output_dir).glob('*.md'):
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Fix citation formatting
        content = content.replace('[^', '^[')  # Fix footnote markers

        with open(md_file, 'w', encoding='utf-8') as f:
            f.write(content)

    print(f"Converted {len(list(Path(output_dir).glob('*.md')))} papers")

if __name__ == "__main__":
    convert_academic_papers('./papers_html', './papers_markdown')
```

### Scenario 3: E-book Creation

**Challenge**: Convert web content to e-book format.

```bash
# Step 1: Convert HTML chapters to single Markdown file (automatic combining!)
python main.py ./book_chapters ./book_output --format md
# Result: All chapters combined into book_output_1.md

# Step 2: Convert to EPUB (requires Pandoc)
pandoc book_output/book_output_1.md -o my_ebook.epub \
  --metadata title="My Book" \
  --metadata author="Your Name" \
  --toc
```

### Scenario 4: Podcast Transcription Processing

**Challenge**: Convert 49 podcast transcription HTML files into single Markdown for analysis.

```bash
# Real-world example: Successfully converted 49 podcast HTML files
python main.py C:\Users\royca\Sidekick\Audrey\Morehead_local\HTML_RAW\49Podcast_Transcription \
               C:\Users\royca\Sidekick\Audrey\Morehead_local\Data \
               --format md

# Results:
# - Input: 49 HTML transcription files
# - Output: Single combined file (49Podcast_Transcription_output_1.md)
# - Success rate: 100%
# - All transcriptions merged automatically into one document
```

**Key Benefits**:
- No manual combining needed
- Preserves chronological order
- Ready for further analysis or LLM training
- Handles large combined output gracefully

## Real-World Use Cases

### Use Case 1: Wikipedia Data Processing

**Goal**: Extract Wikipedia articles for machine learning datasets.

```python
#!/usr/bin/env python3
# process_wikipedia.py

import os
import sys
from pathlib import Path

def process_wikipedia_dump(dump_dir):
    """Process Wikipedia HTML dump for ML training."""

    # Configuration for Wikipedia content
    config = {
        'input': dump_dir,
        'output': './wikipedia_clean',
        'format': 'txt',  # Plain text for ML
        'engine': 'html-to-text'  # Fast processing
    }

    # Run conversion
    cmd = f"python main.py {config['input']} {config['output']} " \
          f"--format {config['format']} --engine {config['engine']}"

    print(f"Processing Wikipedia dump from {dump_dir}")
    os.system(cmd)

    # Post-process: Remove short articles
    for txt_file in Path(config['output']).glob('*.txt'):
        with open(txt_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Remove if less than 100 words
        if len(content.split()) < 100:
            txt_file.unlink()
            print(f"Removed short article: {txt_file.name}")

    print("Wikipedia processing complete!")

if __name__ == "__main__":
    process_wikipedia_dump('./wikipedia_html')
```

### Use Case 2: Website Migration

**Goal**: Migrate entire website from HTML to Markdown for static site generator.

```bash
#!/bin/bash
# migrate_website.sh

# Download website
wget -r -np -k -E https://example.com -P ./website_mirror

# Convert to Markdown
python main.py ./website_mirror/example.com ./website_markdown --format md

# Organize for Hugo/Jekyll
mkdir -p site/content
for file in website_markdown/*.md; do
  # Extract date from content
  date=$(grep -m1 'date:' "$file" | cut -d' ' -f2)

  # Move to appropriate directory
  if [[ $file == *"blog"* ]]; then
    mv "$file" site/content/posts/
  elif [[ $file == *"about"* ]]; then
    mv "$file" site/content/pages/
  else
    mv "$file" site/content/
  fi
done

echo "Website migration complete!"
```

### Use Case 3: Legal Document Processing

**Goal**: Convert legal documents while preserving structure.

```python
#!/usr/bin/env python3
# legal_processor.py

import re
import subprocess
from pathlib import Path

class LegalDocumentProcessor:
    def __init__(self):
        self.section_pattern = re.compile(r'Section \d+\.')
        self.article_pattern = re.compile(r'Article [IVXLC]+')

    def process_legal_docs(self, input_dir, output_dir):
        """Process legal documents with special formatting."""

        # Use Pandoc for precise formatting
        cmd = [
            'python', 'main.py',
            input_dir, output_dir,
            '--format', 'md',
            '--engine', 'pandoc'
        ]

        subprocess.run(cmd, check=True)

        # Post-process for legal formatting
        self.format_legal_structure(output_dir)

    def format_legal_structure(self, output_dir):
        """Add legal document structure."""
        for md_file in Path(output_dir).glob('*.md'):
            with open(md_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            formatted_lines = []
            for line in lines:
                # Emphasize section headers
                if self.section_pattern.match(line):
                    line = f"## {line}"
                elif self.article_pattern.match(line):
                    line = f"### {line}"
                formatted_lines.append(line)

            with open(md_file, 'w', encoding='utf-8') as f:
                f.writelines(formatted_lines)

# Usage
processor = LegalDocumentProcessor()
processor.process_legal_docs('./contracts_html', './contracts_markdown')
```

## Batch Processing

### Large-Scale Batch Processing

```python
#!/usr/bin/env python3
# batch_processor.py

import os
import sys
import time
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor
import subprocess

def process_batch(batch_info):
    """Process a single batch of files."""
    batch_num, input_dir, output_dir = batch_info

    batch_output = f"{output_dir}/batch_{batch_num}"
    os.makedirs(batch_output, exist_ok=True)

    cmd = [
        'python', 'main.py',
        input_dir, batch_output,
        '--format', 'md',
        '--engine', 'html-to-text'
    ]

    start = time.time()
    result = subprocess.run(cmd, capture_output=True, text=True)
    duration = time.time() - start

    return {
        'batch': batch_num,
        'duration': duration,
        'success': result.returncode == 0,
        'files_processed': len(list(Path(input_dir).glob('*.html')))
    }

def parallel_batch_processing(main_input_dir, main_output_dir, batch_size=100):
    """Process files in parallel batches."""

    # Organize files into batches
    all_files = list(Path(main_input_dir).glob('*.html'))
    batches = []

    for i in range(0, len(all_files), batch_size):
        batch_num = i // batch_size
        batch_dir = f"temp_batch_{batch_num}"
        os.makedirs(batch_dir, exist_ok=True)

        # Copy files to batch directory
        for file in all_files[i:i+batch_size]:
            os.link(file, f"{batch_dir}/{file.name}")

        batches.append((batch_num, batch_dir, main_output_dir))

    # Process batches in parallel
    with ProcessPoolExecutor(max_workers=4) as executor:
        results = list(executor.map(process_batch, batches))

    # Clean up temp directories
    for batch_num, batch_dir, _ in batches:
        os.system(f"rm -rf {batch_dir}")

    # Report results
    total_files = sum(r['files_processed'] for r in results)
    total_time = sum(r['duration'] for r in results)

    print(f"Processed {total_files} files in {total_time:.2f} seconds")
    print(f"Average: {total_files/total_time:.2f} files/second")

    return results

# Usage
if __name__ == "__main__":
    results = parallel_batch_processing('./huge_dataset', './output', batch_size=500)
```

### Incremental Processing

```bash
#!/bin/bash
# incremental_process.sh

# Keep track of processed files
PROCESSED_LIST="processed_files.txt"
touch "$PROCESSED_LIST"

# Process only new files
for file in input_html/*.html; do
  basename=$(basename "$file")

  # Check if already processed
  if ! grep -q "$basename" "$PROCESSED_LIST"; then
    echo "Processing new file: $basename"

    # Process single file
    python main.py "$(dirname "$file")" ./output --format md

    # Mark as processed
    echo "$basename" >> "$PROCESSED_LIST"
  fi
done
```

## Pipeline Integration

### Integration with Data Pipeline

```python
#!/usr/bin/env python3
# pipeline_integration.py

import luigi
import subprocess
from pathlib import Path

class DownloadHTML(luigi.Task):
    """Download HTML files from source."""
    url = luigi.Parameter()

    def output(self):
        return luigi.LocalTarget('raw_html/')

    def run(self):
        subprocess.run(['wget', '-r', self.url, '-P', 'raw_html/'])

class ConvertToMarkdown(luigi.Task):
    """Convert HTML to Markdown."""
    url = luigi.Parameter()

    def requires(self):
        return DownloadHTML(self.url)

    def output(self):
        return luigi.LocalTarget('markdown_output/')

    def run(self):
        subprocess.run([
            'python', 'main.py',
            'raw_html/', 'markdown_output/',
            '--format', 'md'
        ])

class ProcessMarkdown(luigi.Task):
    """Post-process Markdown files."""
    url = luigi.Parameter()

    def requires(self):
        return ConvertToMarkdown(self.url)

    def output(self):
        return luigi.LocalTarget('final_output/')

    def run(self):
        # Additional processing
        Path('final_output/').mkdir(exist_ok=True)
        # ... processing logic ...

# Run pipeline
if __name__ == '__main__':
    luigi.run(['ProcessMarkdown', '--url', 'https://example.com'])
```

### CI/CD Integration

```yaml
# .github/workflows/convert.yml
name: HTML Conversion Pipeline

on:
  push:
    paths:
      - 'html_source/**'

jobs:
  convert:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v2

    - name: Setup Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.9'

    - name: Setup Node.js
      uses: actions/setup-node@v2
      with:
        node-version: '16'

    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        npm install -g @html-to/text-cli html-to-md

    - name: Convert HTML files
      run: |
        python main.py ./html_source ./converted --format md

    - name: Upload artifacts
      uses: actions/upload-artifact@v2
      with:
        name: converted-markdown
        path: converted/
```

## Performance Optimization

### Memory-Efficient Processing

```python
#!/usr/bin/env python3
# memory_efficient.py

import os
import gc
from pathlib import Path

def process_in_chunks(input_dir, output_dir, chunk_size=50):
    """Process files in memory-efficient chunks."""

    all_files = list(Path(input_dir).glob('*.html'))
    total_files = len(all_files)

    for i in range(0, total_files, chunk_size):
        chunk_files = all_files[i:i+chunk_size]

        # Create temporary directory for chunk
        chunk_dir = f"temp_chunk_{i}"
        os.makedirs(chunk_dir, exist_ok=True)

        # Process chunk
        for file in chunk_files:
            os.link(file, f"{chunk_dir}/{file.name}")

        # Run conversion
        os.system(f"python main.py {chunk_dir} {output_dir} --format md")

        # Clean up
        os.system(f"rm -rf {chunk_dir}")

        # Force garbage collection
        gc.collect()

        print(f"Processed {min(i+chunk_size, total_files)}/{total_files} files")

# Usage
process_in_chunks('./large_dataset', './output', chunk_size=100)
```

### Speed Optimization

```bash
#!/bin/bash
# speed_optimize.sh

# Use html-to-text for speed
echo "Using fast html-to-text engine..."
time python main.py ./input ./output_fast --engine html-to-text

# Compare with Pandoc
echo "Using accurate Pandoc engine..."
time python main.py ./input ./output_accurate --engine pandoc

# Parallel processing with GNU parallel
find ./input -name "*.html" | \
  parallel -j 4 "python main.py {} ./output/{/.}.md --format md"
```

## Best Practices

### 1. Choose the Right Engine

```python
def select_engine(content_type):
    """Select optimal engine based on content type."""

    engine_map = {
        'academic': 'pandoc',        # Better citation handling
        'news': 'html-to-text',       # Faster processing
        'documentation': 'pandoc',    # Better code blocks
        'blog': 'html-to-text',       # Good enough, faster
        'legal': 'pandoc',            # Precise formatting
        'general': 'html-to-text'     # Default to fast
    }

    return engine_map.get(content_type, 'html-to-text')

# Usage
content_type = detect_content_type('./input')
engine = select_engine(content_type)
os.system(f"python main.py ./input ./output --engine {engine}")
```

### 2. Validate Output Quality

```python
#!/usr/bin/env python3
# validate_output.py

def validate_conversion(input_file, output_file):
    """Validate conversion quality."""

    with open(input_file, 'r') as f:
        html_content = f.read()

    with open(output_file, 'r') as f:
        converted_content = f.read()

    # Check for content preservation
    checks = {
        'min_length': len(converted_content) > 100,
        'no_html': '<' not in converted_content,
        'has_content': len(converted_content.split()) > 50,
        'encoding_ok': not any(c in converted_content for c in ['�', '???'])
    }

    return all(checks.values()), checks

# Run validation
success, details = validate_conversion('input.html', 'output.md')
if not success:
    print("Validation failed:", details)
```

### 3. Handle Errors Gracefully

```python
#!/usr/bin/env python3
# error_handling.py

import subprocess
import logging

def safe_convert(input_dir, output_dir, max_retries=3):
    """Convert with error handling and retries."""

    for attempt in range(max_retries):
        try:
            result = subprocess.run(
                ['python', 'main.py', input_dir, output_dir],
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )

            if result.returncode == 0:
                logging.info("Conversion successful")
                return True
            else:
                logging.warning(f"Attempt {attempt + 1} failed: {result.stderr}")

        except subprocess.TimeoutExpired:
            logging.error("Conversion timed out")
        except Exception as e:
            logging.error(f"Unexpected error: {e}")

        if attempt < max_retries - 1:
            logging.info("Retrying...")

    return False

# Usage
if not safe_convert('./input', './output'):
    print("Conversion failed after all retries")
```

## Common Patterns

### Pattern 1: Directory Structure Preservation

```bash
#!/bin/bash
# preserve_structure.sh

# Replicate directory structure
find ./source -type d | while read dir; do
  mkdir -p "./output/${dir#./source/}"
done

# Convert maintaining structure
find ./source -name "*.html" | while read file; do
  dir=$(dirname "$file")
  outdir="./output/${dir#./source/}"
  python main.py "$dir" "$outdir" --format md
done
```

### Pattern 2: Metadata Extraction

```python
#!/usr/bin/env python3
# extract_metadata.py

from bs4 import BeautifulSoup
import json

def extract_and_convert(html_file):
    """Extract metadata before conversion."""

    with open(html_file, 'r') as f:
        soup = BeautifulSoup(f, 'html.parser')

    # Extract metadata
    metadata = {
        'title': soup.find('title').text if soup.find('title') else '',
        'author': soup.find('meta', {'name': 'author'})['content']
                  if soup.find('meta', {'name': 'author'}) else '',
        'date': soup.find('meta', {'name': 'date'})['content']
                if soup.find('meta', {'name': 'date'}) else '',
    }

    # Save metadata
    with open(f"{html_file}.meta.json", 'w') as f:
        json.dump(metadata, f, indent=2)

    # Convert HTML
    os.system(f"python main.py {html_file} output/ --format md")
```

### Pattern 3: Content Filtering

```python
#!/usr/bin/env python3
# filter_content.py

def convert_with_filter(input_dir, output_dir, min_words=100):
    """Convert only files meeting criteria."""

    from bs4 import BeautifulSoup

    # Pre-filter files
    valid_files = []
    for html_file in Path(input_dir).glob('*.html'):
        with open(html_file, 'r') as f:
            soup = BeautifulSoup(f, 'html.parser')
            text = soup.get_text()

            if len(text.split()) >= min_words:
                valid_files.append(html_file)

    # Convert valid files
    if valid_files:
        temp_dir = "temp_filtered"
        os.makedirs(temp_dir, exist_ok=True)

        for file in valid_files:
            os.link(file, f"{temp_dir}/{file.name}")

        os.system(f"python main.py {temp_dir} {output_dir} --format md")

        # Cleanup
        os.system(f"rm -rf {temp_dir}")
```

## Troubleshooting Examples

### Issue: Empty Output Files

```bash
# Debug with verbose logging
python main.py input/ output/ --format md 2>&1 | tee conversion.log

# Check log for errors
grep -i error conversion.log
grep -i warning conversion.log

# Test with single file
python main.py single_test.html test_output/ --format md
```

### Issue: Encoding Problems

```python
#!/usr/bin/env python3
# fix_encoding.py

import chardet
from pathlib import Path

def convert_with_encoding_detection(input_dir, output_dir):
    """Handle files with unknown encoding."""

    for html_file in Path(input_dir).glob('*.html'):
        # Detect encoding
        with open(html_file, 'rb') as f:
            raw_data = f.read()
            result = chardet.detect(raw_data)
            encoding = result['encoding']

        print(f"Detected encoding for {html_file.name}: {encoding}")

        # Re-encode to UTF-8
        with open(html_file, 'r', encoding=encoding) as f:
            content = f.read()

        utf8_file = f"temp_{html_file.name}"
        with open(utf8_file, 'w', encoding='utf-8') as f:
            f.write(content)

        # Convert
        os.system(f"python main.py {utf8_file} {output_dir} --format md")

        # Cleanup
        os.remove(utf8_file)
```

### Issue: Memory Errors

```bash
#!/bin/bash
# low_memory_process.sh

# Process files one at a time
for file in input/*.html; do
  echo "Processing: $file"

  # Create temp directory with single file
  mkdir -p temp_single
  cp "$file" temp_single/

  # Process with limited memory
  ulimit -v 500000  # Limit to 500MB
  python main.py temp_single/ output/ --format md

  # Clean up
  rm -rf temp_single

  # Give system time to recover
  sleep 1
done
```

## Tips and Tricks

### Quick Tips

1. **Use `--engine html-to-text` for speed**
2. **Use `--engine pandoc` for accuracy**
3. **Process in batches for large datasets**
4. **Check logs for detailed error information**
5. **Test with small samples first**

### Performance Tips

```bash
# Benchmark different approaches
hyperfine \
  'python main.py input/ output1/ --engine html-to-text' \
  'python main.py input/ output2/ --engine pandoc'

# Monitor resource usage
/usr/bin/time -v python main.py input/ output/ --format md
```

### Quality Tips

```python
# Post-process for quality
def improve_quality(markdown_file):
    """Post-process Markdown for better quality."""

    with open(markdown_file, 'r') as f:
        content = f.read()

    # Fix common issues
    content = re.sub(r'\n{3,}', '\n\n', content)  # Fix multiple newlines
    content = re.sub(r' +', ' ', content)         # Fix multiple spaces
    content = re.sub(r'^\s+', '', content, flags=re.MULTILINE)  # Fix indentation

    with open(markdown_file, 'w') as f:
        f.write(content)
```

---

[← Back to Installation](INSTALLATION.md) | [Next: Troubleshooting →](TROUBLESHOOTING.md)