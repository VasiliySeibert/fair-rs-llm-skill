# How the two repositories shape this skill

Inspected on 2026-11-02. Links below pin the exact source commits, rather than a
moving branch. The source repositories were read without modification. The
[manifest](source-manifest.json) records revisions; the installed package retains
its own [source summary](../skills/fair-research-software/references/source-examples.md).

| Concrete source evidence | Practice incorporated in the skill |
| --- | --- |
| awesome-sim: [README.md](https://github.com/VasiliySeibert/awesome-sim/blob/39b1aa986ee42de7b4b37abf15a7850d43cabf5a/README.md), [CITATION.cff](https://github.com/VasiliySeibert/awesome-sim/blob/39b1aa986ee42de7b4b37abf15a7850d43cabf5a/CITATION.cff), [codemeta.json](https://github.com/VasiliySeibert/awesome-sim/blob/39b1aa986ee42de7b4b37abf15a7850d43cabf5a/codemeta.json) | Make software understandable and citable; distinguish declared identifiers from verified archive records. |
| awesome-sim: [pyproject.toml](https://github.com/VasiliySeibert/awesome-sim/blob/39b1aa986ee42de7b4b37abf15a7850d43cabf5a/pyproject.toml), [tests/test_solver.py](https://github.com/VasiliySeibert/awesome-sim/blob/39b1aa986ee42de7b4b37abf15a7850d43cabf5a/tests/test_solver.py) | Compare package/citation versions; distinguish dependency ranges from a lock; document scientific sanity checks. |
| awesome-sim: [.github/workflows/ci.yml](https://github.com/VasiliySeibert/awesome-sim/blob/39b1aa986ee42de7b4b37abf15a7850d43cabf5a/.github/workflows/ci.yml) | Separate unit tests and example smoke tests from full result reproduction. |
| FAIR4RS slides: [index.html](https://github.com/VasiliySeibert/awesome-sim/blob/e354ef2e567223ab8ba6eaac3d572d589efb5ab8/index.html) | Explain DOI granularity, Zenodo’s release webhook, Software Heritage, qualified dependencies, and layered documentation. |
| plate-with-hole: [CITATION.cff](https://github.com/Simulation-Benchmarks/linear-elastic-plate-with-hole/blob/5a8dffb551334e693f45235c1816edc9e45743d1/CITATION.cff) | Detect the same DOI labelled both concept and version; resolve the discrepancy through archive relations. |
| plate-with-hole: [REUSE.toml](https://github.com/Simulation-Benchmarks/linear-elastic-plate-with-hole/blob/5a8dffb551334e693f45235c1816edc9e45743d1/REUSE.toml), [.github/workflows/reuse.yml](https://github.com/Simulation-Benchmarks/linear-elastic-plate-with-hole/blob/5a8dffb551334e693f45235c1816edc9e45743d1/.github/workflows/reuse.yml) | Preserve file-specific rights; inspect overlapping patterns; distinguish license lint from rights ownership. |
| plate-with-hole: [benchmark/1.1.0/minimal-configurations.json](https://github.com/Simulation-Benchmarks/linear-elastic-plate-with-hole/blob/5a8dffb551334e693f45235c1816edc9e45743d1/benchmark/1.1.0/minimal-configurations.json) | Annotate parameters, units, file bindings, model identity, workflow steps, and metrics with community vocabularies. |
| plate-with-hole: [fenics/run_benchmark.py](https://github.com/Simulation-Benchmarks/linear-elastic-plate-with-hole/blob/5a8dffb551334e693f45235c1816edc9e45743d1/fenics/run_benchmark.py), [fenics/Snakefile](https://github.com/Simulation-Benchmarks/linear-elastic-plate-with-hole/blob/5a8dffb551334e693f45235c1816edc9e45743d1/fenics/Snakefile) | Trace runtime solver pinning, supported/skipped configurations, mesh/simulation outputs, and run provenance. |
| plate-with-hole: [.github/workflows/run-benchmark-fenics.yml](https://github.com/Simulation-Benchmarks/linear-elastic-plate-with-hole/blob/5a8dffb551334e693f45235c1816edc9e45743d1/.github/workflows/run-benchmark-fenics.yml) | Record the exact benchmark and environment; distinguish configured checks from observed execution. |
| plate-with-hole: [README.md](https://github.com/Simulation-Benchmarks/linear-elastic-plate-with-hole/blob/5a8dffb551334e693f45235c1816edc9e45743d1/README.md), [.github/workflows/repo2docker.yml](https://github.com/Simulation-Benchmarks/linear-elastic-plate-with-hole/blob/5a8dffb551334e693f45235c1816edc9e45743d1/.github/workflows/repo2docker.yml), [notebooks/RoCrate.ipynb](https://github.com/Simulation-Benchmarks/linear-elastic-plate-with-hole/blob/5a8dffb551334e693f45235c1816edc9e45743d1/notebooks/RoCrate.ipynb) | Distinguish launching, generating a notebook, plotting archived data, and rerunning solvers; record immutable image identities. |
| plate-with-hole: [.github/workflows/rohub-integration.yml](https://github.com/Simulation-Benchmarks/linear-elastic-plate-with-hole/blob/5a8dffb551334e693f45235c1816edc9e45743d1/.github/workflows/rohub-integration.yml), [.github/workflows/upload-rocrate.yml](https://github.com/Simulation-Benchmarks/linear-elastic-plate-with-hole/blob/5a8dffb551334e693f45235c1816edc9e45743d1/.github/workflows/upload-rocrate.yml) | Separate result generation, aggregation, and authorized publication; record retrieved benchmark provenance and final archive identifiers. |

The resulting guides cover [metadata/licensing](../skills/fair-research-software/references/metadata-and-licensing.md),
[Zenodo](../skills/fair-research-software/references/zenodo.md),
[Software Heritage](../skills/fair-research-software/references/software-heritage.md),
[reproducibility](../skills/fair-research-software/references/reproducibility.md), and
[semantic benchmark workflows](../skills/fair-research-software/references/benchmark-workflows.md).

The examples are interpreted rather than copied wholesale. Their badges are not
treated as certification. Claims about automatic archiving or fully pinned
dependencies are checked against the actual evidence. Scientific algorithms and
repository-specific workflows remain in their original projects.

## Try the checker on the same evidence

With Python 3.11+ and PyYAML installed, run from this skill repository:

```sh
python3 skills/fair-research-software/scripts/audit_repository.py ../fair-rs-sources/awesome-sim --format markdown
python3 skills/fair-research-software/scripts/audit_repository.py ../fair-rs-sources/linear-elastic-plate-with-hole --format markdown
```

Adjust paths to your clones. Reports for the inspected revisions are saved in
[the awesome-sim audit](examples/awesome-sim-audit.md) and
[the plate-with-hole audit](examples/plate-with-hole-audit.md).
These are static checks; human/agent interpretation and external validation are
still required. See [validation limits](validation.md).
