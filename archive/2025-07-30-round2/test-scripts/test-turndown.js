const TurndownService = require('turndown');
const fs = require('fs');

// Create test HTML
const testHtml = `
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
`;

// Test with default options
console.log('=== TURNDOWN - DEFAULT OPTIONS ===');
const turndownService = new TurndownService();
const defaultOutput = turndownService.turndown(testHtml);
console.log(defaultOutput);

// Test with ATX headings (like GitHub)
console.log('\n=== TURNDOWN - ATX HEADINGS ===');
const turndownAtx = new TurndownService({
    headingStyle: 'atx',
    codeBlockStyle: 'fenced',
    fence: '```'
});
const atxOutput = turndownAtx.turndown(testHtml);
console.log(atxOutput);

// Test with GitHub Flavored Markdown style
console.log('\n=== TURNDOWN - GFM STYLE ===');
const turndownGfm = new TurndownService({
    headingStyle: 'atx',
    hr: '---',
    bulletListMarker: '-',
    codeBlockStyle: 'fenced',
    fence: '```',
    emDelimiter: '*',
    strongDelimiter: '**',
    linkStyle: 'inlined'
});
const gfmOutput = turndownGfm.turndown(testHtml);
console.log(gfmOutput);

// Save outputs to files for comparison
fs.writeFileSync('turndown-default.md', defaultOutput);
fs.writeFileSync('turndown-atx.md', atxOutput);
fs.writeFileSync('turndown-gfm.md', gfmOutput);

console.log('\n=== FILES SAVED ===');
console.log('- turndown-default.md');
console.log('- turndown-atx.md');
console.log('- turndown-gfm.md');