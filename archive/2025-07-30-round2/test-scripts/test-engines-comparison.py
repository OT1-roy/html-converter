#!/usr/bin/env python3

import subprocess
import sys
import os

# Test HTML content
test_html = """
<!DOCTYPE html>
<html>
<head>
    <title>Test Document</title>
</head>
<body>
    <div class="header">
        <h1>Main Title</h1>
        <p>This is a test paragraph with <strong>bold text</strong> and <em>italic text</em>.</p>
    </div>
    
    <article class="content">
        <h2>Article Section</h2>
        <p>Here's some content with a <a href="https://example.com">link</a>.</p>
        
        <ul>
            <li>First item</li>
            <li>Second item with <code>inline code</code></li>
            <li>Third item</li>
        </ul>
        
        <blockquote>
            <p>This is a blockquote with multiple lines.
            It should be properly formatted in Markdown.</p>
        </blockquote>
        
        <pre><code>function example() {
    return "code block";
}</code></pre>
        
        <table>
            <thead>
                <tr>
                    <th>Column 1</th>
                    <th>Column 2</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>Cell 1</td>
                    <td>Cell 2</td>
                </tr>
            </tbody>
        </table>
    </article>
    
    <footer>
        <p>Footer content</p>
    </footer>
</body>
</html>
"""

def test_pandoc_md(html_content):
    """Test Pandoc Markdown conversion"""
    try:
        command = ['pandoc', '-f', 'html', '-t', 'markdown-smart']
        process = subprocess.Popen(
            command,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        stdout, stderr = process.communicate(input=html_content.encode('utf-8'))
        
        if process.returncode == 0:
            return stdout.decode('utf-8')
        else:
            return f"Error: {stderr.decode('utf-8')}"
    except Exception as e:
        return f"Exception: {e}"

def test_html_to_md(html_content):
    """Test html-to-md conversion"""
    try:
        md_script_path = os.path.join(os.path.dirname(__file__), "html-to-md-cli.js").replace("/", "\\\\")
        command = f'node "{md_script_path}"'
        
        if sys.platform == 'win32':
            process = subprocess.Popen(
                f'cmd /c "{command}"',
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=False
            )
        else:
            process = subprocess.Popen(
                command,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=True
            )
        
        stdout, stderr = process.communicate(input=html_content.encode('utf-8'))
        
        if process.returncode == 0:
            return stdout.decode('utf-8')
        else:
            return f"Error: {stderr.decode('utf-8')}"
    except Exception as e:
        return f"Exception: {e}"

def test_turndown(html_content):
    """Test Turndown conversion"""
    try:
        # Create a simple test script for turndown
        turndown_script = '''
const TurndownService = require('turndown');
const fs = require('fs');

const input = fs.readFileSync(0, 'utf-8'); // Read from stdin
const turndownService = new TurndownService({
    headingStyle: 'atx',
    codeBlockStyle: 'fenced',
    fence: '```'
});

console.log(turndownService.turndown(input));
'''
        
        with open('temp-turndown-test.js', 'w') as f:
            f.write(turndown_script)
        
        command = 'node temp-turndown-test.js'
        
        if sys.platform == 'win32':
            process = subprocess.Popen(
                f'cmd /c "{command}"',
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=False
            )
        else:
            process = subprocess.Popen(
                command,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=True
            )
        
        stdout, stderr = process.communicate(input=html_content.encode('utf-8'))
        
        # Clean up temp file
        if os.path.exists('temp-turndown-test.js'):
            os.remove('temp-turndown-test.js')
        
        if process.returncode == 0:
            return stdout.decode('utf-8')
        else:
            return f"Error: {stderr.decode('utf-8')}"
    except Exception as e:
        return f"Exception: {e}"

if __name__ == "__main__":
    print("=== ENGINE COMPARISON TEST ===\n")
    
    print("1. PANDOC MARKDOWN OUTPUT:")
    print("-" * 40)
    pandoc_result = test_pandoc_md(test_html)
    print(pandoc_result)
    
    print("\n2. HTML-TO-MD OUTPUT:")
    print("-" * 40)
    html_to_md_result = test_html_to_md(test_html)
    print(html_to_md_result)
    
    print("\n3. TURNDOWN OUTPUT:")
    print("-" * 40)
    turndown_result = test_turndown(test_html)
    print(turndown_result)
    
    # Save results to files
    with open('comparison-pandoc.md', 'w', encoding='utf-8') as f:
        f.write(pandoc_result)
    
    with open('comparison-html-to-md.md', 'w', encoding='utf-8') as f:
        f.write(html_to_md_result)
    
    with open('comparison-turndown.md', 'w', encoding='utf-8') as f:
        f.write(turndown_result)
    
    print("\n=== COMPARISON FILES SAVED ===")
    print("- comparison-pandoc.md")
    print("- comparison-html-to-md.md") 
    print("- comparison-turndown.md")