# Software Heritage preservation

Zenodo deposits and Software Heritage have complementary roles. Zenodo can
preserve a release bundle with a citable record. Software Heritage preserves
source-code objects and history; SWHIDs identify content such as revisions,
directories, and snapshots. Neither replaces a tested runtime environment.

1. Record the public repository origin and target release revision.
2. Search the [archive](https://archive.softwareheritage.org/browse/search/) for
   that origin. Check whether the relevant revision is present; an old successful
   visit does not establish preservation of a later release.
3. If preservation is requested and the revision is absent, use
   [Save Code Now](https://archive.softwareheritage.org/save/) or the documented API.
   Follow the host's account/access requirements. A failed access attempt is not
   evidence that the software is unarchived.
4. Inspect request/visit completion. A queued request is **pending**, not archived.
   Do not repeatedly submit the same request because completion takes time.
5. Obtain the actual SWHID permalink for the intended object. State whether it is
   a revision (`rev`), directory (`dir`), or snapshot (`snp`), with useful origin
   and path context where appropriate. Never fabricate an identifier from an
   unverified Git hash or copy a placeholder from a slide.
6. Verify retrieval and record the origin, target revision, SWHID, date, and link.

Do not assume every public GitHub repository or new commit is already archived.
Do not claim that external datasets, binaries, container registries, or all
runtime dependencies were preserved merely because the source was archived.
Where Zenodo also offers Software Heritage integration, inspect its actual
completion and preserved object; do not assume it captured the full Git history.

Sources: [Software Heritage FAQ](https://www.softwareheritage.org/software-heritage-faq/),
[user documentation](https://docs.softwareheritage.org/user/index.html),
[research software guidance](https://www.softwareheritage.org/2019/08/05/saving-and-referencing-research-software-in-software-heritage/).
