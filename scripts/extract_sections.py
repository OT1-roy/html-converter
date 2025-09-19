#!/usr/bin/env python3
"""
Extract specific line ranges from Podcast1+2+3+4+5.md based on Extraction.csv
Creates Extracted.md with all specified sections combined
"""

import csv
import os
import sys
from datetime import datetime
from pathlib import Path

def parse_csv_ranges(csv_path):
    """Parse the CSV file to get line ranges."""
    ranges = []

    try:
        with open(csv_path, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['FROM'] and row['TO']:  # Skip empty rows
                    from_line = int(row['FROM'])
                    to_line = int(row['TO'])
                    if from_line < to_line:  # Validate range
                        ranges.append((from_line, to_line))
                    else:
                        print(f"Warning: Invalid range {from_line}-{to_line}, skipping")
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        sys.exit(1)

    print(f"Parsed {len(ranges)} valid ranges from CSV")
    return ranges

def read_source_file(file_path):
    """Read all lines from the source markdown file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        print(f"Read {len(lines):,} lines from source file")
        return lines
    except Exception as e:
        print(f"Error reading source file: {e}")
        sys.exit(1)

def extract_sections(lines, ranges):
    """Extract specified line ranges from the source content."""
    extracted_sections = []
    total_lines_extracted = 0

    for idx, (from_line, to_line) in enumerate(ranges, 1):
        # Adjust for 0-based indexing
        start_idx = from_line - 1
        end_idx = to_line  # Inclusive, so we use to_line as-is

        # Validate bounds
        if start_idx < 0 or end_idx > len(lines):
            print(f"Warning: Range {from_line}-{to_line} exceeds file bounds, adjusting")
            start_idx = max(0, start_idx)
            end_idx = min(len(lines), end_idx)

        # Extract section
        section_lines = lines[start_idx:end_idx]
        section_text = ''.join(section_lines)

        # Create section with metadata
        section_data = {
            'number': idx,
            'from': from_line,
            'to': to_line,
            'lines_count': len(section_lines),
            'content': section_text
        }

        extracted_sections.append(section_data)
        total_lines_extracted += len(section_lines)

        print(f"  Section {idx:2d}: Lines {from_line:6d}-{to_line:6d} ({len(section_lines):4d} lines)")

    print(f"\nTotal lines extracted: {total_lines_extracted:,}")
    return extracted_sections

def write_output_file(output_path, sections):
    """Write all extracted sections to the output file."""
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            # Write header
            f.write("# Extracted Sections from Podcast Transcripts\n\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total sections: {len(sections)}\n")

            total_lines = sum(s['lines_count'] for s in sections)
            f.write(f"Total lines extracted: {total_lines:,}\n\n")
            f.write("---\n\n")

            # Write each section
            for section in sections:
                f.write(f"## Section {section['number']}\n")
                f.write(f"*Lines {section['from']}-{section['to']} ({section['lines_count']} lines)*\n\n")
                f.write(section['content'])
                if not section['content'].endswith('\n'):
                    f.write('\n')
                f.write("\n---\n\n")

        print(f"Output written to: {output_path}")

        # Calculate file size
        file_size = os.path.getsize(output_path)
        print(f"Output file size: {file_size:,} bytes ({file_size/1024/1024:.2f} MB)")

    except Exception as e:
        print(f"Error writing output file: {e}")
        sys.exit(1)

def generate_report(sections, output_dir):
    """Generate a summary report of the extraction."""
    report_path = output_dir / "extraction_report.txt"

    try:
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("EXTRACTION REPORT\n")
            f.write("=" * 50 + "\n\n")
            f.write(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

            f.write("SUMMARY\n")
            f.write("-" * 30 + "\n")
            f.write(f"Total sections extracted: {len(sections)}\n")
            f.write(f"Total lines extracted: {sum(s['lines_count'] for s in sections):,}\n\n")

            f.write("SECTION DETAILS\n")
            f.write("-" * 30 + "\n")
            for section in sections:
                f.write(f"Section {section['number']:2d}: Lines {section['from']:6d}-{section['to']:6d} "
                       f"({section['lines_count']:4d} lines)\n")

            # Check for overlapping ranges
            f.write("\nVALIDATION\n")
            f.write("-" * 30 + "\n")
            overlaps = []
            for i in range(len(sections) - 1):
                if sections[i]['to'] >= sections[i+1]['from']:
                    overlaps.append(f"Section {sections[i]['number']} and {sections[i+1]['number']}")

            if overlaps:
                f.write("Warning: Overlapping sections found:\n")
                for overlap in overlaps:
                    f.write(f"  - {overlap}\n")
            else:
                f.write("No overlapping sections detected.\n")

        print(f"Report generated: {report_path}")

    except Exception as e:
        print(f"Error generating report: {e}")

def main():
    """Main execution function."""
    print("=" * 60)
    print("PODCAST TRANSCRIPT EXTRACTION TOOL")
    print("=" * 60)

    # Define paths
    base_dir = Path("C:/Users/royca/Sidekick/html_converter")
    data_dir = base_dir / "data"

    csv_path = data_dir / "Extraction.csv"
    source_path = data_dir / "Podcast1+2+3+4+5.md"
    output_path = data_dir / "Extracted.md"

    # Verify input files exist
    if not csv_path.exists():
        print(f"Error: CSV file not found: {csv_path}")
        sys.exit(1)

    if not source_path.exists():
        print(f"Error: Source file not found: {source_path}")
        sys.exit(1)

    print(f"\nInput CSV: {csv_path}")
    print(f"Source file: {source_path}")
    print(f"Output file: {output_path}\n")

    # Process extraction
    print("Step 1: Parsing CSV ranges...")
    ranges = parse_csv_ranges(csv_path)

    print("\nStep 2: Reading source file...")
    lines = read_source_file(source_path)

    print("\nStep 3: Extracting sections...")
    sections = extract_sections(lines, ranges)

    print("\nStep 4: Writing output file...")
    write_output_file(output_path, sections)

    print("\nStep 5: Generating report...")
    generate_report(sections, data_dir)

    print("\n" + "=" * 60)
    print("EXTRACTION COMPLETE!")
    print("=" * 60)
    print(f"[DONE] Extracted {len(sections)} sections")
    print(f"[DONE] Output saved to: {output_path}")
    print(f"[DONE] Report saved to: {data_dir / 'extraction_report.txt'}")

if __name__ == "__main__":
    main()