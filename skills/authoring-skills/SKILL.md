---
name: authoring-skills
description: Guides the creation of effective AI Agent Skills following the Agent Skills specification. Use when creating new skills, improving existing skills, or reviewing skill quality. Covers naming conventions, file structure, progressive disclosure, and validation.
---

# Agent Skills Authoring Guide

## Overview

This skill provides best practices for creating effective AI Agent Skills that are discoverable, concise, and compliant with the [Agent Skills specification](https://agentskills.io/).

## When to Use

- **Creating new skills**: Before writing a new `SKILL.md`
- **Improving existing skills**: When refactoring or enhancing skills
- **Reviewing skill quality**: For code review of skill files
- **Ensuring compliance**: To validate skills against the official specification

## Core Principles

### 1. Concise is Key

The context window is a shared resource. Challenge each piece of information:
- "Does the agent really need this explanation?"
- "Can I assume the agent knows this?"
- "Does this paragraph justify its token cost?"

**Default assumption**: The agent is already very smart. Only add context it doesn't already have.

### 2. Progressive Disclosure

`SKILL.md` serves as an overview that points to detailed materials as needed:
- Keep `SKILL.md` body under **500 lines**.
- Split content into separate files (typically in `references/`) when approaching this limit.
- Agents load additional files only when needed.

### 3. Appropriate Degrees of Freedom

Match specificity to task fragility:

| Freedom Level | Use When | Example |
|--------------|----------|---------|
| **High** (text instructions) | Multiple approaches valid | Code review guidelines |
| **Medium** (pseudocode) | Preferred pattern exists | Report templates |
| **Low** (specific scripts) | Operations are fragile | Database migrations |

## Quick Reference

### YAML Frontmatter Requirements

```yaml
---
name: skill-name        # lowercase, hyphens, max 64 chars
description: Describes what it does and when to use it.  # max 1024 chars
---
```

**Naming convention**: Use gerund form (verb + -ing) or action-oriented names.
- Good: `processing-pdfs`, `analyzing-data`, `testing-code`
- Avoid: `helper`, `utils`, `tools`

**Description rules**:
- Always write in **third person**.
- Include what the skill does AND when to use it.
- Be specific and include key terms for discovery.

See [NAMING.md](references/NAMING.md) for detailed guidelines.

### Directory Structure

A skill must be a directory containing at minimum a `SKILL.md` file:

```
skill-name/
└── SKILL.md          # Required
```

Optional subdirectories:
- `references/`: Technical references and detailed docs.
- `scripts/`: Executable code (Python, Bash, JS).
- `assets/`: Templates, images, or static data.

See [STRUCTURE.md](references/STRUCTURE.md) for organization patterns.

## Skill Creation Workflow

### Step 1: Identify the Gap
Before writing documentation, identify what the agent struggles with:
1. Run representative tasks without a skill.
2. Document specific failures or missing context.

### Step 2: Write Minimal Instructions
Create just enough content to address the gaps. Ensure the `name` field matches the parent directory.

### Step 3: Validate and Iterate
1. Use the `skills-ref` tool to validate: `skills-ref validate ./my-skill`
2. Test with real usage scenarios.
3. Refine based on agent performance.

See [WORKFLOWS.md](references/WORKFLOWS.md) for detailed development workflow.

## Detailed Documentation

- **[NAMING.md](references/NAMING.md)**: Naming conventions and description guidelines.
- **[STRUCTURE.md](references/STRUCTURE.md)**: File organization and progressive disclosure.
- **[WORKFLOWS.md](references/WORKFLOWS.md)**: Development workflow and iteration.
- **[CHECKLIST.md](references/CHECKLIST.md)**: Quality checklist before sharing.

## Related Skills

- **applying-solid-principles**: Code quality for utility scripts.
- **securing-code**: Security standards for skill implementation.
