---
name: daily-paper-briefing
description: Research and prepare a numbered daily paper briefing for configured topics, and email it only when the user has authorized that recipient and schedule.
---

# Daily paper briefing

Read `library.local.json` (or the user-selected config) and resolve paths relative to it. Use the configured topics, timezone, paper limit, subject, recipient, and local briefing archive. This skill needs web research and an authenticated email tool; it does not create a scheduler itself.

Search authoritative publisher, PubMed, and preprint sources for recent relevant papers. Prefer work newly published or newly discovered since the previous digest; verify online dates and distinguish preprints. Check archived DOI/title identifiers to avoid repeating papers. When there are too few relevant papers, send fewer; never fill the quota with invented or unrelated results. Clearly label older newly discovered work and preprints.

Read enough of each paper to support its takeaway. Each item gets a stable number for this issue, exact title, journal/date, DOI or publisher link, 1–2 takeaway sentences, and one short relevance phrase. Include one relevant source figure when available and the mail tool supports it, with attribution and source link. Do not generate substitute scientific figures. Label abstract-only evidence. Keep each item concise.

Use subject `<briefing_subject> — YYYY-MM-DD` in the configured timezone. Include “Reply with item numbers, titles, or DOIs to save papers to Zotero and Obsidian.” Preserve the mapping from numbers to canonical papers in a local JSON archive: date, timezone, subject, numbered items (title, DOI, URL), and send status. After confirmed delivery, add message/thread identifiers and the RFC Message-ID when available.

Send only when the user explicitly authorized this recipient and daily sending. Otherwise prepare the email for review. After a send timeout, check Sent mail before retrying; an unresolved outcome requires clarification, not a second send. Never mark a draft as delivered. If no suitable papers are found, record the empty search and follow the user's empty-day preference; default to a quiet day.

No paper enters the library merely because it appeared in the briefing. User selections are handled by `briefing-replies`; manual imports by `paper-to-library`. Keep archives and email identifiers local, outside version control.
