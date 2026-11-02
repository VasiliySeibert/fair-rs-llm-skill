# Semantic benchmarks and result provenance

Apply this optional workflow to simulations and multi-solver research projects.
It is derived from the inspected plate-with-hole repository; see
[source examples](source-examples.md) for the exact revision. Keep existing
scientific models, solver choices, tolerances, and rights intact.

## Identify the objects separately

| Object | Plate-with-hole example | Evidence to preserve |
| --- | --- | --- |
| Software release | CFF/CodeMeta 0.1.0 | Release tag, source commit, software DOI |
| Benchmark specification | `benchmark/1.1.0/` | Specification version, configuration file and checksum |
| Solver | FEniCS runner selects 0.9.0 | Solver name/version and actual resolved environment |
| Configuration | Generated `parameters_*.json` | Parameter values, units, mesh and other input identities |
| Execution | One supported configuration run | Commands, environment, exit status, outputs, provenance |
| Result collection | Aggregate RO-Crate | Included subcrates, identifiers, rights, checksums |

Different object versions are not automatically inconsistent. Compare metadata
only when it describes the same object. The local checker compares root software
metadata and an explicit root Python package version, not nested benchmark or
solver versions. Confirm the object scope yourself for monorepos and datasets.

## Follow the inputs to the outputs

1. Inspect the JSON-LD context and graph, not just whether JSON parses. The source
   maps benchmark concepts to vocabularies including metadata4ing, QUDT,
   MathModDB, Schema.org, and Croissant. Identify model, parameters, units,
   processing steps, file objects, and metric definitions.
2. Check bindings against actual files. For example, the benchmark connects
   `element_size` to a parameter-file extraction path `/element_size[m]`, and
   `max_von_mises_stress` to an extraction path in a summary file. Verify the
   runner's extraction convention and the generated values; do not assume every
   field called `jsonPath` uses an interchangeable syntax across tools.
3. Trace unit handling. The FEniCS runner calls `prepare_benchmark` with
   `strict_units=True` and a mapping for metre/pascal symbols. Preserve physical
   quantities and conversions explicitly; never change units just to pass a test.
4. Read the runner together with its environment template. Here it injects the
   selected DOLFINx version before invoking Snakemake. A runtime pin for one
   dependency still does not lock the complete environment.
5. Separate supported, skipped, failed, and completed configurations. The inspected
   FEniCS runner skips non-triangle cell types. A successful overall job does not
   establish that every benchmark configuration was executed.
6. Follow the Snakefile: mesh generation produces `mesh.msh`; simulation consumes
   it and the parameter file, producing `solution_metrics.json` and
   `solution_field_data.zip`. Check scientific acceptance criteria separately from
   process exit status or file existence.

Before running, inspect CPU/memory/time requirements. The source runner requests
all available cores; choose a bounded representative run appropriate to the
user's machine and authorization. Do not silently launch the full study merely
because an audit found a workflow file.

## Capture and preserve provenance

The source runner uses a Snakemake reporter to produce per-run RO-Crates, then
passes the collected subcrate paths and solver identity to an aggregate-crate
builder. Verify which files are bundled, which are external references, and
whether the provenance describes successful execution rather than a plan.

Record configuration IDs, skipped runs, source revision, exact benchmark input,
software/environment versions, outputs/checksums, and validation results. When a
workflow downloads a benchmark from RoHub, retain its fetched identifier and
bytes; a filename matching the local specification is insufficient provenance.
Validate the relevant RO-Crate profile and inspect resolved links separately
from parsing JSON. Check that result licensing fits all bundled components.

## Separate execution, viewing, and publication

- Solver workflows create results and crates. CI artifact retention is temporary
  storage, not a preservation policy.
- The notebook loads metric data from RoHub and plots it. Report this as reuse
  or reanalysis of results unless the solver computations were also rerun.
- The repo2docker workflow builds a launchable environment and checks notebook
  existence. Record an image digest, source commit, and input identifiers when
  making a reproducibility claim; `latest` is mutable.
- The RoHub orchestration workflow runs solvers and then invokes a separate
  credentialed upload workflow. Audit/prepare requests do not authorize that
  upload. For requested publication, verify the destination, production versus
  development setting, uploaded contents, resulting identifier, and retrieval.

Use project-appropriate infrastructure. RoHub and `semantic-benchmark` are the
source example's choices, not prerequisites for FAIR research software.
