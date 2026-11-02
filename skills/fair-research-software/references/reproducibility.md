# Reproducibility, provenance, and badges

## Execution

Identify the actual use case: importing a library, inspecting saved results,
running one example, reproducing a figure, or executing a full simulation study.
Keep these claims distinct. Read scripts before executing them and choose a
representative run within available compute and authorization.

Record OS/architecture, language/compiler, environment/lockfile, native libraries,
required hardware, input identifiers/checksums, parameters and units, seeds when
relevant, command, exit status, outputs, and validation tolerances. Use a clean
environment. Dependency ranges describe compatibility; they do not lock a run.
Preserve a resolved environment or image digest when needed for reproducibility.

Keep scientific expected results and tolerances independent of the run being
tested. Do not weaken tests or alter numerical algorithms to make a FAIR audit
pass. Report unavailable commercial solvers or native libraries as limitations.
If execution is outside scope, record exact commands and mark it not_checked.

## Badges

| Badge or check | What it can demonstrate | What it does not establish by itself |
| --- | --- | --- |
| DOI | A link to a deposit | Correct contents, a matching release, or scientific validity |
| REUSE | Licensing metadata compliance for checked files | Ownership or scientific correctness |
| CI | The linked job passed for a revision | Untested platforms, complete reproduction, or future success |
| JupyterHub/Binder launch | A route to an interactive environment | Successful execution of every notebook or solver |
| Software Heritage | A link to an archived object | Preservation of every external dependency |

Link badges to their evidence. Pin source launch links to a release/commit and
container launches to an image digest for a paper's results; moving `HEAD` or
`latest` can change. Identify the scope of a smoke test: creating a
notebook file is not executing its cells, and plotting downloaded data is not
rerunning the underlying simulation. Do not add a static green badge as evidence
for work that was never performed.

## RO-Crate and semantic metadata

Use `ro-crate-metadata.json` to describe a research object and relevant files,
people, tools, inputs, outputs, and provenance. Select an appropriate RO-Crate
profile and validate it; parseable JSON is not sufficient. Crates may reference
external resources, so explicitly distinguish bundled and referenced artifacts.
Preserve required external inputs separately where necessary.

For simulations, describe physical quantities and units, parameter sets,
configuration-to-file bindings, model/solver identity, workflow steps, and result
metrics. Prefer established community vocabularies such as metadata4ing and QUDT
when appropriate. Do not force a simulation ontology on unrelated software.

Distinguish a planned workflow description from provenance captured during an
actual run. Record whether historical provenance was reconstructed. A manifest
helps a future user understand the workflow; a runner, dependencies, and verified
execution are still needed. A research result and a software release may need
separate records, identifiers, and access conditions.

Sources: [RO-Crate](https://www.researchobject.org/ro-crate/about_ro_crate),
[repo2docker](https://repo2docker.readthedocs.io/),
[REUSE](https://reuse.software/), and the source example reference in this skill.
