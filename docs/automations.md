# Daily schedules

Create two tasks in your agent runtime. Keep the existing briefing sender if you already have one; add only the missing reply checker. Use a local execution environment for imports so the vault and Zotero are reachable. Refer to [official scheduling documentation](https://learn.chatgpt.com/docs/automations?surface=app) for current runtime requirements. A GitHub-hosted CI job does not have access to your local Zotero application.

The following are reusable task prompts. Replace `<REPOSITORY>` with the absolute checkout path. Set frequency/time/timezone in your scheduler UI; these Markdown files do not install a schedule.

## Morning briefing — daily, 08:00 in your configured timezone

> Read `<REPOSITORY>/library.local.json` and use `<REPOSITORY>/skills/daily-paper-briefing/SKILL.md`. Research the configured topics and produce today's numbered briefing. I authorize sending the daily briefing to the configured `briefing_recipient` address [replace this with the actual address when authorizing]. Verify source links and publication dates, exclude previously covered papers, and archive the exact number-to-paper mapping with delivery identifiers. Keep each item to a headline, 1–2 takeaway sentences, one short relevance phrase, and an original figure when available. Check delivery status before retrying an uncertain send.

The authorization must identify the real recipient before activation; a placeholder is not approval. The sending skill is a reusable reconstruction of the daily-paper stage; no private historical email prompt is bundled.

## Evening reply check — daily, 20:00 in your configured timezone

> Read `<REPOSITORY>/library.local.json` and use `<REPOSITORY>/skills/briefing-replies/SKILL.md`. Check my replies to the configured paper briefing once daily. Process only explicit selections in my new reply text. Resolve numbers against the exact referenced briefing. Use `<REPOSITORY>/skills/paper-to-library/SKILL.md` for imports into the configured Zotero collection and Obsidian vault. Paginate all results, use an overlapping scan window, and retry pending requests regardless of age. Persist per-paper progress atomically. Verify both destinations before marking complete. Keep mail read-only. Notify me here only for new completions, changed failures, or questions; remain quiet otherwise.

## Test before relying on the schedule

Run each task once on demand. Confirm the briefing is actually delivered and that its reply maps to the right issue. Try “save 1 and 3” against an older issue, a DOI already in the library, and a reply containing only quoted briefing text. The last case must import nothing. An ambiguous “that one” should remain pending clarification. After a partial failure, restoring access and rerunning should complete only the missing work.

Keep schedules serialized for each ledger/vault. Avoid concurrent reply checks. Runtime permissions, connector availability, and local machine availability can block unattended runs; pending state must survive those failures. Do not duplicate your existing schedules when installing this kit.
