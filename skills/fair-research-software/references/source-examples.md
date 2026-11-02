# Source examples and provenance

Inspected on 2026-11-02 from the two repositories cloned with `gh` on the
maintainer's Mac. Both main working trees were clean. These are practical
examples, not normative requirements or a claim of complete FAIR4RS compliance.

## awesome-sim and slides

- [Software source](https://github.com/VasiliySeibert/awesome-sim/tree/39b1aa986ee42de7b4b37abf15a7850d43cabf5a):
  `39b1aa986ee42de7b4b37abf15a7850d43cabf5a` (2026-04-21).
- [Slide source on gh-pages](https://github.com/VasiliySeibert/awesome-sim/blob/e354ef2e567223ab8ba6eaac3d572d589efb5ab8/index.html):
  `e354ef2e567223ab8ba6eaac3d572d589efb5ab8` (2026-05-12).
  [Rendered slides](https://vasiliyseibert.github.io/awesome-sim/) may change later.
- Inspected README, `CITATION.cff`, `codemeta.json`, `pyproject.toml`,
  `.github/workflows/ci.yml`, `tests/`, `examples/`, and `CHANGELOG.md`.

The small heat-equation package connects a mathematical model and runnable
example to metadata, an MIT license, CI, and citation identifiers. Its CFF,
CodeMeta, and Python package declare software version 1.1.0. The CFF records a
concept DOI and separate release DOIs; these declarations still require checking
against the corresponding archive records when publishing or citing results.

The scientific tests check boundary values, finite outputs, nonincreasing energy,
and rejection of unstable time steps. CI defines unit tests and a small headless
example. Reading those files establishes the test design, not a successful run.
The dependency bounds in `pyproject.toml` are compatibility ranges rather than a
fully resolved environment, despite the README's use of the word "pinned".

The slides teach concept/version DOI identity, Zenodo's GitHub release webhook,
Software Heritage, qualified dependency references, and layered documentation.
Treat preservation statements as intentions until the actual archived revision
is checked. Do not copy an illustrative SWHID or promise permanent availability.

## linear-elastic-plate-with-hole

- [Software source](https://github.com/Simulation-Benchmarks/linear-elastic-plate-with-hole/tree/5a8dffb551334e693f45235c1816edc9e45743d1):
  `5a8dffb551334e693f45235c1816edc9e45743d1` (2026-10-23).
- Inspected README, CFF/CodeMeta, `REUSE.toml`, `LICENSES/`, benchmark 1.1.0
  configurations, the FEniCS runner/Snakefile/environments, solver and publishing
  workflows, `postBuild`, notebook build scripts, and `notebooks/RoCrate.ipynb`.

This example adds mixed file licensing, a semantic benchmark specification,
unit-aware parameter extraction, multiple solvers, Snakemake/Conda execution,
per-run and aggregate RO-Crate provenance, and a separate RoHub upload workflow.
Use [the benchmark workflow guide](benchmark-workflows.md) when those patterns
fit the target project; do not impose them on a small library.

Source-derived review points:

- CFF labels `10.5281/zenodo.21718397` as both concept and version DOI. Verify
  archive relations before correcting either label; never guess the other DOI.
- Repository software metadata says 0.1.0; benchmark definitions are 1.1.0;
  the FEniCS runner selects solver 0.9.0. These identify different objects.
- The JupyterHub launch badge selects a container tagged `latest`. A repeatable
  publication should record an immutable image digest and matching code/input IDs.
- The repo2docker check establishes notebook existence. The notebook fetches and
  plots RoHub results; neither alone proves the underlying simulations reran.
- FEniCS's environment template has an unpinned solver entry, but its runner
  writes the selected solver version into the runtime environment. Inspect both.
- REUSE has overlapping patterns, including `benchmark/**` and extension rules.
  Check effective annotations with REUSE tooling before describing coverage.

## Evidence limits

These observations concern the pinned source trees and slide source. No fresh
scientific execution, live CI result, private webhook configuration, completed
Software Heritage archival, or new Zenodo deposit is claimed. Service procedures
are supported by the official documentation linked in the individual guides.
