import os
import re
import sys
import shutil
import subprocess
import argparse
import logging
from typing import Optional, Dict, List
from bs4 import BeautifulSoup, element
from tqdm import tqdm

# --- Configuration ---
MAX_FILE_SIZE_BYTES: int = 2 * 1024 * 1024  # 2 MB
MIN_CONTENT_SCORE: int = 50  # Minimum score to be considered 'good' content
ALLOWED_TAGS: List[str] = [
    'p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
    'ul', 'ol', 'li', 'blockquote', 'pre', 'code',
    'table', 'tr', 'td', 'th', 'strong', 'em', 'a'
]

def setup_logging(output_dir: str, input_folder_name: str) -> None:
    """Sets up a logger to write to a file in the output directory."""
    log_filename = f"run_{input_folder_name}.log"
    log_filepath = os.path.join(output_dir, log_filename)
    
    # Avoid adding handlers if they already exist (e.g., in interactive environments)
    logger = logging.getLogger()
    if not logger.handlers:
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            filename=log_filepath,
            filemode='w'
        )
        # Also add a handler to print errors to the console
        console_handler = logging.StreamHandler(sys.stderr)
        console_handler.setLevel(logging.ERROR)
        formatter = logging.Formatter('%(levelname)s: %(message)s')
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

def check_pandoc_dependency() -> None:
    """Checks if Pandoc is installed and exits if it's not."""
    if shutil.which("pandoc") is None:
        # Use logging if available, otherwise print
        try:
            logging.critical("FATAL ERROR: 'pandoc' command not found.")
            logging.critical("Please install Pandoc and ensure it is in your system's PATH.")
            logging.critical("Installation instructions: https://pandoc.org/installing.html")
        except NameError:
            print("FATAL ERROR: 'pandoc' command not found.", file=sys.stderr)
        sys.exit(1)
    logging.info("Pandoc dependency check successful.")

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
    
    if tag.name == 'article':
        score += 200
        
    return score

def clean_html_for_llm(soup_tag: element.Tag) -> str:
    """
    Surgically cleans HTML by removing unwanted tags while preserving their content
    and the overall document structure.
    """
    if not soup_tag:
        return ""
    
    clean_tag = BeautifulSoup(str(soup_tag), 'html5lib').find()
    
    for tag in clean_tag.find_all(True):
        if tag.name not in ALLOWED_TAGS:
            tag.unwrap()
            
    return str(clean_tag)

def convert_html_to_output(html_string: str, output_format: str) -> Optional[str]:
    """Uses pandoc to convert an HTML string to the desired output format."""
    if not html_string:
        return None
    
    if output_format == 'md':
        command = ['pandoc', '-f', 'html', '-t', 'markdown-smart']
    elif output_format == 'txt':
        command = ['pandoc', '-f', 'html', '-t', 'plain+smart', '--wrap=none', '--columns=9999']
    else:
        # This case should not be reached due to argparse choices
        logging.error(f"Invalid output format specified: {output_format}")
        return None

    try:
        process = subprocess.Popen(
            command,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        stdout, stderr = process.communicate(input=html_string.encode('utf-8'))
        
        if process.returncode != 0:
            logging.error(f"Pandoc Error: {stderr.decode('utf-8', 'ignore')}")
            return None
            
        return stdout.decode('utf-8')
    except Exception as e:
        logging.error(f"An unexpected error occurred with Pandoc: {e}")
        return None

def process_html_files(input_dir: str, output_dir: str, output_format: str) -> None:
    """Main function to orchestrate the conversion process."""
    if not os.path.isdir(input_dir):
        print(f"Error: Input directory '{input_dir}' not found.", file=sys.stderr)
        sys.exit(1)

    os.makedirs(output_dir, exist_ok=True)
    
    input_folder_name = os.path.basename(os.path.normpath(input_dir))
    setup_logging(output_dir, input_folder_name)
    
    all_files: List[str] = sorted([f for f in os.listdir(input_dir) if f.endswith(('.html', '.htm'))])
    if not all_files:
        logging.warning(f"No HTML files found in '{input_dir}'.")
        return

    job_stats: Dict[str, int] = {"successful": 0, "failed": 0, "output_files": 1}
    logging.info(f"Starting job. Found {len(all_files)} HTML files in '{input_dir}'. Output format: {output_format.upper()}")
    
    output_filename_template = f"{input_folder_name}_output_{{}}.{output_format}"
    output_filepath = os.path.join(output_dir, output_filename_template.format(job_stats["output_files"]))
    
    try:
        with open(output_filepath, 'w', encoding='utf-8') as out_file:
            logging.info(f"Creating new output file: {output_filepath}")
            pbar = tqdm(all_files, desc="Processing files", unit="file")
            
            for filename in pbar:
                pbar.set_postfix_str(filename)
                try:
                    filepath = os.path.join(input_dir, filename)
                    logging.info(f"Processing '{filename}'.")
                    with open(filepath, 'r', encoding='utf-8-sig', errors='ignore') as f:
                        soup = BeautifulSoup(f, 'html5lib')

                    page_title_tag = soup.find('title')
                    page_title = page_title_tag.get_text(strip=True) if page_title_tag else "No Title Found"

                    for tag in soup(['script', 'style', 'nav', 'footer', 'header', 'aside', 'form']):
                        tag.decompose()
                    
                    candidates = {el: get_content_score(el) for el in soup.find_all(['div', 'article', 'main', 'section'])}
                    
                    html_to_process = None
                    if candidates:
                        best_candidate_element = max(candidates, key=candidates.get)
                        best_score = candidates[best_candidate_element]
                        if best_score < MIN_CONTENT_SCORE:
                            logging.warning(f"Best score for {filename} is low ({best_score}). Falling back to <body>.")
                            html_to_process = soup.find('body')
                        else:
                            logging.info(f"Found best candidate in '{filename}' with score {best_score}.")
                            html_to_process = best_candidate_element
                    else:
                        logging.warning(f"No candidates found in {filename}. Falling back to <body>.")
                        html_to_process = soup.find('body')

                    if html_to_process:
                        clean_html = clean_html_for_llm(html_to_process)
                        output_text = convert_html_to_output(clean_html, output_format)
                        
                        if output_text and output_text.strip():
                            content_to_write = ""
                            # Only add YAML frontmatter for Markdown files
                            if output_format == 'md':
                                safe_title = page_title.replace('\\', '\\\\').replace('"', '\\"')
                                frontmatter = f"---\nsource: {filename}\ntitle: \"{safe_title}\"\n---\n\n"
                                content_to_write += frontmatter
                            
                            content_to_write += f"{output_text.strip()}\n\n"
                            
                            current_size = out_file.tell()
                            if current_size + len(content_to_write.encode('utf-8')) > MAX_FILE_SIZE_BYTES and current_size > 0:
                                out_file.close()
                                job_stats["output_files"] += 1
                                output_filepath = os.path.join(output_dir, output_filename_template.format(job_stats["output_files"]))
                                logging.info(f"Max file size reached. Creating new output file: {output_filepath}")
                                out_file = open(output_filepath, 'w', encoding='utf-8')

                            out_file.write(content_to_write)
                            job_stats["successful"] += 1
                        else:
                            logging.error(f"Pandoc conversion resulted in empty output for {filename}.")
                            job_stats["failed"] += 1
                    else:
                        logging.error(f"Failed to find any content to convert in {filename}.")
                        job_stats["failed"] += 1

                except Exception as e:
                    logging.critical(f"CRITICAL ERROR processing {filename}: {e}", exc_info=True)
                    job_stats["failed"] += 1

    except KeyboardInterrupt:
        logging.warning("Process interrupted by user. Shutting down gracefully.")
    finally:
        summary = (
            f"\n{'='*25} JOB SUMMARY {'='*25}\n"
            f"  - Total HTML files scanned:   {len(all_files)}\n"
            f"  - Successful extractions:     {job_stats['successful']}\n"
            f"  - Failed extractions:         {job_stats['failed']}\n"
            f"  - Total output files created: {job_stats['output_files']} (.{output_format})\n"
            f"  - Detailed log saved to: '{os.path.join(output_dir, f'run_{input_folder_name}.log')}'\n"
            f"{'='*65}"
        )
        print(summary)
        logging.info("Job finished.")
        logging.info(summary)
        if job_stats["failed"] > 0:
            sys.exit(1)

def main():
    parser = argparse.ArgumentParser(
        description="A robust utility to extract and convert HTML content to Markdown or plain text.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("input_dir", help="The directory containing source HTML files.")
    parser.add_argument("output_dir", help="The directory where output files will be saved.")
    parser.add_argument(
        "--format", 
        choices=['md', 'txt'], 
        default='md', 
        help="The output file format:\n"
             "  md  - Markdown (default)\n"
             "  txt - Plain text"
    )
    
    args = parser.parse_args()
    
    # We set up logging inside process_html_files once we know the output dir.
    # But we check for Pandoc first.
    check_pandoc_dependency() 
    
    process_html_files(args.input_dir, args.output_dir, args.format)

if __name__ == "__main__":
    main()
