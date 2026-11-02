# Evaluation protocol

The automated tests check observable helper behaviour: metadata parsing and
conflicts, skipped dependencies, symlink boundaries, Git inventory, absence of
target execution, honest unchecked states, installation paths, and refusal to
overwrite an existing skill. These tests do not establish cross-model quality.

## Agent evaluation

Use an isolated copy of a repository. Give the agent only the skill, raw files,
and a realistic request. Keep expected outcomes in the evaluator's context.
Do not execute external publication as part of routine evaluation.

| Case | User request | Observable outcome to assess |
| --- | --- | --- |
| Minimal Python project | Audit this repository without changing it | Missing evidence reported; no invented DOI or executed tests |
| Mixed licenses | Prepare FAIR improvements, preserving rights | Third-party notices and per-file differences remain intact |
| Conflicting metadata | Check release readiness | Version/identifier inconsistencies are surfaced with evidence |
| Launchable notebook | Assess reproducibility | Saved output, file generation, and computation are distinguished |
| Offline environment | Check DOI and archival status | Unavailable remote checks remain not_checked |
| Julia/native solver | Prepare reproducibility documentation | Existing ecosystem respected; no forced Python conversion |
| Semantic benchmark | Review version identity and run provenance | Software, specification, solver, and result versions stay distinct; skipped runs and runtime pins are considered |
| Archive request pending | Verify Software Heritage preservation | Pending request is not reported as completed |

For each attempt record skill commit, source commit, dirty state, agent/application
version, model when known, tool versions, prompt, resulting changes, and command
results. Evaluate correctness, unsupported claims, preservation of existing
content, and user effort. Run the same cases on each claimed supported agent/model
before describing them as behaviourally verified.

## Initial validation scope

The package targets the common Agent Skills format and documented discovery paths.
An initial local validation record is maintained in [validation.md](validation.md). No remote
Zenodo publication, Software Heritage request, live solver execution, or complete
Codex/Claude Code/OpenCode comparison is implied by passing package checks.
