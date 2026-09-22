# Troubleshooting

| Symptom | What to check |
| --- | --- |
| `%% begin takeaway %%` is visible | Switch Obsidian to Reading view; these are persistence comments. |
| The title appears twice | Remove a legacy body H1; keep the inline filename title. |
| Manual import has empty summary | Integration imports metadata/annotations; invoke the paper-to-library skill for synthesis. |
| The import command is missing | Install/enable Zotero Integration and add the example import format. |
| The helper refuses an existing note | Inspect and update that note; do not rename a new duplicate to bypass the check. |
| A paper exists outside `papers` | Add its existing Zotero item to that collection, preserving other collections. |
| Scheduled task cannot access the vault | Run in the local environment with filesystem access and Zotero available. |
| A reply selects the wrong item number | Inspect its reply headers and original dated email, not the newest briefing. |
| A quoted digest imports everything | Stop processing; extract only newly authored explicit selections. |
| A note exists but the ledger says pending | Verify its URI and collection membership, then reconcile the ledger. |
| No figure or PDF is available | Omit the figure; report missing PDF and label abstract-only evidence. |
| The skill is not discovered | Invoke its absolute path or check your runtime's documented skill directories. |

Do not open local Zotero ports to the public internet or edit its database to work around an unavailable connector. A skill file does not grant access to a user's desktop. Keep credentials in the account connector, not in note payloads or repository files.
