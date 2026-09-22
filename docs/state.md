# Reply processing state and recovery

Store the ledger at `state_path` and issue archives at `briefing_archive` from the private config. The agent maintains these JSON files; no Gmail daemon is included. Never commit message IDs, email bodies, archives, or your reading history.

A minimal empty ledger is:

```json
{"schema_version": 1, "last_successful_scan": null, "requests": []}
```

Each request represents **one selected paper**, not one email. Record:

| Field | Meaning |
| --- | --- |
| `request_id` | Stable local identifier for this message + selection |
| `message_id`, `thread_id` | Mail-provider IDs used to retrieve the source |
| `briefing_date`, `selection` | Original issue and user's selection text |
| `doi`, `title` | Resolved canonical identifiers, null until resolved |
| `zotero_status`, `obsidian_status` | `pending`, `complete`, or `failed` |
| `status` | `pending`, `needs_clarification`, `partial`, `complete`, or `failed` |
| `zotero_item_key`, `zotero_uri`, `note_path` | Verified results when available |
| `last_error`, `updated_at`, `completed_at` | Recovery information in UTC |
| `last_notified_state` | Signature of the last user-visible result/blocker |

Persist a request before importing. Save progress after each verified destination. Check DOI/title across the whole Zotero library, then the note by item URI/DOI/title, before each retry. Multiple messages selecting the same paper should point to the same library item and note. Record each request as satisfied after verifying those existing artifacts.

Advance `last_successful_scan` only after all mail result pages have been read and candidates either processed or durably recorded. Per-paper failures can remain pending while the scan checkpoint advances. A failed page fetch must retain the earlier checkpoint. Retry pending requests on every run even when their emails fall outside the overlap window.

Use one writer per ledger. To save: write UTF-8 JSON to a temporary file in the same directory, flush and close it, then atomically replace the ledger using `os.replace`. A corrupt/unreadable ledger requires recovery from a backup or reconciliation against mail and actual library state; never silently reset it and import everything again.

Uncertain Zotero writes and uncertain email sends must be checked against the destination before retrying. After one unsuccessful verification, leave the request pending and report uncertainty. Quiet scans may update the checkpoint without notifying the user; unchanged failures should not generate a notification every day.
