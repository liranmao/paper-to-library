import copy
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('write_note', ROOT / 'skills/paper-to-library/scripts/write_note.py')
writer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(writer)


class NoteTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.vault = Path(self.tmp.name) / 'vault'
        self.data = json.loads((ROOT / 'examples/paper.json').read_text())

    def test_dry_run_has_no_side_effects(self):
        result = writer.create(self.data, self.vault, True)
        self.assertTrue(result['dry_run'])
        self.assertFalse(self.vault.exists())

    def test_rendered_note_and_provenance(self):
        p = Path(writer.create(self.data, self.vault)['path'])
        body = p.read_text()
        self.assertEqual(p.name, 'NM：Example spatial atlas study.md')
        self.assertFalse(any(line.startswith('# ') for line in body.splitlines()))
        self.assertIn('**Authors:** Example Researcher; Another Researcher', body)
        self.assertIn('**Journal IF:** Not verified', body)
        self.assertIn(self.data['zotero_uri'], body)
        self.assertIn('"doi": "10.0000/example-only"', body)

    def test_existing_note_is_not_overwritten(self):
        p = Path(writer.create(self.data, self.vault)['path'])
        p.write_text(p.read_text() + '\nMy reading notes.\n')
        before = p.read_bytes()
        with self.assertRaises(FileExistsError):
            writer.create(self.data, self.vault)
        self.assertEqual(p.read_bytes(), before)

    def test_same_item_under_renamed_nested_note(self):
        p = Path(writer.create(self.data, self.vault)['path'])
        sub = p.parent / 'archive'
        sub.mkdir()
        p.rename(sub / 'old-title.md')
        other = copy.deepcopy(self.data)
        other['title'] = 'A new title'
        with self.assertRaises(FileExistsError):
            writer.create(other, self.vault)

    def test_requires_explicit_abstract_scope(self):
        self.data['takeaway'] = 'An unsupported full-text claim.'
        with self.assertRaises(ValueError):
            writer.create(self.data, self.vault)
        self.assertFalse(self.vault.exists())

    def test_figure_copied_and_embedded_last(self):
        import base64
        image = Path(self.tmp.name) / 'figure.png'
        image.write_bytes(base64.b64decode('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+aO1sAAAAASUVORK5CYII='))
        self.data.update(image=str(image), image_source='Synthetic test pixel, not a scientific figure.')
        result = writer.create(self.data, self.vault)
        self.assertEqual(Path(result['image']).read_bytes(), image.read_bytes())
        body = Path(result['path']).read_text()
        self.assertIn('|480]]', body)
        self.assertLess(body.index('## Why it matters'), body.index('![[literature/'))

    def test_missing_figure_source_writes_nothing(self):
        image = Path(self.tmp.name) / 'figure.png'
        image.write_bytes(b'test')
        self.data['image'] = str(image)
        with self.assertRaises(ValueError):
            writer.create(self.data, self.vault)
        self.assertFalse(self.vault.exists())

    def test_invalid_uri_and_comment_delimiters(self):
        for field, value in [('zotero_uri', 'zotero://invented'), ('journal', 'Nature\n%%'), ('authors', ['Name %%'])]:
            data = copy.deepcopy(self.data)
            data[field] = value
            with self.subTest(field=field), self.assertRaises(ValueError):
                writer.create(data, self.vault)

    def test_filename_sanitization_and_journal_mapping(self):
        self.assertEqual(writer.filename('A/B: C?', 'Nature Medicine'), 'Nat Med：A-B- C-.md')
        self.assertEqual(writer.filename('Study', 'Example Journal'), 'Example Journal：Study.md')
        with self.assertRaises(ValueError):
            writer.filename('x' * 300, 'Nature')

    def test_impact_factor_requires_metric_year_and_source(self):
        self.data['impact_factor'] = {'value': '1.2'}
        with self.assertRaises(ValueError):
            writer.create(self.data, self.vault)
        self.data['impact_factor'].update(year=2025, source='https://example.org/metrics')
        p = Path(writer.create(self.data, self.vault)['path'])
        self.assertIn('1.2 (2025) · [Source](https://example.org/metrics)', p.read_text())

    def test_invalid_source_url_is_rejected(self):
        self.data['sources'] = ['/private/local/file']
        with self.assertRaises(ValueError):
            writer.create(self.data, self.vault)


if __name__ == '__main__':
    unittest.main()
