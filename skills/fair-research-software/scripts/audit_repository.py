#!/usr/bin/env python3
"""Read-only local evidence checks. Does not certify FAIRness or run target code."""

import argparse
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None

SKIP_DIRS = {".git", ".hg", ".svn", ".venv", "venv", "node_modules",
             "__pycache__", ".tox", ".mypy_cache", "build", "dist"}
MAX_METADATA_BYTES = 2_000_000


def git(root, *args):
    """Run a fixed, read-only Git command, never a repository-provided command."""
    try:
        result = subprocess.run(
            ["git", "-c", "core.fsmonitor=false", "-C", str(root), *args],
            capture_output=True, timeout=15, check=False,
            env=dict(os.environ, GIT_OPTIONAL_LOCKS="0"),
        )
    except (OSError, subprocess.TimeoutExpired):
        return None
    return result.stdout.decode("utf-8", errors="replace") if result.returncode == 0 else None


def safe_file(root, relative):
    """Reject symlinks (including directory symlinks) and paths outside the root."""
    path = root / relative
    try:
        path.resolve().relative_to(root)
        if any(p.is_symlink() for p in [path, *path.parents] if p != root and root in p.parents):
            return False
        return path.is_file()
    except (ValueError, OSError, RuntimeError):
        return False


def inventory(root):
    top = git(root, "rev-parse", "--show-toplevel")
    is_repo_root = bool(top and Path(top.strip()).resolve() == root)
    names = None
    if is_repo_root:
        listing = git(root, "ls-files", "--cached", "--others", "--exclude-standard", "-z")
        if listing is not None:
            names = set(filter(None, listing.split("\0")))
    if names is None:
        names = set()
        def onerror(error):
            raise error
        for current, dirs, files in os.walk(root, followlinks=False, onerror=onerror):
            dirs[:] = sorted(d for d in dirs if d not in SKIP_DIRS and not (Path(current) / d).is_symlink())
            for name in files:
                names.add((Path(current) / name).relative_to(root).as_posix())
    excluded = sorted(name for name in names if not safe_file(root, name))
    return sorted(names.difference(excluded)), excluded, is_repo_root


def read_text(root, name):
    if not safe_file(root, name):
        raise ValueError("not a regular file inside the repository")
    path = root / name
    if path.stat().st_size > MAX_METADATA_BYTES:
        raise ValueError("metadata exceeds the 2 MB inspection limit")
    return path.read_text(encoding="utf-8")


def unique_json(pairs):
    obj = {}
    for key, value in pairs:
        if key in obj:
            raise ValueError("duplicate JSON key: " + key)
        obj[key] = value
    return obj


def parse_yaml(text):
    """Safe YAML with duplicate-key rejection; optional dependency."""
    class UniqueLoader(yaml.SafeLoader):
        pass

    def mapping(loader, node, deep=False):
        loader.flatten_mapping(node)
        result = {}
        for key_node, value_node in node.value:
            key = loader.construct_object(key_node, deep=deep)
            if key in result:
                raise ValueError("duplicate YAML key: " + str(key))
            result[key] = loader.construct_object(value_node, deep=deep)
        return result

    UniqueLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, mapping)
    return yaml.load(text, Loader=UniqueLoader)


def normalize_doi(value):
    return re.sub(r"^(?:https?://(?:dx\.)?doi\.org/|doi:\s*)", "", str(value).strip(), flags=re.I).lower()


def audit(root):
    root = Path(root).expanduser().resolve()
    if not root.is_dir():
        raise ValueError("repository must be an existing directory")
    files, excluded, is_repo_root = inventory(root)
    checks = []
    parsed = {}

    def add(identifier, status, claim, evidence=None, detail=""):
        checks.append({"id": identifier, "status": status, "claim": claim,
                       "evidence": evidence or [], "detail": detail})

    def presence(identifier, claim, matches, detail):
        add(identifier, "verified" if matches else "failed", claim, matches, detail)

    top = {f.lower(): f for f in files if "/" not in f}
    readmes = [f for lower, f in top.items() if re.fullmatch(r"readme(?:\.(?:md|rst|txt))?", lower)]
    licenses = [f for f in files if
                re.fullmatch(r"(?:license|licence|copying)(?:[.-].+)?", f.lower())
                or (f.startswith("LICENSES/") and f.lower().endswith(".txt"))]
    presence("readme", "Root README is present", readmes, "Contents and usability require review.")
    presence("license-files", "License text location is present", licenses,
             "Presence does not establish coverage, rights, or license compatibility.")
    presence("citation-file", "Root CITATION.cff convention is present",
             [top["citation.cff"]] if "citation.cff" in top else [],
             "A missing convention is a review candidate, not a FAIR verdict.")
    presence("discovery-metadata", "Root CodeMeta or Zenodo metadata is present",
             [top[n] for n in ("codemeta.json", ".zenodo.json") if n in top],
             "Other discovery mechanisms may be appropriate; assess applicability.")

    for expected in ("CITATION.cff", "codemeta.json", ".zenodo.json", "ro-crate-metadata.json"):
        name = top.get(expected.lower())
        if not name:
            continue
        identifier = "parse-" + expected.lower()
        if expected == "CITATION.cff" and yaml is None:
            add(identifier, "not_checked", "CFF syntax and mapping structure", [name], "Install PyYAML to enable parsing.")
            continue
        try:
            text = read_text(root, name)
            data = parse_yaml(text) if expected == "CITATION.cff" else json.loads(text, object_pairs_hook=unique_json)
            if not isinstance(data, dict):
                raise ValueError("metadata root must be a mapping/object")
            parsed[expected] = data
            add(identifier, "verified", expected + " syntax and mapping structure", [name],
                "Full schema validation and factual correctness are separate checks.")
            if re.search(r"\bREPLACE_[A-Z0-9_]+\b", text):
                add("placeholders-" + expected.lower(), "failed", "Release metadata has no template placeholders", [name],
                    "Resolve or remove REPLACE_... values before release.")
        except Exception as exc:
            add(identifier, "failed", expected + " syntax and mapping structure", [name],
                "Could not parse safely: " + type(exc).__name__)

    if "citation.cff" in top and ".zenodo.json" in top:
        add("zenodo-precedence", "verified", "Both Zenodo ingestion metadata files are present",
            [top["citation.cff"], top[".zenodo.json"]],
            ".zenodo.json takes precedence over CITATION.cff; review it for stale metadata.")

    versions = {name: str(data["version"]).strip() for name, data in parsed.items()
                if "version" in data and data["version"] is not None and str(data["version"]).strip()}
    if len(versions) > 1:
        normalized = {v[1:] if re.match(r"^v\d", v) else v for v in versions.values()}
        add("version-consistency", "verified" if len(normalized) == 1 else "failed",
            "Explicit versions agree across parsed root metadata", list(versions),
            json.dumps(versions, sort_keys=True))
    else:
        add("version-consistency", "not_checked", "Explicit versions agree across parsed root metadata",
            list(versions), "At least two parseable explicit versions are required for this comparison.")

    cff = parsed.get("CITATION.cff")
    if cff is not None:
        identifiers = cff.get("identifiers", [])
        if not isinstance(identifiers, list):
            add("doi-role-consistency", "failed", "CFF DOI role annotations do not conflict",
                ["CITATION.cff"], "identifiers must be a list; run the CFF schema validator.")
        else:
            roles = {}
            for entry in identifiers:
                if not isinstance(entry, dict) or str(entry.get("type", "")).lower() != "doi":
                    continue
                doi = normalize_doi(entry.get("value", ""))
                desc = str(entry.get("description", "")).lower()
                if not doi:
                    continue
                if "concept" in desc or "all versions" in desc:
                    roles.setdefault(doi, set()).add("concept")
                elif re.search(r"\bversion\b|\brelease\b", desc):
                    roles.setdefault(doi, set()).add("version")
            conflicts = sorted(doi for doi, role in roles.items() if len(role) > 1)
            add("doi-role-consistency", "failed" if conflicts else "not_checked",
                "CFF DOI role annotations do not conflict", ["CITATION.cff"],
                "Same DOI labelled concept and version: " + ", ".join(conflicts) if conflicts else
                "No explicit duplicate-role conflict detected; archive relations are not checked.")

    envs = [f for f in files if Path(f).name.lower() in
            {"pyproject.toml", "requirements.txt", "environment.yml", "environment.yaml",
             "project.toml", "manifest.toml", "dockerfile", "renv.lock", "uv.lock",
             "poetry.lock", "package-lock.json", "pixi.lock", "conda-lock.yml"}
            or re.fullmatch(r"environment_.+\.ya?ml", Path(f).name.lower())]
    workflows = [f for f in files if f.startswith(".github/workflows/") and f.endswith((".yml", ".yaml"))]
    reuse_files = [f for f in files if f in {"REUSE.toml", ".reuse/dep5"}]
    add("environment-evidence", "verified" if envs else "not_checked", "Environment definition locations",
        envs, "Candidate files only; version pinning and execution are not checked.")
    add("ci-evidence", "verified" if workflows else "not_checked", "GitHub Actions definition locations",
        workflows, "No live CI status or scientific result has been checked.")
    add("reuse-evidence", "verified" if reuse_files else "not_checked", "REUSE annotation manifest locations",
        reuse_files, "Headers and sidecars may also provide coverage; run reuse lint separately.")
    for identifier, claim in [
        ("schema-validation", "Metadata complies with applicable complete schemas"),
        ("license-coverage", "File licensing coverage and rights are verified"),
        ("zenodo-archive", "Intended release is archived and DOI relations verified"),
        ("software-heritage", "Intended source revision is archived with a verified SWHID"),
        ("execution", "Documented scientific computation reproduces its expected results"),
    ]:
        add(identifier, "not_checked", claim, detail="Requires a separate scoped validation step.")

    head = git(root, "rev-parse", "HEAD") if is_repo_root else None
    state = git(root, "status", "--porcelain", "--untracked-files=normal") if is_repo_root else None
    return {"report_schema_version": "1.0", "generated_at": datetime.now(timezone.utc).isoformat(),
            "repository": str(root), "commit": head.strip() if head else None,
            "dirty": bool(state.strip()) if state is not None else None,
            "inventory_method": "git" if is_repo_root else "filesystem",
            "files_inspected_for_inventory": len(files), "excluded_paths": excluded,
            "tools": {"python": sys.version.split()[0], "pyyaml": getattr(yaml, "__version__", None)},
            "scope": "Local static checks only; no FAIR certification, network checks, or target execution.",
            "checks": checks}


def markdown(report):
    def cell(value):
        return str(value).replace("\n", " ").replace("|", "\\|")
    lines = ["# Local FAIR practice evidence", "", report["scope"], "",
             "Revision: " + (report["commit"] or "unavailable"), "",
             "| Check | Status | Evidence | Limitation / detail |",
             "| --- | --- | --- | --- |"]
    for check in report["checks"]:
        lines.append("| " + " | ".join(cell(v) for v in [check["claim"], check["status"],
                     ", ".join(check["evidence"]), check["detail"]]) + " |")
    return "\n".join(lines)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repository", type=Path)
    parser.add_argument("--format", choices=["json", "markdown"], default="json")
    parser.add_argument("--strict", action="store_true", help="Return 1 if local checks fail; unchecked is not pass")
    args = parser.parse_args(argv)
    try:
        report = audit(args.repository)
    except (OSError, ValueError, RuntimeError) as exc:
        print("audit error: " + str(exc), file=sys.stderr)
        return 2
    print(json.dumps(report, indent=2, ensure_ascii=False) if args.format == "json" else markdown(report))
    return 1 if args.strict and any(c["status"] == "failed" for c in report["checks"]) else 0


if __name__ == "__main__":
    sys.exit(main())
