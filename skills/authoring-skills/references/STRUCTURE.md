# File Structure and Progressive Disclosure

## How Skills are Loaded

Understanding the loading mechanism helps structure skills efficiently:

1. **Metadata**: `name` and `description` fields loaded at startup (~100 tokens)
2. **Instructions**: Full `SKILL.md` body loaded when skill activates (< 5000 tokens recommended)
3. **Resources**: Files in `references/`, `scripts/`, `assets/` loaded only when required

## Directory Structures

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
    └── template.pdf      # Template for output
```

### Domain-Specific Organization
For skills with multiple domains, organize by domain:
```
bigquery-skill/
├── SKILL.md              # Overview and navigation
└── references/
    ├── finance.md        # Revenue, billing metrics
    ├── sales.md          # Opportunities, pipeline
    ├── product.md        # API usage, features
    └── marketing.md      # Campaigns, attribution
```

When user asks about sales, agent only reads `sales.md`.

### Multi-Framework Organization
```
cloud-deploy/
├── SKILL.md              # Workflow + provider selection
└── references/
    ├── aws.md            # AWS patterns
    ├── gcp.md            # GCP patterns
    └── azure.md          # Azure patterns
```

## Progressive Disclosure Patterns

### Pattern: High-Level Guide with References
`SKILL.md` provides overview, links to details:
```markdown
# PDF Processing

## Advanced Features
- **Form filling**: See [FORMS.md](references/FORMS.md)
- **API reference**: See [REFERENCE.md](references/REFERENCE.md)
```

### Pattern: Conditional Details
Show basic content, link to advanced:
```markdown
# DOCX Processing

## Creating Documents
Use docx-js for new documents. See [DOCX-JS.md](references/DOCX-JS.md).

## Editing Documents
For simple edits, modify XML directly.

**For tracked changes**: See [REDLINING.md](references/REDLINING.md)
```

## Best Practices

### Keep References One Level Deep
All references should link directly from SKILL.md:
```
Good:  SKILL.md -> references/advanced.md
Bad:   SKILL.md -> references/advanced.md -> references/details.md
```

### Target Lengths
- **SKILL.md**: Under 500 lines (aim for 150-300)
- **Reference files**: Under 300 lines each
- **Example files**: Under 200 lines each

### Use Descriptive File Names
Names should indicate content: `api_authentication.md` not `doc1.md`

### Structure Longer Reference Files
For files over 100 lines, include a table of contents so the agent can see the scope when previewing.
