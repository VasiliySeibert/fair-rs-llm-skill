# Validation record

Date: 2026-11-02. Environment: macOS arm64.

| Check | Observed result |
| --- | --- |
| Package structure, frontmatter, resources, relative links | Passed |
| Codex skill-creator quick validator | Passed with Python 3.12.3 / PyYAML 6.0.3 |
| Python 3.12.3, PyYAML 6.0.3 | All 21 unit tests passed |
| Python 3.9.6, no PyYAML | 16 tests passed; 2 YAML-dependent and 3 TOML-dependent tests explicitly skipped |
| Installer | Project paths for all three agents and personal/XDG paths tested in temporary directories; existing installs preserved |
| Fresh awesome-sim clone | Clean revision 39b1aa986ee42de7b4b37abf15a7850d43cabf5a; CFF, CodeMeta, and package versions agree at 1.1.0; no local helper failures |
| Fresh plate-with-hole clone | Clean revision 5a8dffb551334e693f45235c1816edc9e45743d1; duplicated DOI roles detected; benchmark and solver versions are treated separately |
| Actual slide source | Read origin/gh-pages at e354ef2e567223ab8ba6eaac3d572d589efb5ab8, including Zenodo webhook and preservation guidance |
| Source links | Every pinned source path in the traceability table checked against its cloned Git object |
| Independent agent trial | Audited a synthetic heat-example project with this skill; reported conflicting versions and DOI roles, missing rights, unavailable solver, and unsupported plot claim |
| External/archive claims in trial | Correctly left unverified; no target edits or publication |

The independent trial used a fresh agent context with the skill and example files,
without the evaluator's expected conclusions. It is one behavioural trial, not a
comparison across Codex, Claude Code, OpenCode, or open-weight models.

The tests additionally confirm that the checker does not run target scripts,
dynamic version build backends, or Git fsmonitor hooks; skips out-of-root
symlinks; reports missing YAML/TOML support honestly; and rejects duplicate
JSON/YAML/TOML metadata keys. Result-crate and nested benchmark versions are
excluded from software version comparisons.

The fresh clone review supersedes the initial source acquisition limitation and
older benchmark checkout used during scaffolding. Source revisions and their
derived practices are in [source-traceability.md](source-traceability.md).
Saved example reports include their generation time, source revision, clean
state, tool versions, and helper SHA-256. Neither static report is a FAIR verdict.

Commands used from the skill repository:

```sh
python3 tools/validate_package.py
python3.12 -m unittest discover -s tests -v
python3 -m unittest discover -s tests -v
python3.12 skills/fair-research-software/scripts/audit_repository.py ../fair-rs-sources/awesome-sim --format markdown
python3.12 skills/fair-research-software/scripts/audit_repository.py ../fair-rs-sources/linear-elastic-plate-with-hole --format markdown
git diff --check
```

## Unperformed checks

- Live remote CI: no run was retrieved or triggered by the agent.
- Full external CFF/CodeMeta/RO-Crate schema validation.
- Native scientific solver execution or numerical result reproduction.
- Zenodo publication and Software Heritage archival submissions.
- End-to-end use in actual Claude Code and OpenCode sessions.

The included GitHub Actions workflow defines future CI checks; no successful
remote run is claimed. Re-run tests and record the exact package commit when
evaluating a later revision.
