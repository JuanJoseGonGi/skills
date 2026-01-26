# Naming Conventions and Descriptions

## Skill Name Requirements

### Technical Constraints

| Constraint | Requirement |
|-----------|-------------|
| Max length | 64 characters |
| Allowed chars | Lowercase alphanumeric and hyphens (`a-z`, `0-9`, `-`) |
| Forbidden | Spaces, underscores, uppercase, consecutive hyphens (`--`) |
| Start/End | Must not start or end with a hyphen |
| Directory | Must match the parent directory name exactly |

### Naming Style: Gerund Form (Recommended)

Use verb + -ing form to clearly describe the activity:

| Good (Gerund) | Acceptable | Avoid |
|--------------|------------|-------|
| `processing-pdfs` | `pdf-processing` | `pdf-helper` |
| `analyzing-data` | `data-analysis` | `data-utils` |
| `testing-code` | `code-testing` | `test-tools` |
| `building-apis` | `api-builder` | `api-stuff` |

## Writing Effective Descriptions

### Format Requirements

| Field | Constraint |
|-------|-----------|
| Max length | 1024 characters |
| Required | Non-empty |
| Forbidden | Angle brackets (< or >) |

### The Two-Part Formula

Every description must answer:
1. **What does it do?** (capability)
2. **When to use it?** (trigger conditions)

```yaml
# Template
description: [What it does]. Use when [trigger conditions].

# Example
description: Extracts text and tables from PDF files. Use when working with PDF files or when the user mentions PDFs, forms, or document extraction.
```

### Point of View: Always Third Person

Descriptions are used for discovery. Inconsistent point-of-view causes problems.

| Good (Third Person) | Avoid |
|--------------------|-------|
| "Processes Excel files and generates reports" | "I can help you process Excel files" |
| "Creates deployment configurations for cloud providers" | "Use me to create deployments" |

### Include Key Search Terms

Think about what words users might say that should trigger this skill:

```yaml
# Good - includes relevant terms
description: Comprehensive document creation, editing, and analysis with support for tracked changes, comments, formatting preservation, and text extraction. Use when working with professional documents (.docx files).

# Bad - too vague
description: Handles documents.
```

## Checklist

Before finalizing:

- [ ] Name matches the directory name exactly
- [ ] Name uses gerund form (verb + -ing) when possible
- [ ] Name is lowercase with hyphens only
- [ ] Name is 1-64 characters
- [ ] Name doesn't start/end with a hyphen
- [ ] No consecutive hyphens
- [ ] Description uses third person
- [ ] Description explains what it does and when to use it
- [ ] Description includes key search terms
- [ ] Description is under 1024 characters
- [ ] No angle brackets in description
