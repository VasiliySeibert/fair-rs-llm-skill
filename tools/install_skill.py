#!/usr/bin/env python3
"""Copy this skill into a local agent's discovery directory, without overwriting."""

import argparse
import os
import shutil
import sys
from pathlib import Path

NAME = "fair-research-software"
SOURCE = Path(__file__).resolve().parents[1] / "skills" / NAME
PROJECT_DIRS = {"codex": ".agents/skills", "claude": ".claude/skills", "opencode": ".opencode/skills"}
PERSONAL_DIRS = {"codex": ".agents/skills", "claude": ".claude/skills", "opencode": ".config/opencode/skills"}


def install(agent, project=None, home=None):
    home = Path(home) if home is not None else Path.home()
    if project is not None:
        root = Path(project).expanduser().resolve()
        if not root.is_dir():
            raise ValueError("project must be an existing directory")
        destination = root / PROJECT_DIRS[agent] / NAME
    else:
        if agent == "opencode" and os.environ.get("XDG_CONFIG_HOME"):
            config = Path(os.environ["XDG_CONFIG_HOME"]).expanduser()
            if not config.is_absolute():
                raise ValueError("XDG_CONFIG_HOME must be absolute")
            destination = config / "opencode" / "skills" / NAME
        else:
            destination = home / PERSONAL_DIRS[agent] / NAME
    if destination.exists() or destination.is_symlink():
        raise FileExistsError("installation already exists; review and move it aside before updating: " + str(destination))
    if not (SOURCE / "SKILL.md").is_file():
        raise ValueError("skill source is missing")
    shutil.copytree(SOURCE, destination, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    return destination


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--agent", required=True, choices=sorted(PROJECT_DIRS))
    parser.add_argument("--project", type=Path, help="Install for an existing project instead of the current user")
    args = parser.parse_args(argv)
    try:
        destination = install(args.agent, args.project)
    except (OSError, ValueError) as exc:
        print("install error: " + str(exc), file=sys.stderr)
        return 1
    print("Installed " + NAME + " at " + str(destination))
    print("Select the skill in your agent; refresh discovery if it is not yet listed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
