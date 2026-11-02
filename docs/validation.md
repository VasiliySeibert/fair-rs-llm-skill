# Initial validation record

Date: 2026-11-02. Environment: macOS arm64.

| Check | Observed result |
| --- | --- |
| Package structure, frontmatter, resources, relative links | Passed |
| Codex skill-creator quick validator | Passed with Python 3.12.3 / PyYAML 6.0.3 |
| Python 3.12.3, PyYAML 6.0.3 | All 17 unit tests passed |
| Python 3.9.6, no PyYAML | 15 tests passed; 2 YAML-dependent tests explicitly skipped |
| Installer | Project paths for all three agents and personal/XDG paths tested in temporary directories; existing installs preserved |
| Existing plate-with-hole checkout | Inspected revision 7149c0bac70d44ee5a536d486943c46a1a236565; duplicated DOI roles detected |
| Independent agent trial | Audited a synthetic heat-example project with this skill; reported conflicting versions and DOI roles, missing rights, unavailable solver, and unsupported plot claim |
| External/archive claims in trial | Correctly left unverified; no target edits or publication |

The independent trial used a fresh agent context with the skill and example files,
without the evaluator's expected conclusions. It is one behavioural trial, not a
comparison across Codex, Claude Code, OpenCode, or open-weight models.

The tests additionally confirm that the checker does not run target scripts or
Git fsmonitor hooks, skips out-of-root symlinks, reports missing YAML support
honestly, and rejects duplicate JSON/YAML metadata keys.

## Unperformed checks

- Fresh GitHub clones and live remote CI: GitHub API connectivity was unavailable.
- Full external CFF/CodeMeta/RO-Crate schema validation.
- Native scientific solver execution or numerical result reproduction.
- Zenodo publication and Software Heritage archival submissions.
- End-to-end use in actual Claude Code and OpenCode sessions.

The included GitHub Actions workflow defines future CI checks; no successful
remote run is claimed. Re-run tests and record the exact package commit when
evaluating a later revision.
