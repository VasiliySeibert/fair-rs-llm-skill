# Local FAIR practice evidence

Local static checks only; no FAIR certification, network checks, or target execution.

Revision: 5a8dffb551334e693f45235c1816edc9e45743d1

Generated: 2026-11-02T12:04:11.007425+00:00; dirty: False

Tools: {"python": "3.12.3", "pyyaml": "6.0.3", "toml_parser": "tomllib"}

| Check | Status | Evidence | Limitation / detail |
| --- | --- | --- | --- |
| Root README is present | verified | README.md | Contents and usability require review. |
| License text location is present | verified | LICENSES/CC-BY-4.0.txt, LICENSES/CC0-1.0.txt, LICENSES/MIT.txt | Presence does not establish coverage, rights, or license compatibility. |
| Root CITATION.cff convention is present | verified | CITATION.cff | A missing convention is a review candidate, not a FAIR verdict. |
| Root CodeMeta or Zenodo metadata is present | verified | codemeta.json | Other discovery mechanisms may be appropriate; assess applicability. |
| CITATION.cff syntax and mapping structure | verified | CITATION.cff | Full schema validation and factual correctness are separate checks. |
| codemeta.json syntax and mapping structure | verified | codemeta.json | Full schema validation and factual correctness are separate checks. |
| Explicit versions agree across parsed root software metadata | verified | CITATION.cff, codemeta.json | {"CITATION.cff": "0.1.0", "codemeta.json": "0.1.0"} |
| CFF DOI role annotations do not conflict | failed | CITATION.cff | Same DOI labelled concept and version: 10.5281/zenodo.21718397 |
| Environment definition locations | verified | benchmark/1.1.0/environment_mesh.yml, edelweissFE/environment_benchmark.yml, edelweissFE/environment_postProcessing.yml, edelweissFE/environment_preProcessing.yml, extendablefem/Project.toml, extendablefem/environment_benchmark.yml, fenics/environment_benchmark.yml, fenics/environment_simulation.yml, kratos/environment_benchmark.yml, kratos/environment_simulation.yml, provenance/environment_provenance.yml, requirements.txt | Candidate files only; version pinning and execution are not checked. |
| GitHub Actions definition locations | verified | .github/workflows/repo2docker.yml, .github/workflows/reuse.yml, .github/workflows/rohub-integration.yml, .github/workflows/run-benchmark-edelweissfe.yml, .github/workflows/run-benchmark-extendablefem.yml, .github/workflows/run-benchmark-fenics.yml, .github/workflows/run-benchmark-kratos.yml, .github/workflows/upload-rocrate.yml | No live CI status or scientific result has been checked. |
| REUSE annotation manifest locations | verified | REUSE.toml | Headers and sidecars may also provide coverage; run reuse lint separately. |
| Metadata complies with applicable complete schemas | not_checked |  | Requires a separate scoped validation step. |
| File licensing coverage and rights are verified | not_checked |  | Requires a separate scoped validation step. |
| Intended release is archived and DOI relations verified | not_checked |  | Requires a separate scoped validation step. |
| Intended source revision is archived with a verified SWHID | not_checked |  | Requires a separate scoped validation step. |
| Documented scientific computation reproduces its expected results | not_checked |  | Requires a separate scoped validation step. |

Helper SHA-256: `6379dceb1192c0ebbd2725011bc43fda25f812cad835624d8cf0b1f363bf591e`
