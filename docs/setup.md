# Setup

## Runtime and accounts

Use a local agent runtime that can read skills, browse primary sources, access an authenticated email connector, and operate Zotero through its UI or a verified API. The original workflow used Codex on macOS, Gmail, Zotero, Better BibTeX, and Obsidian. Python 3.10+ runs the note helper without third-party packages. PDF figure extraction can use Poppler (`pdftotext` / `pdftoppm`) or another available PDF tool.

Connect email through your runtime's supported account flow. The briefing sender needs sending permission; the reply checker needs read access. Do not put credentials in this repository. Configuring an email address does not authorize sending; explicitly authorize the daily recipient when enabling that task.

## Local settings

Copy `config/library.example.json` to `library.local.json`. Replace both example email addresses and the absolute vault path. Set `briefing_sender` to the account that actually sends the digest; it can differ from `owner_email`. `briefing_recipient` is the authorized destination. Relative state/archive paths are resolved from the local config's directory. `literature` is currently the supported note folder; change code and Integration templates together if you customize it.

The example uses an 08:00 briefing and 20:00 reply check in America/New_York. These are suggested schedule values, not installed tasks. Times, topics, and the maximum of five papers can be changed. Neither copying the config nor installing skills schedules anything.

## Skills

Invoke `skills/<name>/SKILL.md` directly by path from your project, or install the three folders using your runtime's skill installer. Current Codex documentation describes repository skill discovery under `.agents/skills`; one project-local option is:

```sh
mkdir -p .agents/skills
ln -s ../../skills/paper-to-library .agents/skills/paper-to-library
ln -s ../../skills/daily-paper-briefing .agents/skills/daily-paper-briefing
ln -s ../../skills/briefing-replies .agents/skills/briefing-replies
```

Run these from the repository root. If a link already exists, inspect it instead of replacing it blindly. Keep this repository available: the skills refer to its config, examples, and state documentation. For installation outside the repository, include its absolute path in the invocation or scheduled prompt. Skill installation does not install connectors or grant filesystem access. See [official skill documentation](https://learn.chatgpt.com/docs/build-skills).

## Zotero and Obsidian

Create the configured `papers` collection in Zotero. Install [Better BibTeX](https://retorque.re/zotero-better-bibtex/) for stable citation keys and keep Zotero available while importing. A verified Zotero API adapter may replace UI operations if your runtime provides one; this repository does not supply that adapter.

The note helper writes Markdown directly, so [Zotero Integration](https://github.com/community-archive/obsidian-zotero-integration) is optional for agent imports. Install it in Obsidian if you also want manual imports and citation suggestions. Copy `templates/concise-literature.md` into `<vault>/literature/_templates/concise-literature.md`.

In Integration settings, add an import format using the fields in `config/zotero-integration.example.json`. Merge those settings into your existing configuration; do not replace an existing plugin data file wholesale. Keep the configured template path and journal-prefix mapping aligned. The command is **Import concise literature note** (usually surfaced under the plugin's command prefix).

Use Obsidian Reading view and enable inline titles. The generated filename supplies the title; comment markers remain visible in source editing mode. The agent creates English summaries; a manual plugin import alone leaves summary/IF placeholders.

## First end-to-end check

Ask the agent to import one real DOI. Verify the target collection, PDF if available, English note, source image, and Zotero URI. Then ask it to preview a briefing, authorize sending to your own address, reply “save item 1”, and run the reply skill once manually. Run it a second time and verify it creates no duplicates. Enable the daily tasks only after this local check. The public test suite validates the note helper, not live Gmail or desktop operations.
