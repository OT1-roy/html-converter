# Repository Management Guide

## 🎯 Purpose
This document provides **crystal clear instructions** for managing dual repositories and preventing file confusion.

## 📁 Repository Definitions

### 🌍 PUBLIC Repository (html-converter)
**URL**: https://github.com/OT1-roy/html-converter  
**Purpose**: Clean, professional open-source release  
**Audience**: General public, potential users, contributors

#### ✅ PUBLIC Files (INCLUDE):
```
main.py                 # Main application
requirements.txt        # Dependencies only
README.md              # Public documentation
License               # MIT license
.gitignore            # Public gitignore (restrictive)
```

#### ❌ PUBLIC Exclusions (NEVER INCLUDE):
```
.claude/              # Development tools
README-PRIVATE.md     # Internal documentation  
.gitignore.private    # Private gitignore
.gitignore.public     # Gitignore variants
archive/              # Development artifacts
old/                  # Version history
*-PRIVATE.*           # Any private-suffixed files
REPO-MANAGEMENT.md    # This management file
```

### 🔒 PRIVATE Repository (html-converter-private)  
**URL**: https://github.com/OT1-roy/html-converter-private  
**Purpose**: Complete development environment  
**Audience**: Development team only

#### ✅ PRIVATE Files (INCLUDE EVERYTHING):
```
main.py               # Main application
requirements.txt      # Dependencies
README.md            # Public documentation (copy)
README-PRIVATE.md    # Private development docs
License             # MIT license
.claude/            # Claude Code settings
.gitignore          # Active gitignore (less restrictive)
.gitignore.private  # Private gitignore template
.gitignore.public   # Public gitignore template
archive/            # Housekeeping archives
old/                # Version history
REPO-MANAGEMENT.md  # This file
```

## 🚨 Current Issues to Fix

### Issues Found:
1. **Public repo contaminated** with private files (.claude/, README-PRIVATE.md, etc.)
2. **Private repo incomplete** - missing archive/, local development files
3. **No clear workflow** for future changes

## 📋 Action Plan

### Step 1: Clean Public Repository
```bash
# Remove private files from public repo
git rm .claude/settings.local.json
git rm README-PRIVATE.md  
git rm .gitignore.private
git rm .gitignore.public
git commit -m "Clean public repo: Remove private development files"
git push origin main
```

### Step 2: Complete Private Repository
```bash
# Switch to private gitignore
cp .gitignore.private .gitignore

# Add all missing files  
git add .
git commit -m "Complete private repo: Add all development files"
git push private main
```

### Step 3: Implement Workflow

## 🔄 Daily Workflow

### Making Changes:
1. **Work in local directory** (has everything)
2. **Test changes** with full development environment
3. **Choose destination** for each change:

#### For Public Release:
```bash
# Copy specific files to public repo staging
cp main.py /tmp/public-staging/
cp README.md /tmp/public-staging/
# Review, test, then:
git add main.py README.md
git commit -m "Description"
git push origin main
```

#### For Development:  
```bash
# All changes go to private
git add .
git commit -m "Development: description"  
git push private main
```

## 📝 File Decision Matrix

| File/Directory | Public | Private | Notes |
|----------------|---------|---------|-------|
| `main.py` | ✅ | ✅ | Core application |
| `requirements.txt` | ✅ | ✅ | Dependencies |
| `README.md` | ✅ | ✅ | Public documentation |
| `License` | ✅ | ✅ | MIT license |
| `.gitignore` | ✅ | ✅ | Different versions |
| `.claude/` | ❌ | ✅ | Development tools |
| `README-PRIVATE.md` | ❌ | ✅ | Internal docs |
| `archive/` | ❌ | ✅ | Development artifacts |
| `old/` | ❌ | ✅ | Version history |
| `REPO-MANAGEMENT.md` | ❌ | ✅ | This guide |
| `*.private` | ❌ | ✅ | Private suffixed files |

## 🔍 Pre-Push Checklist

### Before pushing to PUBLIC:
- [ ] No `.claude/` directory
- [ ] No `README-PRIVATE.md`
- [ ] No `.gitignore.private/.public`
- [ ] No `archive/` directory
- [ ] No `REPO-MANAGEMENT.md`
- [ ] Only essential files for users

### Before pushing to PRIVATE:
- [ ] All local files included
- [ ] Development tools preserved
- [ ] Archive directory included
- [ ] Management documentation updated

## 🚀 Quick Commands

### Status Check:
```bash
# Check what's in each repo
git ls-tree -r HEAD --name-only | grep -E "\.(claude|private)" && echo "❌ Private files detected in public repo" || echo "✅ Public repo clean"
```

### Emergency Cleanup:
```bash
# If private files leak to public
git rm -r .claude/
git rm README-PRIVATE.md
git rm .gitignore.private .gitignore.public
git rm REPO-MANAGEMENT.md
git commit -m "Emergency cleanup: Remove private files"
git push origin main
```

---
**⚠️ CRITICAL**: Always check file destinations before pushing!
**🔄 UPDATE**: Keep this guide updated as project evolves