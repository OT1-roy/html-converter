import os
import re
import sys
import shutil
import subprocess
import argparse
from typing import Optional, Dict, List
from bs4 import BeautifulSoup, element
from tqdm import tqdm

# --- Configuration ---
MAX_FILE_SIZE_BYTES: int = 2 * 1024 * 1024  # 2 MB
MIN_CONTENT_SCORE: int = 50  # Minimum score to be considered 'good' content

def check_pandoc_dependency() -> None:
    """Checks if Pandoc is installed and exits if it's not."""
    if shutil.which("pandoc") is None:
        print("FATAL ERROR: 'pandoc' command not found.", file=sys.stderr)
        print("Please install Pandoc and ensure it is in your system's PATH.", file=sys.stderr)
        print("Installation instructions: https://pandoc.org/installing.html", file=sys.stderr)
        sys.exit(1)
    print("Pandoc dependency check successful.")

def get_content_score(tag: element.Tag) -> int:
    """Calculates a 'content score' for a given HTML element."""
    if not tag:
        return 0
    
    score = 0
    text = tag.get_text(separator=' ', strip=True)
    score += len(text)
    score += len(tag.find_all('p')) * 25

    links = tag.find_all('a')
    link_text_length = sum(len(link.get_text(strip=True)) for link in links)
    
    if len(text) > 0 and (link_text_length / len(text)) > 0.4:
        score -= 100

    class_id_string = ' '.join(tag.get('class', [])) + ' ' + (tag.get('id', '') or '')
    
    if re.search('comment|sidebar|footer|menu|nav|ad|promo|share|social', class_id_string, re.I):
        score -= 50
    if re.search('article|content|post|body|main|story|entry', class_id_string, re.I):
        score += 50
    
    # REFINED: Give a massive bonus to <article> tags as they are strong indicators.
    if tag.name == 'article':
        score += 200
        
    return score

def convert_html_to_markdown_pandoc(html_string: str) -> Optional[str]:
    """Uses pandoc to convert an HTML string to Markdown."""
    try:
        process = subprocess.Popen(
            ['pandoc', '-f', 'html', '-t', 'markdown-smart'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        stdout, stderr = process.communicate(input=html_string.encode('utf-8'))
        
        if process.returncode != 0:
            sys.stderr.write(f"  -> Pandoc Error: {stderr.decode('utf-8', 'ignore')}\n")
            return None
            
        return stdout.decode('utf-8')
    except Exception as e:
        sys.stderr.write(f"An unexpected error occurred with Pandoc: {e}\n")
        return None

def process_html_files(input_dir: str, output_dir: str) -> None:
    """Main function to orchestrate the conversion process."""
    if not os.path.isdir(input_dir):
        print(f"Error: Input directory '{input_dir}' not found.", file=sys.stderr)
        sys.exit(1)

    os.makedirs(output_dir, exist_ok=True)
    
    all_files: List[str] = sorted([f for f in os.listdir(input_dir) if f.endswith(('.html', '.htm'))])
    if not all_files:
        print(f"No HTML files found in '{input_dir}'.")
        return

    job_stats: Dict[str, int] = {"successful": 0, "failed": 0, "output_files": 1}
    
    output_filepath = os.path.join(output_dir, f'output_{job_stats["output_files"]}.md')
    
    try:
        with open(output_filepath, 'w', encoding='utf-8') as md_file:
            print(f"Creating new output file: {output_filepath}")
            pbar = tqdm(all_files, desc="Processing files", unit="file")
            for filename in pbar:
                try:
                    with open(os.path.join(input_dir, filename), 'r', encoding='utf-8-sig', errors='ignore') as f:
                        soup = BeautifulSoup(f, 'html5lib')

                    page_title_tag = soup.find('title')
                    page_title = page_title_tag.get_text(strip=True) if page_title_tag else "No Title Found"

                    # NEW: Aggressively remove known non-content blocks before scoring
                    for tag in soup.find_all(['script', 'style', 'nav', 'footer', 'header', 'aside', 'form']):
                        tag.decompose()
                    # Specifically remove the podcast player iframe and button containers
                    for iframe in soup.find_all('iframe', src=lambda x: x and 'libsyn.com' in x):
                        iframe.decompose()
                    for button_container in soup.find_all('div', class_='sqs-block-button-container'):
                        button_container.decompose()

                    candidates = {el: get_content_score(el) for el in soup.find_all(['div', 'article', 'main', 'section'])}
                    
                    html_to_convert = None
                    if candidates:
                        best_candidate_element = max(candidates, key=candidates.get)
                        best_score = candidates[best_candidate_element]

                        if best_score < MIN_CONTENT_SCORE:
                            pbar.write(f"  -> Warning: Best score for {filename} is low. Falling back to <body>.")
                            html_to_convert = soup.find('body')
                        else:
                            html_to_convert = best_candidate_element
                    else:
                        pbar.write(f"  -> Warning: No candidates found in {filename}. Falling back to <body>.")
                        html_to_convert = soup.find('body')

                    if html_to_convert:
                        markdown_text = convert_html_to_markdown_pandoc(str(html_to_convert))
                        if markdown_text:
                            safe_title = page_title.replace('\\', '\\\\').replace('"', '\\"')
                            frontmatter = f"---\nsource: {filename}\ntitle: \"{safe_title}\"\n---\n\n"
                            content_to_write = f"{frontmatter}{markdown_text.strip()}\n\n"
                            
                            current_size = md_file.tell()
                            if current_size + len(content_to_write.encode('utf-8')) > MAX_FILE_SIZE_BYTES and current_size > 0:
                                md_file.close()
                                job_stats["output_files"] += 1
                                output_filepath = os.path.join(output_dir, f'output_{job_stats["output_files"]}.md')
                                pbar.write(f"\nMax file size reached. Creating new output file: {output_filepath}")
                                md_file = open(output_filepath, 'w', encoding='utf-8')

                            md_file.write(content_to_write)
                            job_stats["successful"] += 1
                        else:
                            job_stats["failed"] += 1
                    else:
                        pbar.write(f"  -> Failed to find any content to convert in {filename}.")
                        job_stats["failed"] += 1

                except Exception as e:
                    pbar.write(f"  -> CRITICAL ERROR processing {filename}: {e}", file=sys.stderr)
                    job_stats["failed"] += 1

    except KeyboardInterrupt:
        print("\n\nProcess interrupted by user. Shutting down gracefully.", file=sys.stderr)
    finally:
        print("\n" + "="*25 + " JOB SUMMARY " + "="*25)
        print(f"  - Total HTML files scanned:   {len(all_files)}")
        print(f"  - Successful extractions:     {job_stats['successful']}")
        print(f"  - Failed extractions:         {job_stats['failed']}")
        print(f"  - Total Markdown files created: {job_stats['output_files']}")
        print(f"Output saved in directory: '{output_dir}'")
        print("="*65)
        if job_stats["failed"] > 0:
            sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="A robust utility to extract and convert HTML content to Markdown.")
    parser.add_argument("input_dir", help="The directory containing source HTML files.")
    parser.add_argument("output_dir", help="The directory where output Markdown files will be saved.")
    
    check_pandoc_dependency()
    args = parser.parse_args()
    process_html_files(args.input_dir, args.output_dir)

if __name__ == "__main__":
    main()
