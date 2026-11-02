# Metadata and licensing

## Citation and discovery

- Put a software `CITATION.cff` at the repository root. Use known author names,
  ORCIDs, release/version information, repository URL, and citation guidance.
  Validate against the [CFF schema](https://citation-file-format.github.io/).
  YAML parsing alone is not schema validation.
- Use `codemeta.json` when useful to discovery systems, with a suitable JSON-LD
  context and software type. Consult [CodeMeta](https://codemeta.github.io/).
  Valid JSON alone does not establish valid or meaningful JSON-LD.
- Keep titles, versions, release dates, creator roles, license scope, repository
  URLs, and identifiers consistent across CFF, CodeMeta, package metadata, and
  release records. Differences may be intentional (e.g. upload date versus release
  date, or contributor versus author); report and resolve rather than overwrite.
- Use ORCID for people, ROR for organisations, and SPDX identifiers for licenses
  when verified. Do not infer an ORCID from a name or invent an affiliation.
- Keep the software's own identifier distinct from a related article's DOI and
  from the concept DOI for all versions. Retrieve relations from the archive;
  never guess adjacent DOI numbers.
- Zenodo's GitHub integration consumes `.zenodo.json` ahead of `CITATION.cff`
  when both exist. It does not follow that any `codemeta.json` will be harvested
  by every service. Verify the resulting metadata at the destination.

Templates: `../assets/CITATION.cff.template` and
`../assets/codemeta.json.template`. Use only known facts; remove optional unknown
fields and resolve all `REPLACE_...` values before release. A DOI is optional
before one exists; do not insert a fictional value to satisfy a template.

## Rights and per-file annotations

Inventory code, docs, data, images, generated material, and third-party sources.
Preserve existing rights and attribution. A researcher may not own all included
material. A license choice requires a legitimate project decision, not inference
from file extension. Describe mixed licensing accurately in the README/metadata.

[REUSE](https://reuse.software/spec/) associates copyright and SPDX license
information with files, using headers, `REUSE.toml`, or sidecar license files as
appropriate. Put the applicable license texts in `LICENSES/` for REUSE projects.
An illustrative Python header, only after the facts are established:

```python
# SPDX-FileCopyrightText: REPLACE_YEAR REPLACE_RIGHTSHOLDER
# SPDX-License-Identifier: REPLACE_SPDX_LICENSE
```

Prefer headers where they travel naturally with reused source. Use sidecars or
`REUSE.toml` for formats that do not support comments. Scope glob patterns
carefully; a broad annotation must not silently replace a third party's rights.
Check overlapping patterns and existing annotations.

Run `reuse lint` with a recorded tool version when REUSE is chosen. A passing
result checks the specification's requirements, not legal ownership. Use the
project's actual license policy; MIT for code, CC-BY for docs, and CC0 for data
are examples from a source repository, not a universal prescription.

Sources: [Zenodo metadata precedence](https://help.zenodo.org/docs/github/describe-software/),
[CFF](https://citation-file-format.github.io/), [CodeMeta](https://codemeta.github.io/),
[REUSE](https://reuse.software/spec/), [SPDX license identifiers](https://spdx.org/licenses/).
