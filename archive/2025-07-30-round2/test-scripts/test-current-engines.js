const fs = require('fs');

// Same test HTML as turndown test
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

// Save test HTML to file
fs.writeFileSync('test-html-sample.html', testHtml);
console.log('Test HTML saved to test-html-sample.html');