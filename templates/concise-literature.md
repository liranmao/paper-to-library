{# Filename: journal prefix + full-width colon + original paper title. Configured in the Integration output path; do not repeat it as a body heading. #}
{% persist "publication" %}
{% if not _retained or not (_retained.publication | trim) %}
**Journal:** {{publicationTitle or "Not available"}}

**Published:** {% if date %}{{date | format("YYYY-MM-DD")}} (Zotero date; verify online and issue dates){% else %}Not available{% endif %}

**Journal IF:** Not verified (add value, metric year, and source)

**Authors:** {{authors or "Not available"}}
{% endif %}
{% endpersist %}

## Key takeaway

{% persist "takeaway" %}{% if isFirstImport %}
To be added in 1–2 sentences.
{% endif %}{% endpersist %}

## Why it matters

{% persist "importance" %}{% if isFirstImport %}
To be added as one short phrase.
{% endif %}{% endpersist %}

{% persist "image" %}
{% if not _retained or not (_retained.image | trim) %}
{% set pictures = annotations | selectattr("imageRelativePath") | list %}
{% set preferred = annotations | filterby("comment", "contains", "#headline") | selectattr("imageRelativePath") | list %}
{% if preferred.length %}
![[{{preferred[0].imageRelativePath}}|480]]
{% elif pictures.length %}
![[{{pictures[0].imageRelativePath}}|480]]
{% endif %}

{% endif %}
{% endpersist %}

%% Zotero citekey: {{citekey}}; source: {{desktopURI}} %%

{% persist "provenance" %}{% endpersist %}
