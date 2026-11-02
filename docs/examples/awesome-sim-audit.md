# Local FAIR practice evidence

Local static checks only; no FAIR certification, network checks, or target execution.

Revision: 39b1aa986ee42de7b4b37abf15a7850d43cabf5a

Generated: 2026-11-02T12:04:10.959116+00:00; dirty: False

Tools: {"python": "3.12.3", "pyyaml": "6.0.3", "toml_parser": "tomllib"}

| Check | Status | Evidence | Limitation / detail |
| --- | --- | --- | --- |
| Root README is present | verified | README.md | Contents and usability require review. |
| License text location is present | verified | LICENSE | Presence does not establish coverage, rights, or license compatibility. |
| Root CITATION.cff convention is present | verified | CITATION.cff | A missing convention is a review candidate, not a FAIR verdict. |
| Root CodeMeta or Zenodo metadata is present | verified | codemeta.json | Other discovery mechanisms may be appropriate; assess applicability. |
| CITATION.cff syntax and mapping structure | verified | CITATION.cff | Full schema validation and factual correctness are separate checks. |
| codemeta.json syntax and mapping structure | verified | codemeta.json | Full schema validation and factual correctness are separate checks. |
| Python package metadata syntax and project structure | verified | pyproject.toml | Full packaging schema and dependency resolution are separate checks. |
| Explicit versions agree across parsed root software metadata | verified | CITATION.cff, codemeta.json, pyproject.toml | {"CITATION.cff": "1.1.0", "codemeta.json": "1.1.0", "pyproject.toml": "1.1.0"} |
| CFF DOI role annotations do not conflict | not_checked | CITATION.cff | No explicit duplicate-role conflict detected; archive relations are not checked. |
| Environment definition locations | verified | pyproject.toml | Candidate files only; version pinning and execution are not checked. |
| GitHub Actions definition locations | verified | .github/workflows/ci.yml | No live CI status or scientific result has been checked. |
| REUSE annotation manifest locations | not_checked |  | Headers and sidecars may also provide coverage; run reuse lint separately. |
| Metadata complies with applicable complete schemas | not_checked |  | Requires a separate scoped validation step. |
| File licensing coverage and rights are verified | not_checked |  | Requires a separate scoped validation step. |
| Intended release is archived and DOI relations verified | not_checked |  | Requires a separate scoped validation step. |
| Intended source revision is archived with a verified SWHID | not_checked |  | Requires a separate scoped validation step. |
| Documented scientific computation reproduces its expected results | not_checked |  | Requires a separate scoped validation step. |

Helper SHA-256: `6379dceb1192c0ebbd2725011bc43fda25f812cad835624d8cf0b1f363bf591e`
