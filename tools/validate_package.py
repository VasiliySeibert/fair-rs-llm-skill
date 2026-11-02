#!/usr/bin/env python3
"""Validate this package's portable subset, resources, and relative Markdown links."""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "fair-research-software"


def validate():
    errors = []
    text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    match = re.match(r"\A---\nname: ([a-z0-9]+(?:-[a-z0-9]+)*)\ndescription: (\"[^\n]+\")\n---\n", text)
    if not match:
        errors.append("SKILL.md must use the package's simple name/description frontmatter")
    else:
        name, description = match.groups()
        try:
            description = json.loads(description)
        except ValueError:
            errors.append("description must be a valid quoted string")
        if name != SKILL.name or len(name) > 64:
            errors.append("name must match its directory and be at most 64 characters")
        if not 1 <= len(description) <= 1024:
            errors.append("description length must be 1..1024 characters")
    if len(text.splitlines()) > 500:
        errors.append("SKILL.md exceeds the recommended 500 lines")
    if "[TODO:" in text:
        errors.append("SKILL.md contains unfinished scaffolding")
    for path in ROOT.rglob("*.md"):
        if any(part in {".venv", ".git", "reports"} for part in path.relative_to(ROOT).parts):
            continue
        for destination in re.findall(r"\[[^\]]*\]\(([^)]+)\)", path.read_text(encoding="utf-8")):
            if re.match(r"[a-z]+:", destination) or destination.startswith("#"):
                continue
            target = (path.parent / destination.split("#", 1)[0]).resolve()
            if not target.exists():
                errors.append(str(path.relative_to(ROOT)) + ": missing link " + destination)
    for required in ["scripts/audit_repository.py", "assets/audit-report.md", "agents/openai.yaml"]:
        if not (SKILL / required).is_file():
            errors.append("missing resource: " + required)
    for path in SKILL.glob("references/*.md"):
        if "references/" + path.name not in text:
            errors.append("reference is not discoverable from SKILL.md: " + path.name)
    return errors


if __name__ == "__main__":
    errors = validate()
    if errors:
        print("\n".join(errors), file=sys.stderr)
        sys.exit(1)
    print("Package structure, portable frontmatter, resources, and local links validated.")
