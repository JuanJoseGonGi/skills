---
name: authoring-skills
description: Guides the creation of effective AI Agent Skills. Use when creating new skills, improving existing skills, or reviewing skill quality. Covers the full workflow from understanding requirements through packaging, including scripts for initialization and validation.
---

# Agent Skills Authoring Guide

This skill provides best practices for creating effective AI Agent Skills that extend Claude's capabilities with specialized knowledge, workflows, and tools.

## Core Principles

### 1. Concise is Key

The context window is a shared resource. Challenge each piece of information:
- "Does the agent really need this explanation?"
- "Does this paragraph justify its token cost?"

**Default assumption**: The agent is already very smart. Only add context it doesn't already have. Prefer concise examples over verbose explanations.

### 2. Progressive Disclosure

Skills use a three-level loading system:

1. **Metadata** (name + description) - Always in context (~100 words)
2. **SKILL.md body** - When skill triggers (< 500 lines)
3. **Bundled resources** - As needed (unlimited, scripts can execute without reading)

Keep `SKILL.md` lean. Split content into `references/` when approaching limits. Always clearly reference external files so the agent knows they exist.

### 3. Appropriate Degrees of Freedom

Match specificity to task fragility:

| Freedom | Use When | Example |
|---------|----------|---------|
| **High** (text instructions) | Multiple approaches valid | Code review guidelines |
| **Medium** (pseudocode) | Preferred pattern exists | Report templates |
| **Low** (specific scripts) | Operations are fragile | Database migrations |

## Skill Anatomy

```
skill-name/
├── SKILL.md              # Required: frontmatter + instructions
├── scripts/              # Optional: executable code
├── references/           # Optional: detailed documentation
└── assets/               # Optional: templates, images, files for output
```

### YAML Frontmatter

```yaml
---
name: skill-name        # lowercase, hyphens, max 64 chars, must match directory
description: What it does. Use when [triggers].  # max 1024 chars, third person
---
```

**Description must include**:
- What the skill does (capability)
- When to use it (trigger conditions)

See [NAMING.md](references/NAMING.md) for detailed naming conventions.

### Bundled Resources

| Directory | Purpose | When to Include |
|-----------|---------|-----------------|
| `scripts/` | Executable code (Python/Bash) | Same code rewritten repeatedly; deterministic reliability needed |
| `references/` | Documentation loaded into context | Detailed info only needed for specific use cases |
| `assets/` | Files used in output (not loaded) | Templates, images, boilerplate for final output |

**Important**: Don't create extraneous files (README.md, CHANGELOG.md, etc.). Skills contain only what the agent needs to do the job.

See [STRUCTURE.md](references/STRUCTURE.md) for organization patterns.

## Skill Creation Workflow

### Step 1: Understand with Concrete Examples

Skip only if usage patterns are clearly understood.

Ask clarifying questions to understand how the skill will be used:
- "What functionality should this skill support?"
- "Can you give examples of how it would be used?"
- "What would a user say that should trigger this skill?"

Avoid overwhelming users. Start with the most important questions.

### Step 2: Plan Reusable Contents

For each example, analyze:
1. How would you execute this from scratch?
2. What scripts/references/assets would help when doing this repeatedly?

**Example analyses**:
- PDF rotation → `scripts/rotate_pdf.py` (same code each time)
- Frontend webapp → `assets/hello-world/` template (same boilerplate)
- BigQuery queries → `references/schema.md` (rediscovering schemas each time)

### Step 3: Initialize the Skill

For new skills, run the initialization script:

```bash
python scripts/init_skill.py <skill-name> --path <output-directory>
```

This creates a template with proper structure and TODO placeholders.

Skip if iterating on an existing skill.

### Step 4: Edit the Skill

Start with bundled resources (scripts, references, assets), then update SKILL.md.

**For scripts**: Test by actually running them to verify they work.

**For SKILL.md**:
- Write for another Claude instance to use
- Include non-obvious procedural knowledge
- Delete example files/directories not needed
- Reference design patterns: [WORKFLOWS.md](references/WORKFLOWS.md), [OUTPUT-PATTERNS.md](references/OUTPUT-PATTERNS.md)

### Step 5: Package the Skill

```bash
python scripts/package_skill.py <path/to/skill-folder> [output-directory]
```

The script validates then creates a `.skill` file (zip format).

### Step 6: Iterate

1. Use the skill on real tasks
2. Notice struggles or inefficiencies
3. Update SKILL.md or bundled resources
4. Test again

See [WORKFLOWS.md](references/WORKFLOWS.md) for iteration patterns.

## Validation

Before sharing, verify:

```bash
python scripts/quick_validate.py <skill-directory>
```

Or use the full checklist: [CHECKLIST.md](references/CHECKLIST.md)

## Reference Documentation

- **[NAMING.md](references/NAMING.md)**: Naming conventions and description guidelines
- **[STRUCTURE.md](references/STRUCTURE.md)**: File organization and progressive disclosure
- **[WORKFLOWS.md](references/WORKFLOWS.md)**: Workflow patterns and iteration
- **[OUTPUT-PATTERNS.md](references/OUTPUT-PATTERNS.md)**: Template and example patterns for output
- **[CHECKLIST.md](references/CHECKLIST.md)**: Quality checklist before sharing
