# Naming Conventions and Descriptions

## Skill Name Requirements

### Technical Constraints (Agent Skills Spec)

| Constraint | Requirement |
|-----------|-------------|
| Max length | 64 characters |
| Allowed chars | unicode lowercase alphanumeric characters and hyphens (`a-z` and `-`) |
| Forbidden | Spaces, underscores, uppercase, consecutive hyphens (`--`), non-alphanumeric chars |
| Start/End | Must not start or end with a hyphen |
| Directory | Must match the parent directory name |

### Naming Style: Gerund Form (Recommended)

Use verb + -ing form to clearly describe the activity:

| Good (Gerund) | Acceptable Alternative | Avoid |
|--------------|----------------------|-------|
| `processing-pdfs` | `pdf-processing` | `pdf-helper` |
| `analyzing-data` | `data-analysis` | `data-utils` |
| `testing-code` | `code-testing` | `test-tools` |

## Writing Effective Descriptions

### Format Requirements

| Field | Constraint |
|-------|-----------|
| Max length | 1024 characters |
| Required | Non-empty |

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

**Critical**: Descriptions are used for discovery. Inconsistent point-of-view causes problems.

| Good (Third Person) | Avoid |
|--------------------|-------|
| "Processes Excel files and generates reports" | "I can help you process Excel files" |

## Checklist

Before finalizing your skill name and description:

- [ ] Name matches the directory name exactly.
- [ ] Name uses gerund form (verb + -ing).
- [ ] Name is lowercase with hyphens only.
- [ ] Name is 1-64 characters and doesn't start/end with a hyphen.
- [ ] Description uses third person.
- [ ] Description explains what it does and when to use it.
- [ ] Description is specific with key search terms.
- [ ] Description is under 1024 characters.
