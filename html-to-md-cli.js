#!/usr/bin/env node

const htmlToMd = require('C:/Users/royca/AppData/Roaming/npm/node_modules/html-to-md');
const fs = require('fs');

// Read from stdin
let input = '';

if (process.stdin.isTTY) {
    console.error('Error: No input provided. Please pipe HTML content to this script.');
    process.exit(1);
}

process.stdin.setEncoding('utf8');

process.stdin.on('readable', () => {
    let chunk;
    while (null !== (chunk = process.stdin.read())) {
        input += chunk;
    }
});

process.stdin.on('end', () => {
    try {
        const markdown = htmlToMd(input);
        console.log(markdown);
    } catch (error) {
        console.error('Error converting HTML to Markdown:', error.message);
        process.exit(1);
    }
});