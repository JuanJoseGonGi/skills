# File Structure and Progressive Disclosure

## How Skills are Loaded

Understanding the loading mechanism helps you structure skills efficiently:

1. **Metadata**: The `name` and `description` fields are loaded at startup (~100 tokens).
2. **Instructions**: The full `SKILL.md` body is loaded when the skill is activated (< 5000 tokens recommended).
3. **Resources**: Files in `references/`, `scripts/`, or `assets/` are loaded only when required.

## Recommended Directory Structure

### Simple Skill (Single File)
For straightforward skills under 200 lines:
```
my-skill/
└── SKILL.md
```

### Standard Skill (Multiple Files)
For skills with detailed documentation:
```
my-skill/
├── SKILL.md              # Overview and quick start
└── references/
    ├── REFERENCE.md      # API reference / detailed docs
    └── EXAMPLES.md       # Usage examples
```

### Complex Skill (With Scripts and Assets)
```
pdf-processing/
├── SKILL.md              # Instructions and workflow
├── references/
│   ├── FORMS.md          # Form-filling guide
│   └── REFERENCE.md      # API reference
├── scripts/
│   └── analyze_form.py   # Extract form fields
└── assets/
    └── template.pdf      # Template for testing
```

## Progressive Disclosure Patterns

### Pattern: High-Level Guide with References
`SKILL.md` provides an overview and links to details using relative paths:
```markdown
# PDF Processing

## Advanced Features
- **Form filling**: See [FORMS.md](references/FORMS.md)
- **API reference**: See [REFERENCE.md](references/REFERENCE.md)
```

## Best Practices

### Keep References One Level Deep
Avoid deeply nested reference chains. Keep all references directly accessible from `SKILL.md`.
```
# Good - One level
SKILL.md → references/advanced.md

# Bad - Too deep
SKILL.md → references/advanced.md → references/details.md
```

### Target Length
- **SKILL.md**: Under 500 lines (hard limit). Aim for 150-300.
- **Reference files**: Under 300 lines each.
- **Example files**: Under 200 lines each.

### Use Descriptive File Names
Names should indicate content (e.g., `api_authentication.md` not `doc1.md`).
