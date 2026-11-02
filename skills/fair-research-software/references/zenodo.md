# Zenodo release and DOI workflow

Use this guide for a user-requested GitHub integration, release preparation, or
deposit. A local audit does not authorize publishing a repository or creating a
record. Existing explicit publication authorization remains valid.

## Prepare

1. Establish the repository, owner, release tag, intended commit, visibility,
   metadata, and which artifacts belong in the archive. Check whether an existing
   Zenodo record already represents the project; avoid duplicate record series.
2. Validate metadata and rights before release. For GitHub ingestion, prepare
   `CITATION.cff` or `.zenodo.json` at the root of the released revision.
   **If both exist, `.zenodo.json` wins.** Check for stale copies and unsupported
   fields against current official documentation.
3. Inspect what the source archive will contain. Large data, Git LFS objects,
   submodules, external inputs, release attachments, and container images may
   require separate preservation. Verify the actual archive instead of assuming
   it contains every dependency or output.

## Enable the GitHub webhook

1. Sign in to Zenodo and connect the relevant GitHub account.
2. Open the profile menu's **GitHub** page; choose **Sync now**.
3. Find the public repository and enable its switch. Zenodo installs its release
   webhook when integration is enabled; do not invent or manually guess a receiver URL.
4. If an organisation repository is missing, check admin rights, the organisation's
   approval of the Zenodo application, and then sync again. Use an appropriate
   user handoff for account authorization that the agent cannot perform.
5. Verify the enabled repository in Zenodo. When available, GitHub repository
   Settings → Webhooks provides delivery evidence; do not expose webhook secrets.

The documented integration concerns public repositories. A private or restricted
project needs a suitable deposit/access workflow; do not make it public merely
to enable this integration.

## Release and verify

Publish a **GitHub Release** associated with the intended tag after preparation.
A pushed tag alone does not trigger the documented release-ingestion workflow.
Wait for processing and inspect status before retrying. For old releases, do not
assume enabling the switch retroactively archives them; check supported ingestion
options or arrange a deliberate manual deposit.

Verify and record:

- the release tag and exact commit;
- the Zenodo record, resource type, creator metadata, rights, and version;
- archive contents and relevant checksums;
- the release DOI and its relation to the concept DOI;
- any missing external inputs or runtime artifacts.

Use the version DOI for a computation using that release; use the concept DOI to
refer to the project across versions. Copy identifiers from service records.
Do not equate a DOI in a README with a verified deposit. A DOI identifies a record
and supports preservation/citation; it is not an execution test.

## DOI timing and recovery

With automatic GitHub ingestion, a newly minted DOI may become known only after
release. Add the verified citation to the working branch and service metadata as
appropriate; do not move the existing tag to pretend the archived bytes included
that subsequent change. A deliberate manual-deposit workflow can reserve a DOI
before finalising files, but do not mix it with automatic ingestion in a way that
creates two independent records for the same intended release.

On a timeout or failed response, inspect existing releases, records, and webhook
delivery status before retrying any write. Report an unresolved deposit as pending
or not_checked. Use Zenodo Sandbox for explicitly requested end-to-end publication
tests; sandbox identifiers are not production citations.

## Official sources

- [Enable a repository](https://help.zenodo.org/docs/github/enable-repository/)
- [GitHub permissions](https://support.zenodo.org/help/en-gb/24-github-integration/127-which-github-permissions-do-you-request-and-why)
- [Describe software](https://help.zenodo.org/docs/github/describe-software/)
- [Archive a GitHub release](https://help.zenodo.org/docs/github/archive-software/github-upload/)
- [Reserve a DOI](https://help.zenodo.org/docs/deposit/describe-records/reserve-doi/)

Service interfaces can change. Check these pages when carrying out a live task.
