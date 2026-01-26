#!/usr/bin/env python3
"""
Quick validation script for skills

Usage:
    quick_validate.py <skill_directory>
"""

import sys
import re
from pathlib import Path


ALLOWED_PROPERTIES = {"name", "description", "license", "allowed-tools", "metadata"}


def parse_simple_yaml(text):
    """
    Parse simple YAML frontmatter without external dependencies.
    Only handles flat key-value pairs (no nested structures).
    """
    result = {}
    for line in text.strip().split("\n"):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        # Match key: value pattern
        match = re.match(r"^([a-zA-Z_-]+):\s*(.*)$", line)
        if match:
            key = match.group(1)
            value = match.group(2).strip()
            # Remove surrounding quotes if present
            if (value.startswith('"') and value.endswith('"')) or (
                value.startswith("'") and value.endswith("'")
            ):
                value = value[1:-1]
            result[key] = value
    return result


def validate_skill(skill_path):
    """
    Validate a skill directory.

    Returns:
        tuple: (is_valid: bool, message: str)
    """
    skill_path = Path(skill_path).resolve()

    # Check SKILL.md exists
    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        return False, "SKILL.md not found"

    # Read and validate frontmatter
    content = skill_md.read_text()
    if not content.startswith("---"):
        return False, "No YAML frontmatter found"

    # Extract frontmatter
    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return False, "Invalid frontmatter format"

    frontmatter_text = match.group(1)

    # Parse YAML frontmatter
    try:
        frontmatter = parse_simple_yaml(frontmatter_text)
        if not isinstance(frontmatter, dict):
            return False, "Frontmatter must be a YAML dictionary"
    except Exception as e:
        return False, f"Invalid YAML in frontmatter: {e}"

    # Check for unexpected properties
    unexpected_keys = set(frontmatter.keys()) - ALLOWED_PROPERTIES
    if unexpected_keys:
        return False, (
            f"Unexpected key(s) in frontmatter: {', '.join(sorted(unexpected_keys))}. "
            f"Allowed: {', '.join(sorted(ALLOWED_PROPERTIES))}"
        )

    # Check required fields
    if "name" not in frontmatter:
        return False, "Missing 'name' in frontmatter"
    if "description" not in frontmatter:
        return False, "Missing 'description' in frontmatter"

    # Validate name
    name = frontmatter.get("name", "")
    if not isinstance(name, str):
        return False, f"Name must be a string, got {type(name).__name__}"
    name = name.strip()

    if name:
        if not re.match(r"^[a-z0-9-]+$", name):
            return (
                False,
                f"Name '{name}' should be hyphen-case (lowercase letters, digits, and hyphens only)",
            )
        if name.startswith("-") or name.endswith("-") or "--" in name:
            return (
                False,
                f"Name '{name}' cannot start/end with hyphen or contain consecutive hyphens",
            )
        if len(name) > 64:
            return (
                False,
                f"Name is too long ({len(name)} chars). Maximum is 64 characters.",
            )

        # Check name matches directory
        if name != skill_path.name:
            return (
                False,
                f"Name '{name}' does not match directory name '{skill_path.name}'",
            )

    # Validate description
    description = frontmatter.get("description", "")
    if not isinstance(description, str):
        return False, f"Description must be a string, got {type(description).__name__}"
    description = description.strip()

    if description:
        if "<" in description or ">" in description:
            return False, "Description cannot contain angle brackets (< or >)"
        if len(description) > 1024:
            return (
                False,
                f"Description is too long ({len(description)} chars). Maximum is 1024 characters.",
            )

    # Check SKILL.md line count
    lines = content.split("\n")
    if len(lines) > 500:
        return False, f"SKILL.md has {len(lines)} lines. Maximum recommended is 500."

    return True, "Skill is valid!"


def main():
    if len(sys.argv) != 2:
        print("Usage: quick_validate.py <skill_directory>")
        sys.exit(1)

    skill_path = sys.argv[1]
    valid, message = validate_skill(skill_path)

    print(message)
    sys.exit(0 if valid else 1)


if __name__ == "__main__":
    main()
