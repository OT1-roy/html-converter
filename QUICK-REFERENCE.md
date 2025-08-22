# 🚀 Quick Reference - Dual Repo Management

## 📋 Daily Checklist

### Before Any Push:
```bash
# Check which files you're about to push
git ls-tree -r HEAD --name-only

# ❌ If you see these in PUBLIC repo - STOP!
.claude/
README-PRIVATE.md
.gitignore.private
.gitignore.public  
archive/
REPO-MANAGEMENT.md
QUICK-REFERENCE.md
```

## 🎯 Push Destinations

### 🌍 Public Repo (origin)
**ONLY include:**
- `main.py` (now with dual-engine support v2.0.0)
- `html-to-md-cli.js` (Node.js wrapper for Markdown conversion)
- `requirements.txt` 
- `README.md` (updated with dual-library installation)
- `License`
- `.gitignore` (public version)

### 🔒 Private Repo (private)  
**Include EVERYTHING**

## ⚡ Quick Commands

### Status Check:
```bash
git remote -v                    # Show remotes
git branch -vv                   # Show tracking branches
```

### Emergency Public Cleanup:
```bash
git rm -rf .claude/
git rm README-PRIVATE.md .gitignore.private .gitignore.public
git rm REPO-MANAGEMENT.md QUICK-REFERENCE.md archive/
git commit -m "Emergency: Remove private files"
git push origin main
```

### Switch Contexts:
```bash
# For public release (restrictive .gitignore)
cp .gitignore.public .gitignore
git add main.py requirements.txt README.md License .gitignore
git push origin main

# For private development (permissive .gitignore)  
cp .gitignore.private .gitignore
git add .
git push private main
```

## 🚨 Red Flags
- ❌ `.claude/` visible in public GitHub
- ❌ `README-PRIVATE.md` in public repo
- ❌ Missing `archive/` in private repo
- ❌ Private repo smaller than local directory

---
**💡 Tip**: When in doubt, push to private first, then selectively copy to public!