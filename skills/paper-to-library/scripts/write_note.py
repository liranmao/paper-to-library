#!/usr/bin/env python3
"""Create a concise, persist-compatible note from agent-verified paper data."""
import argparse
import datetime
import hashlib
import json
import re
import shutil
from pathlib import Path


JOURNAL_PREFIXES = {'Nature Methods': 'NM', 'Nature Communications': 'NC', 'Cell': 'Cell', 'Nature': 'Nature', 'Nature Medicine': 'Nat Med'}

def filename(title, journal):
    name = re.sub(r'[\\/:*?"<>|#\[\]\r\n]', '-', title).strip()
    prefix = JOURNAL_PREFIXES.get(journal, journal)
    prefix = re.sub(r'[\\/:*?"<>|#\[\]\r\n]', '-', prefix).strip()
    if not prefix:
        raise ValueError('Journal required for note title')
    if name in ('', '.', '..'):
        raise ValueError('Invalid title')
    name = prefix + '：' + name
    if len((name + '.md').encode()) > 250:
        raise ValueError('Title exceeds filename byte limit; shorten filename deliberately, retain full title in provenance')
    return name + '.md'

def publication_block(data):
    for key in ('journal', 'published'):
        if not isinstance(data.get(key), str) or not data[key].strip():
            raise ValueError('Missing verified publication field: ' + key)
    authors = data.get('authors')
    if not isinstance(authors, list) or not authors or any(not isinstance(a, str) or not a.strip() for a in authors):
        raise ValueError('Full author list in publication order required')
    if any('%%' in a or '\n' in a or '\r' in a for a in authors):
        raise ValueError('Authors must be single-line names without comment delimiters')
    impact = data.get('impact_factor')
    impact_text = 'Not verified'
    if impact is not None:
        if not isinstance(impact, dict) or any(not str(impact.get(k, '')).strip() for k in ('value', 'year', 'source')):
            raise ValueError('Impact factor requires value, metric year, and source URL')
        impact_text = f"{impact['value']} ({impact['year']}) · [Source]({impact['source']})"
    return ("%% begin publication %%\n"
            f"**Journal:** {data['journal']}\n\n"
            f"**Published:** {data['published']}\n\n"
            f"**Journal IF:** {impact_text}\n\n"
            f"**Authors:** {'; '.join(authors)}\n"
            "%% end publication %%\n\n")

def create(data, vault, dry_run=False):
    for key in ('title', 'takeaway', 'importance', 'zotero_uri', 'citekey', 'evidence'):
        if not isinstance(data.get(key), str) or not data[key].strip():
            raise ValueError('Missing ' + key)
    if data['evidence'] not in ('full_text', 'abstract'):
        raise ValueError('Evidence must be full_text or abstract')
    if not isinstance(data.get('sources'), list) or not data['sources'] or any(not isinstance(u, str) or not u.startswith(('https://', 'http://')) for u in data['sources']):
        raise ValueError('Verified source URLs required')
    if not re.fullmatch(r'zotero://select/(?:library|groups/\d+)/items/[A-Z0-9]{8}', data['zotero_uri']):
        raise ValueError('Verified Zotero item URI required')
    for key in ('title','takeaway','importance','journal','published','citekey'):
        if not isinstance(data.get(key), str) or '\n' in data[key] or '\r' in data[key] or '%%' in data[key]:
            raise ValueError('Use one paragraph without comment delimiters: ' + key)
    if data['evidence'] == 'abstract' and 'based on the abstract' not in data['takeaway'].lower():
        raise ValueError('Abstract-only takeaway must say Based on the abstract')
    publication = publication_block(data)
    folder = vault / 'literature'
    target = folder / filename(data['title'], data['journal'])
    for note in folder.rglob('*.md'):
        if note == target or data['zotero_uri'] in note.read_text(encoding='utf-8'):
            raise FileExistsError('Existing note; inspect and update without overwriting: ' + str(note))
    picture = ''
    image_dest = None
    if data.get('image'):
        source = Path(data['image']).resolve()
        if not source.is_file() or source.suffix.lower() not in ('.png','.jpg','.jpeg','.webp'):
            raise ValueError('Image must be a local PNG/JPEG/WebP file')
        if not data.get('image_source'):
            raise ValueError('Figure source required')
        digest = hashlib.sha256(source.read_bytes()).hexdigest()[:12]
        image_dest = folder / '_images' / data['zotero_uri'].split('/')[-1] / ('figure-' + digest + source.suffix.lower())
        picture = '![[%s|480]]\n' % image_dest.relative_to(vault).as_posix()
    provenance = json.dumps({k:data[k] for k in ('title','doi','sources','evidence','image_source','verified_at') if k in data},ensure_ascii=False).replace('%%', '% %')
    now = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='milliseconds')
    body = (publication + f"## Key takeaway\n\n%% begin takeaway %%\n{data['takeaway']}\n%% end takeaway %%\n\n"
            f"## Why it matters\n\n%% begin importance %%\n{data['importance']}\n%% end importance %%\n\n"
            f"%% begin image %%\n{picture}%% end image %%\n\n"
            f"%% Zotero citekey: {data['citekey']}; source: {data['zotero_uri']} %%\n"
            f"%% begin provenance %%\n%% {provenance} %%\n%% end provenance %%\n\n"
            f"%% Import Date: {now} %%\n")
    if not dry_run:
        folder.mkdir(parents=True,exist_ok=True)
        if image_dest:
            image_dest.parent.mkdir(parents=True,exist_ok=True)
            if not image_dest.exists(): shutil.copy2(source,image_dest)
        with target.open('x',encoding='utf-8') as f: f.write(body)
    return {'path':str(target),'image':str(image_dest) if image_dest else None,'dry_run':dry_run}

if __name__ == '__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--input',type=Path,required=True)
    p.add_argument('--vault',type=Path,required=True)
    p.add_argument('--dry-run',action='store_true')
    args=p.parse_args()
    print(json.dumps(create(json.loads(args.input.read_text(encoding='utf-8')),args.vault.resolve(),args.dry_run),ensure_ascii=False))
