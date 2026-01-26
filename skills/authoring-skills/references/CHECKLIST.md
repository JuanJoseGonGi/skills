# Quality Checklist

Use this checklist before sharing a skill.

## Pre-Release Checklist

### Core Compliance
- [ ] Name matches the directory name exactly
- [ ] Name is lowercase, hyphens only, max 64 chars
- [ ] Name does not start or end with a hyphen
- [ ] No consecutive hyphens in name
- [ ] Frontmatter contains required `name` and `description` fields
- [ ] Description explains what it does AND when to use it
- [ ] Description uses third person voice
- [ ] Description is under 1024 characters
- [ ] `SKILL.md` body is under 500 lines

### Structure
- [ ] Relative paths used for all file references
- [ ] Detailed documentation in `references/` directory
- [ ] File references are only one level deep
- [ ] All file names are descriptive and lowercase
- [ ] No extraneous files (README.md, CHANGELOG.md, etc.)

### Content
- [ ] No time-sensitive information (or clearly marked)
- [ ] Consistent terminology throughout
- [ ] Concrete examples (input/output) provided where helpful
- [ ] Assumes the agent is already intelligent
- [ ] Avoids over-explaining basics

### Bundled Resources
- [ ] Scripts tested and working
- [ ] References contain only necessary detail
- [ ] Assets are appropriate file types
- [ ] Example/placeholder files removed if not needed

### Validation
- [ ] Pass `quick_validate.py` check
- [ ] Tested with real usage scenarios
- [ ] Navigation links verified and working

## Quick Validation Command

```bash
python scripts/quick_validate.py <skill-directory>
```
