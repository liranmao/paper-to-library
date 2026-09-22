---
name: paper-to-library
description: Add a paper by title, DOI, or URL to a Zotero collection and create a concise English Obsidian note with verified metadata and an optional source figure.
---

# Paper to library

Read the user-selected local configuration (default `library.local.json` in the project root). Resolve relative paths against that config's directory, expand `~`, and use its vault and Zotero collection. The included writer uses the `literature` folder; keep that setting or adapt the writer and Integration paths together. Missing local configuration requires setup; do not guess a destination. Skills alone do not provide mail, browser, filesystem, or Zotero capabilities.

## Verify and reuse

1. Resolve the supplied title/DOI against the publisher, PubMed, or Crossref. Distinguish journal versions from preprints. Ask only when there are multiple plausible matches.
2. Read accessible full text; otherwise use the abstract and begin the takeaway with “Based on the abstract”. A title alone cannot support a completed note.
3. Search the entire Zotero library by DOI and normalized title. Reuse an existing item, preserving its original collections. Add it to the configured collection. For new items, use a verified write API or Zotero's Add Item(s) by Identifier while the collection is selected. Never mutate SQLite directly.
4. Retrieve a legally available PDF through Zotero when possible. Record the real item URI and citation key; never invent keys. Verify collection membership. After an uncertain write, search again before retrying. If one check cannot establish the result, report the uncertainty instead of repeating the add.

## Write the note

Obsidian content is English even when the conversation is in another language. Preserve the original paper title. The writer prefixes filenames with the journal: Nature Methods → NM, Nature Communications → NC, Nature → Nature, Cell → Cell, Nature Medicine → Nat Med; otherwise the full journal name. Use the full-width colon `：`. Do not repeat the title as a body H1.

Include, in this order:
- Journal, online publication date and different issue date, latest verifiable journal IF with metric year and source, complete authors in published order.
- `## Key takeaway`: 1–2 precise sentences supported by the accessible paper.
- `## Why it matters`: one short phrase.
- At most one locally saved original framework/result figure, displayed at width 480. Inspect it for relevance. Omit when unavailable; do not generate a scientific replacement image.

Verify metadata and IF with publisher/Clarivate sources. Use `Not verified` when IF cannot be checked; for preprints explain in the publication field that no journal IF applies. Record source URLs, verification date, evidence scope, and figure number/page/license in hidden provenance. Do not conflate IF release year with metric year.

Before writing, search existing notes by Zotero URI, DOI, current filename, and legacy title filename. Preserve user-authored content. For requested regeneration, back up outside the literature folder and edit the existing note; never create a renamed duplicate to bypass the helper's refusal. Maintain aliases/backlinks when renaming.

Prepare the JSON shape shown in the repository's `examples/paper.json`; optional fields are `doi`, `verified_at`, `impact_factor` (`value`, `year`, `source`), and `image` plus `image_source`. Sources must be HTTP(S) URLs. The executable helper is adjacent to this skill:

```sh
python3 <skill-directory>/scripts/write_note.py --input <verified-paper.json> --vault <vault-path> --dry-run
python3 <skill-directory>/scripts/write_note.py --input <verified-paper.json> --vault <vault-path>
```

The helper writes notes only. A successful script run is not evidence of Zotero import. Preserve the `publication`, `takeaway`, `importance`, `image`, and `provenance` persistence regions and import date for Integration compatibility. The Integration template is a manual-import fallback with placeholders, not an AI summarizer.

## Verify completion

Recheck the target in the configured Zotero collection, the written English note, and its referenced image. Report each side separately and provide the note link. Disclose missing PDF or abstract-only evidence. For email-driven requests, return identifiers and separate Zotero/Obsidian status to the reply skill; only both verified sides count as complete.
