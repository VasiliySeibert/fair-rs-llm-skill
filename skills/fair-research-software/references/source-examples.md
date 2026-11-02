# Source examples and provenance

Review date: 2026-11-02. These are examples, not normative requirements or claims
that all FAIR4RS principles are satisfied.

## awesome-sim and slides

- Repository: https://github.com/VasiliySeibert/awesome-sim
- Slides: https://vasiliyseibert.github.io/awesome-sim/
- Inspected evidence: a previously saved HTML slide copy, last modified locally
  on 2026-10-09. A fresh source checkout was unavailable during initial authoring.
- The slides describe a small heat-diffusion example with citation metadata,
  concept/version DOIs, CodeMeta, licensing, environments, CI, and preservation.
  These were treated as teaching examples, not independently verified live status.

Useful lessons: connect each FAIR practice to a concrete artifact; distinguish
project and release identity; give a researcher a small executable example.
Do not reproduce absolute promises of permanent availability, infer automated
metadata harvesting by every service, or treat RO-Crate as an execution engine.

## linear-elastic-plate-with-hole

- Repository: https://github.com/Simulation-Benchmarks/linear-elastic-plate-with-hole
- Inspected source revision: `7149c0bac70d44ee5a536d486943c46a1a236565`
  (2026-09-23), from an existing clean local checkout.
- Verified public release record: https://zenodo.org/records/21718397 (`v0.1.0`).
  The record is separate evidence from the later inspected source revision.
- Inspected files: README, `CITATION.cff`, `codemeta.json`, `REUSE.toml`,
  `LICENSES/`, solver workflows, repo2docker and REUSE CI definitions, `postBuild`,
  the notebook build guide, and semantic benchmark configuration.

Useful patterns: file-level licensing, Snakemake/Conda execution, a JupyterHub
entry point, JSON-LD parameter descriptions with units and file bindings, and
RO-Crate provenance generated through `semantic-benchmark`.

Examples of checks the skill should make:

- The inspected CFF labels the same DOI as both concept and version; retrieve
  archive relations before accepting that distinction.
- The launch badge uses `HEAD`; a publication's execution should identify a
  specific release or commit.
- The inspected repo2docker CI checks notebook existence, not successful execution
  of every cell. Solver workflows must be evaluated separately.
- The notebook requirements include version ranges/unpinned packages; presence of
  an environment file is not evidence of a fully locked environment.

## Acquisition limitation

Fresh `gh repo clone` attempts for both repositories failed because the execution
environment could not reach `api.github.com`. No fresh clone, private webhook
configuration, live CI result, or new simulation execution is claimed here.
Revisit the examples at their current revisions before extending their factual
descriptions. The skill's service procedures were checked against official
documentation linked in the individual references.
