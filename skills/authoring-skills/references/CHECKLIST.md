# Quality Checklist

Use this checklist before sharing a skill.

## Pre-Release Checklist

### CORE COMPLIANCE
- [ ] Name matches the directory name exactly.
- [ ] Name is lowercase, hyphens only, max 64 chars.
- [ ] Name does not start or end with a hyphen.
- [ ] Frontmatter contains required `name` and `description` fields.
- [ ] Description explains what the skill does AND when to use it.
- [ ] Description uses third person voice.
- [ ] `SKILL.md` body is under 500 lines.

### STRUCTURE
- [ ] Relative paths are used for all file references.
- [ ] Detailed documentation is in the `references/` directory.
- [ ] File references are only one level deep.
- [ ] All file names are descriptive and lowercase.

### CONTENT
- [ ] No time-sensitive information (or clearly marked as legacy).
- [ ] Consistent terminology used throughout.
- [ ] Concrete examples (input/output) provided.
- [ ] Assumes the agent is already intelligent; avoids over-explaining basics.

### VALIDATION
- [ ] Pass `skills-ref validate [path]` check.
- [ ] Tested with real usage scenarios and fresh agent instances.
- [ ] Navigation links verified and working.
