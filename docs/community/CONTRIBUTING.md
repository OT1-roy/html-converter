# Contributing to HTML Converter

![Contributors](https://img.shields.io/badge/contributors-welcome-brightgreen)
![PRs Welcome](https://img.shields.io/badge/PRs-welcome-blue)
![Code of Conduct](https://img.shields.io/badge/code%20of%20conduct-enforced-orange)

Thank you for your interest in contributing to HTML Converter! We welcome contributions from everyone, whether you're fixing a typo, adding a feature, or proposing major changes.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [How to Contribute](#how-to-contribute)
- [Development Setup](#development-setup)
- [Development Workflow](#development-workflow)
- [Code Standards](#code-standards)
- [Testing Guidelines](#testing-guidelines)
- [Pull Request Process](#pull-request-process)
- [Commit Guidelines](#commit-guidelines)
- [Documentation](#documentation)
- [Community](#community)
- [Recognition](#recognition)

## Code of Conduct

### Our Pledge

We are committed to providing a welcoming and inclusive experience for everyone. We expect all participants to:

- **Be Respectful**: Value each other's ideas, styles, and viewpoints
- **Be Direct but Professional**: Be honest and straightforward while being respectful
- **Be Inclusive**: Seek diverse perspectives and welcome newcomers
- **Understand Disagreements**: Disagreements happen, but frustration should not turn into attacks
- **Be Open**: Be open to feedback and changing your mind

### Enforcement

Violations of the code of conduct may result in:
1. Warning
2. Temporary ban
3. Permanent ban

Report issues to: conduct@example.com

## Getting Started

### First Time Contributors

We love first-time contributors! Look for issues labeled:

- `good first issue` - Simple fixes perfect for beginners
- `help wanted` - We need your help!
- `documentation` - Help improve our docs
- `bug` - Help us squash bugs

### Understanding the Project

1. **Read the Documentation**
   - [README.md](../../../README.md) - Project overview
   - [ARCHITECTURE.md](../technical/ARCHITECTURE.md) - System design
   - [API.md](../api/API.md) - API reference

2. **Explore the Codebase**
   ```bash
   # Main application logic
   main.py

   # Node.js wrapper
   html-to-md-cli.js

   # Documentation
   docs/
   ```

3. **Run the Application**
   ```bash
   python main.py ./sample_html ./output --format md
   ```

## How to Contribute

### Ways to Contribute

#### 🐛 Report Bugs

Create an issue with:
- Clear, descriptive title
- Steps to reproduce
- Expected vs actual behavior
- System information
- Error messages/logs

**Bug Report Template:**
```markdown
## Bug Description
Brief description of the bug

## Steps to Reproduce
1. Run command: `...`
2. See error

## Expected Behavior
What should happen

## Actual Behavior
What actually happens

## System Information
- OS: Windows 10 / macOS 12 / Ubuntu 20.04
- Python: 3.9.7
- Node.js: 16.13.0
- Engine: pandoc / html-to-text

## Logs
```
Paste relevant logs here
```
```

#### ✨ Suggest Features

Create an issue with:
- Use case description
- Proposed solution
- Alternative solutions
- Mockups/examples (if applicable)

**Feature Request Template:**
```markdown
## Feature Description
What feature would you like to see?

## Use Case
Why is this feature needed?

## Proposed Solution
How should it work?

## Alternatives Considered
What other solutions did you consider?

## Additional Context
Any mockups, examples, or references?
```

#### 📝 Improve Documentation

- Fix typos and grammar
- Add examples
- Clarify confusing sections
- Translate documentation
- Add diagrams

#### 💻 Submit Code

- Fix bugs
- Add features
- Improve performance
- Refactor code
- Add tests

## Development Setup

### Prerequisites

```bash
# Install Python 3.7+
python --version

# Install Node.js 14+ (for html-to-text)
node --version

# Install Git
git --version
```

### Fork and Clone

1. **Fork the Repository**
   - Click "Fork" on GitHub
   - Creates your copy: `https://github.com/YOUR_USERNAME/html-converter`

2. **Clone Your Fork**
   ```bash
   git clone https://github.com/YOUR_USERNAME/html-converter.git
   cd html-converter
   ```

3. **Add Upstream Remote**
   ```bash
   git remote add upstream https://github.com/OT1-roy/html-converter.git
   git remote -v
   ```

### Environment Setup

```bash
# Create virtual environment
python -m venv venv

# Activate it
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt  # Development dependencies

# Install Node.js dependencies
npm install -g @html-to/text-cli
npm install -g html-to-md

# Install pre-commit hooks
pre-commit install
```

### Development Dependencies

Create `requirements-dev.txt`:
```txt
# Testing
pytest>=7.0.0
pytest-cov>=3.0.0
pytest-mock>=3.6.0

# Code Quality
black>=22.0.0
flake8>=4.0.0
pylint>=2.12.0
mypy>=0.930

# Documentation
sphinx>=4.0.0
sphinx-rtd-theme>=1.0.0

# Development Tools
ipython>=8.0.0
pre-commit>=2.17.0
```

## Development Workflow

### 1. Create a Branch

```bash
# Sync with upstream
git fetch upstream
git checkout main
git merge upstream/main

# Create feature branch
git checkout -b feature/amazing-feature
# Or: bugfix/issue-123
# Or: docs/improve-readme
```

### Branch Naming

- `feature/` - New features
- `bugfix/` - Bug fixes
- `docs/` - Documentation
- `refactor/` - Code refactoring
- `test/` - Test improvements
- `perf/` - Performance improvements

### 2. Make Changes

```bash
# Make your changes
vim main.py

# Run tests frequently
pytest

# Check code style
black --check main.py
flake8 main.py
```

### 3. Test Your Changes

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=main --cov-report=html

# Test specific function
pytest tests/test_main.py::test_get_content_score

# Test with different Python versions
tox
```

### 4. Commit Changes

```bash
# Stage changes
git add .

# Commit with meaningful message
git commit -m "feat: add support for custom content scoring

- Implement custom_content_scorer function
- Add configuration for score weights
- Update documentation

Fixes #123"
```

### 5. Push Changes

```bash
# Push to your fork
git push origin feature/amazing-feature
```

### 6. Create Pull Request

1. Go to your fork on GitHub
2. Click "Pull Request"
3. Fill out the PR template
4. Submit for review

## Code Standards

### Python Style Guide

We follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) with these specifications:

```python
# Imports
import os
import sys
from typing import Optional, List

import third_party_lib

from main import local_module

# Constants
MAX_FILE_SIZE_BYTES = 2 * 1024 * 1024  # Comment explaining value
ALLOWED_TAGS = ["p", "h1", "h2"]  # Use double quotes for strings

# Functions
def process_file(
    input_path: str,
    output_path: str,
    format: str = "md"
) -> Optional[str]:
    """
    Process a single HTML file.

    Args:
        input_path: Path to input HTML file
        output_path: Path for output file
        format: Output format ('md' or 'txt')

    Returns:
        Converted content or None if failed

    Raises:
        FileNotFoundError: If input file doesn't exist
    """
    # Implementation
    pass

# Classes
class HTMLProcessor:
    """Process HTML documents."""

    def __init__(self, engine: str = "html-to-text") -> None:
        """Initialize processor with specified engine."""
        self.engine = engine

    def process(self, html: str) -> str:
        """Process HTML content."""
        # Use descriptive variable names
        cleaned_html = self._clean_html(html)
        converted_content = self._convert(cleaned_html)
        return converted_content
```

### Code Quality Tools

#### Black (Formatting)
```bash
# Format code
black main.py

# Check without changing
black --check main.py

# Configuration in pyproject.toml
[tool.black]
line-length = 88
target-version = ['py37', 'py38', 'py39']
```

#### Flake8 (Linting)
```bash
# Check code
flake8 main.py

# Configuration in .flake8
[flake8]
max-line-length = 88
exclude = venv,__pycache__
ignore = E203,W503
```

#### MyPy (Type Checking)
```bash
# Check types
mypy main.py

# Configuration in mypy.ini
[mypy]
python_version = 3.7
warn_return_any = True
warn_unused_configs = True
```

### JavaScript Style Guide

For `html-to-md-cli.js`:

```javascript
#!/usr/bin/env node
'use strict';

// Use const/let, not var
const fs = require('fs');
const path = require('path');

// Use arrow functions for callbacks
process.stdin.on('data', (chunk) => {
    processChunk(chunk);
});

// Use async/await over promises
async function convertHTML(html) {
    try {
        const result = await htmlToMd(html);
        return result;
    } catch (error) {
        console.error('Conversion error:', error.message);
        process.exit(1);
    }
}

// Export for testing
module.exports = { convertHTML };
```

## Testing Guidelines

### Test Structure

```python
# tests/test_main.py
import pytest
from unittest.mock import Mock, patch

from main import get_content_score, clean_html_for_llm

class TestContentScoring:
    """Test content scoring functionality."""

    def test_scores_article_tag_highly(self):
        """Article tags should receive bonus points."""
        mock_tag = Mock()
        mock_tag.name = 'article'
        mock_tag.get_text.return_value = 'Content'
        mock_tag.find_all.return_value = []
        mock_tag.get.return_value = []

        score = get_content_score(mock_tag)
        assert score >= 200

    @pytest.mark.parametrize("text,expected_min", [
        ("Short", 5),
        ("This is a longer text", 20),
        ("This is a much longer text with many words", 40),
    ])
    def test_scores_by_text_length(self, text, expected_min):
        """Longer text should score higher."""
        mock_tag = Mock()
        mock_tag.get_text.return_value = text
        mock_tag.find_all.return_value = []
        mock_tag.get.return_value = []

        score = get_content_score(mock_tag)
        assert score >= expected_min
```

### Test Coverage

```bash
# Run with coverage
pytest --cov=main --cov-report=term-missing

# Generate HTML report
pytest --cov=main --cov-report=html

# Coverage requirements
# - Minimum: 70% overall
# - Goal: 90% for critical functions
```

### Integration Tests

```python
# tests/test_integration.py
import tempfile
import os
from pathlib import Path

def test_full_conversion_pipeline():
    """Test complete HTML to Markdown conversion."""
    # Setup
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create test HTML
        input_dir = Path(tmpdir) / "input"
        input_dir.mkdir()
        html_file = input_dir / "test.html"
        html_file.write_text("<h1>Test</h1><p>Content</p>")

        output_dir = Path(tmpdir) / "output"
        output_dir.mkdir()

        # Run conversion
        from main import process_html_files
        process_html_files(
            str(input_dir),
            str(output_dir),
            'md',
            'html-to-text'
        )

        # Verify output
        output_files = list(output_dir.glob("*.md"))
        assert len(output_files) == 1

        content = output_files[0].read_text()
        assert "# Test" in content
        assert "Content" in content
```

## Pull Request Process

### PR Requirements

1. **Code Quality**
   - Passes all tests
   - Follows style guidelines
   - No linting errors
   - Type hints included

2. **Testing**
   - New features have tests
   - Bug fixes include regression tests
   - All tests pass

3. **Documentation**
   - Docstrings for new functions
   - README updated if needed
   - CHANGELOG entry added

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix (non-breaking change)
- [ ] New feature (non-breaking change)
- [ ] Breaking change (fix or feature that breaks existing functionality)
- [ ] Documentation update

## Testing
- [ ] All tests pass locally
- [ ] New tests added for changes
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No new warnings generated
- [ ] Added tests that prove fix/feature works
- [ ] All tests pass

## Related Issues
Fixes #(issue number)

## Screenshots (if applicable)
Add screenshots for UI changes
```

### Review Process

1. **Automated Checks**
   - CI/CD runs tests
   - Code coverage checked
   - Linting validation

2. **Code Review**
   - At least 1 approval required
   - Address all feedback
   - Resolve all conversations

3. **Merge**
   - Squash and merge for features
   - Merge commit for releases
   - Rebase for small fixes

## Commit Guidelines

We follow [Conventional Commits](https://www.conventionalcommits.org/):

### Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `perf`: Performance improvements
- `test`: Test additions/changes
- `build`: Build system changes
- `ci`: CI/CD changes
- `chore`: Maintenance tasks

### Examples

```bash
# Feature
git commit -m "feat(engine): add support for custom HTML parsers

- Implement parser interface
- Add BeautifulSoup parser
- Add lxml parser option

Closes #45"

# Bug fix
git commit -m "fix(converter): handle empty HTML files gracefully

Previously crashed with empty input, now returns None

Fixes #67"

# Documentation
git commit -m "docs(api): add examples for all public functions"

# Performance
git commit -m "perf(scoring): optimize content scoring algorithm

Reduces scoring time by 40% for large documents"
```

## Documentation

### Documentation Standards

1. **Docstrings** (Google Style)
   ```python
   def function_name(param1: str, param2: int = 0) -> bool:
       """Brief description of function.

       Longer description if needed, explaining behavior,
       edge cases, and important details.

       Args:
           param1: Description of param1
           param2: Description of param2 (default: 0)

       Returns:
           Description of return value

       Raises:
           ValueError: When param1 is empty
           TypeError: When param2 is not integer

       Example:
           >>> function_name("test", 42)
           True
       """
   ```

2. **Inline Comments**
   ```python
   # Explain why, not what
   score += 200  # Article tags are primary content containers
   ```

3. **README Updates**
   - Keep examples current
   - Update feature list
   - Maintain compatibility notes

### Building Documentation

```bash
# Install Sphinx
pip install sphinx sphinx-rtd-theme

# Generate docs
cd docs
sphinx-build -b html . _build

# View documentation
open _build/index.html
```

## Community

### Communication Channels

- **GitHub Issues**: Bug reports and features
- **GitHub Discussions**: Questions and ideas
- **Discord**: Real-time chat (coming soon)
- **Twitter**: @htmlconverter (coming soon)

### Getting Help

1. **Search existing issues**
2. **Check documentation**
3. **Ask in Discussions**
4. **Create an issue**

### Helping Others

- Answer questions in Discussions
- Review pull requests
- Test pre-releases
- Share your use cases

## Recognition

### Contributors

We recognize all contributors:

- **Code Contributors**: Listed in [AUTHORS.md](AUTHORS.md)
- **Issue Reporters**: Thanked in release notes
- **Documentation Writers**: Credited in docs
- **Testers**: Mentioned in CHANGELOG
- **Idea Contributors**: Acknowledged in features

### Contributor Levels

🥉 **Bronze** (1-2 contributions)
🥈 **Silver** (3-9 contributions)
🥇 **Gold** (10-24 contributions)
💎 **Diamond** (25+ contributions)
🌟 **Core Team** (Maintainers)

### All Contributors

We use [All Contributors](https://allcontributors.org/) to recognize everyone:

<!-- ALL-CONTRIBUTORS-LIST:START -->
<!-- ALL-CONTRIBUTORS-LIST:END -->

## Release Process

### Version Numbering

We use [Semantic Versioning](https://semver.org/):
- MAJOR.MINOR.PATCH (e.g., 2.1.3)
- MAJOR: Breaking changes
- MINOR: New features (backward compatible)
- PATCH: Bug fixes

### Release Checklist

```markdown
- [ ] All tests pass
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
- [ ] Version bumped in main.py
- [ ] Git tag created
- [ ] GitHub Release created
- [ ] PyPI package uploaded (future)
```

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to HTML Converter! 🎉

[← Back to Architecture](../technical/ARCHITECTURE.md) | [Home](../../../README.md)