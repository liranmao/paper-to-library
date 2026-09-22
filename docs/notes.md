# Notes and templates

The source of the note generator is `skills/paper-to-library/scripts/write_note.py`. The Integration template is `templates/concise-literature.md`; its output filename and citation suggestions live in `config/zotero-integration.example.json`.

The note title comes from the filename, e.g. `NM：Original paper title.md`. No body H1 is emitted. Metadata comes first, then a 1–2 sentence takeaway, a one-phrase explanation of relevance, and an optional source figure at width 480. `%%` comments hold persistence markers, a Zotero URI/citekey, and JSON provenance. They are hidden in Obsidian Reading view, but visible in source mode. Enable inline titles to see the filename above the note.

The Python helper requires `--vault` and refuses to overwrite an existing filename or another Markdown note containing the same Zotero URI. The agent additionally checks DOI/title for duplicates across renamed notes and Zotero entries. Existing-note regeneration is an explicit agent edit with a backup and preserved user content; there is no destructive `--force` mode.

Required JSON fields are demonstrated in `examples/paper.json`. `sources` is a nonempty list of HTTP(S) URLs. `evidence` is `full_text` or `abstract`; an abstract-only takeaway must say “Based on the abstract”. Optional `image` is a local PNG/JPEG/WebP file with `image_source` describing the original figure, page, source, and attribution. Images are copied under `literature/_images/<Zotero item key>/` with a content hash in the filename.

An optional `impact_factor` object holds `value`, `year` (metric year), and `source`. Omit it when not verified. Do not substitute CiteScore or the five-year IF. Journal IF is journal metadata, not a measure of the individual paper's quality. Keep author order and online/issue date precision as published.

Manual Zotero Integration imports use its persistence regions to retain existing content. They do not perform research or generate AI summaries. Inspect any automatically selected annotation image before treating the note as complete. Changing journal abbreviations requires updating `JOURNAL_PREFIXES` in the helper and both path/citation templates in the Integration config.

Article text, PDFs, and figures are governed by their original licenses. This repository ships only synthetic examples, not library exports or publisher figures.
