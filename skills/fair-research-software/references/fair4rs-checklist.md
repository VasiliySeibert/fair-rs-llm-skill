# FAIR4RS practices and evidence

Use [FAIR4RS v1.0](https://doi.org/10.15497/RDA00068) as the normative source.
The following is an implementation aid, not an official certification scheme.
Record applicability; none of these particular hosting services is mandatory.

| Area | Practical questions | Useful evidence |
| --- | --- | --- |
| Findable | Does the project have an identifier? Are distinct releases identified? Is accurate metadata indexed and linked to the software? | Version DOI, concept identifier, citation file, searchable archive or registry |
| Accessible | Can people retrieve software/metadata through documented protocols and access conditions? Can metadata survive loss of the original host? | HTTPS retrieval, documented authentication where needed, archival records |
| Interoperable | Are inputs/outputs represented in community formats? Are dependencies and related objects referenced meaningfully? | Format/schema docs, units, qualified identifiers, tested interfaces |
| Reusable | Are purpose, limitations, license, authorship, and provenance clear? Can the relevant community understand and use the software? | README, file rights, examples, scientific documentation, provenance and community standards |

Distinguish these evidence levels:

1. A file or badge exists.
2. A parser accepts it and required schema fields validate.
3. Its metadata matches the actual project, release, rights, and authors.
4. Referenced objects resolve and the intended execution succeeds.

Do not use success at one level as proof of later levels. FAIR does not necessarily
mean unrestricted access; clearly documented authentication/access conditions can
be appropriate. FAIR also does not establish scientific correctness or guarantee
future executability. Supplement FAIR practices with reproducibility checks.

Choose a proportionate improvement path: first fix misleading metadata or missing
rights, then make the documented use case work, then prepare identified and
preserved releases. For a simulation benchmark, include parameter meaning, units,
reference solutions, validation tolerances, and execution provenance. For other
software, use its community's relevant standards instead of imposing simulation
ontologies or RO-Crate everywhere.
