# Output Patterns

Use these patterns when skills need to produce consistent, high-quality output.

## Template Pattern

Provide templates for output format. Match strictness to requirements.

### Strict Requirements (API responses, data formats)

```markdown
## Report Structure

ALWAYS use this exact template:

# [Analysis Title]

## Executive Summary
[One-paragraph overview of key findings]

## Key Findings
- Finding 1 with supporting data
- Finding 2 with supporting data

## Recommendations
1. Specific actionable recommendation
2. Specific actionable recommendation
```

### Flexible Guidance (when adaptation is useful)

```markdown
## Report Structure

Sensible default format (adapt as needed):

# [Analysis Title]

## Executive Summary
[Overview]

## Key Findings
[Adapt sections based on what you discover]

## Recommendations
[Tailor to the specific context]
```

## Examples Pattern

For skills where output quality depends on seeing examples, provide input/output pairs:

```markdown
## Commit Message Format

Generate commit messages following these examples:

**Example 1:**
Input: Added user authentication with JWT tokens
Output:
feat(auth): implement JWT-based authentication

Add login endpoint and token validation middleware

**Example 2:**
Input: Fixed bug where dates displayed incorrectly
Output:
fix(reports): correct date formatting in timezone conversion

Use UTC timestamps consistently across report generation
```

Examples help the agent understand desired style better than descriptions alone.

## Checklist Pattern

For multi-step quality assurance:

```markdown
## Before Submitting

Verify:
- [ ] All required fields populated
- [ ] Format matches specification
- [ ] No placeholder text remains
- [ ] Links are valid
```
