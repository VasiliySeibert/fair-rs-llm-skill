# FAIR-RS LLM Skill

A portable Agent Skill for making research software easier to find, access,
understand, cite, preserve, and reuse. It guides an AI coding agent through
FAIR4RS audits and improvements, with templates and a read-only local checker.

The skill supports Codex, Claude Code, and OpenCode through the open
[Agent Skills format](https://agentskills.io/specification). It is an instruction
package, not a trained model. The same files can be used with an open-weight model
in a compatible agent; results still depend on model capability, tools, and access.

## What it does

| Mode | Ask for | Expected result |
| --- | --- | --- |
| Audit | Review a repository | Findings linked to files, commands, and records; no target edits |
| Prepare | Implement FAIR improvements | Reviewable metadata, licensing, documentation, or workflow changes and validation |
| Publish | Publish a specified release or archive | Authorized service actions followed by verification of the actual record |

Topics include `CITATION.cff`, CodeMeta, Zenodo DOIs and GitHub webhooks, Software
Heritage and SWHIDs, REUSE/SPDX file licensing, environments, tests, runnable
notebooks, RO-Crate, and scientific provenance. It distinguishes evidence of
execution from badges or saved notebook outputs. It does not certify FAIRness.

## Get the package

Clone this repository, or download its source archive and extract it. When using
a clone, select a reviewed release or commit for repeatable installation. Run the
commands below from the directory containing this README. Python 3.9+ is needed
for the included scripts; the instructions themselves do not require Python.

The repository name is `fair-rs-llm-skill`; the installed skill name is
`fair-research-software`.

## Install for your agent

Use the installer for **one** agent. It copies the complete skill directory and
refuses to replace an existing installation. It does not download dependencies,
change agent permissions, log into services, or install other software.

```sh
# Choose one:
python3 tools/install_skill.py --agent codex
python3 tools/install_skill.py --agent claude
python3 tools/install_skill.py --agent opencode
```

| Agent | Personal installation | Project installation |
| --- | --- | --- |
| Codex CLI / IDE | `~/.agents/skills/fair-research-software/` | `.agents/skills/fair-research-software/` |
| Claude Code | `~/.claude/skills/fair-research-software/` | `.claude/skills/fair-research-software/` |
| OpenCode | `~/.config/opencode/skills/fair-research-software/` | `.opencode/skills/fair-research-software/` |

For a project-local installation that can be committed with the project:

```sh
python3 tools/install_skill.py --agent codex --project /absolute/path/to/research-repo
```

Replace `codex` with `claude` or `opencode` as appropriate. OpenCode also recognises
the Codex-compatible `.agents/skills` and Claude-compatible `.claude/skills`
locations. Avoid installing duplicate copies into several discovery locations.
You can instead manually copy `skills/fair-research-software/` into the appropriate
directory. Copy its supporting resources too, not just `SKILL.md`.

For an update, review changes in the source repository, remove or move aside the
previous installed directory yourself, and install again. A copied installation
does not update when the source clone changes. To uninstall, remove only the
installed `fair-research-software` directory.

These instructions target local coding agents. ChatGPT/Claude web and managed
cloud sessions have separate skill or plugin installation mechanisms; copying
files on your laptop does not install them in a remote session.

## Use it

Open your research repository in the agent, then invoke the installed skill:

**Codex CLI / IDE** — select it through `/skills` or enter:

```text
$fair-research-software Audit this repository. Report verified practices,
gaps, and checks you could not perform. Do not edit files.
```

**Claude Code:**

```text
/fair-research-software Audit this repository and prioritise the changes
needed before publishing a citable research software release.
```

**OpenCode:**

```text
Use the fair-research-software skill to audit this repository.
```

Then request the work you want, for example:

```text
Prepare the metadata and documentation improvements from the audit.
Preserve our existing licensing choices. Validate the changes locally.
```

```text
Help connect this public repository to Zenodo. Explain the account steps,
prepare release metadata, and verify the resulting archive after release.
```

```text
Check whether the exact release revision is archived in Software Heritage.
Report the SWHID if verified; otherwise tell me what remains to be done.
```

The agent can read the skill when its description matches a task, but explicit
invocation is useful when first trying it. If it is not listed, verify the
installation path and refresh the agent's skill discovery according to its docs.
Without native skill support, ask an agent with file access to read `SKILL.md`
and its relevant references; automatic discovery is then unavailable.

## Run the local checker without an LLM

```sh
python3 skills/fair-research-software/scripts/audit_repository.py /path/to/repo
python3 skills/fair-research-software/scripts/audit_repository.py /path/to/repo --format markdown
python3 skills/fair-research-software/scripts/audit_repository.py /path/to/repo --strict
```

The checker reads local files and Git state, emits a report to stdout, and never
executes the target's code. It checks metadata presence, JSON structure, selected
cross-file consistency, and evidence locations. Full schema validation, license
coverage, remote identifier resolution, and scientific execution remain separate
checks. Repository examples and templates are not accepted as root metadata.

PyYAML enables CFF syntax and cross-file checks. Install the development dependencies
in an isolated environment if needed:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
.venv/bin/python skills/fair-research-software/scripts/audit_repository.py /path/to/repo
```

No PyYAML means CFF parsing is reported as `not_checked`. Exit status is 0 for a
completed report, 1 for local failures with `--strict`, and 2 for an invocation or
repository-read error. Exit 0 does not mean FAIR compliance or completed remote
checks. Reports can contain repository paths and metadata: review them before sharing.

## How the package is organised

| Path | Purpose |
| --- | --- |
| `skills/fair-research-software/SKILL.md` | Portable agent instructions |
| `skills/fair-research-software/references/` | Focused FAIR and service guidance |
| `skills/fair-research-software/assets/` | Templates; replace marked placeholders before use |
| `skills/fair-research-software/scripts/` | Read-only audit helper |
| `tools/install_skill.py` | Agent-specific local installer |
| `tools/validate_package.py` | Package structure and link validation |
| `tests/` | Checker and installer regression tests |
| `docs/evaluation.md` | Behavioural evaluation cases and limitations |

## Development and validation

```sh
python3 tools/validate_package.py
python3 -m unittest discover -s tests -v
```

The CI workflow is configured to run these checks with and without PyYAML. See the
[initial validation record](docs/validation.md) for checks actually performed.
Evaluate actual agent behaviour on representative repositories as described in
[the evaluation protocol](docs/evaluation.md); automated
package checks alone do not establish equivalent behaviour across agents/models.

## Sources and scope

This workflow is informed by
[awesome-sim](https://github.com/VasiliySeibert/awesome-sim), its
[FAIR4RS slides](https://vasiliyseibert.github.io/awesome-sim/), and
[linear-elastic-plate-with-hole](https://github.com/Simulation-Benchmarks/linear-elastic-plate-with-hole).
See [source provenance](skills/fair-research-software/references/source-examples.md)
for what was actually inspected and which claims remain unverified.

Official references: [FAIR4RS](https://doi.org/10.15497/RDA00068),
[Agent Skills](https://agentskills.io/specification),
[Codex skills](https://developers.openai.com/codex/skills/),
[Claude Code skills](https://code.claude.com/docs/en/skills), and
[OpenCode skills](https://opencode.ai/docs/skills/).

License: [MIT](LICENSE). Existing research repositories retain their own licenses;
installing this skill does not relicense their content. No DOI or archival status
is claimed for this skill until an actual release has been deposited and verified.
