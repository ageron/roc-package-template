import tempfile
import unittest
from pathlib import Path

from example_dependencies import read_alias, replace_dependency, update_examples


class ExampleDependenciesTests(unittest.TestCase):
    def test_local_old_and_placeholder_sources(self):
        for old in ['../package/main.roc', 'https://example.com/v1/old.tar.zst', 'PLACEHOLDER']:
            source = f'app [] {{ lib: "{old}", other: "keep" }}\nimport lib.Example\n'
            self.assertEqual(replace_dependency(source, 'lib', 'new.tar.zst'),
                             'app [] { lib: "new.tar.zst", other: "keep" }\nimport lib.Example\n')

    def test_only_header_dependency_changes(self):
        source = '''# app [] { pkg: "comment" }
app [main!] {
    pf: platform "platform.tar.zst",
    other: "{ pkg: fake }",
    # pkg: "also a comment",
    pkg: # a comment between the label and value
        "old.tar.zst",
}
record = { pkg: "body stays" }
text = "old.tar.zst"
'''
        expected = source.replace('        "old.tar.zst",', '        "new.tar.zst",')
        self.assertEqual(replace_dependency(source, 'pkg', 'new.tar.zst'), expected)

    def test_bad_headers_fail(self):
        for source in ['app [] {}\nx = { pkg: "body" }',
                       'app [] { pkg: "one", pkg: "two" }',
                       'app [] { pkg: platform "host" }',
                       'app [] { pkg: "unclosed"',
                       'app [] { pkg: "unterminated }',
                       'package [Example] {}']:
            with self.subTest(source=source), self.assertRaises(ValueError):
                replace_dependency(source, 'pkg', 'new')

    def test_alias_configuration(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            with self.assertRaises(ValueError):
                read_alias(root)
            path = root / '.package-alias'
            path.write_text('my_pkg\n')
            self.assertEqual(read_alias(root), 'my_pkg')
            for invalid in ['', 'pkg other', 'pkg\nother', 'roc', 'platform', 'Bad', 'p.*']:
                path.write_text(invalid)
                with self.subTest(alias=invalid), self.assertRaises(ValueError):
                    read_alias(root)

    def test_no_partial_updates_and_repeat_is_safe(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            good = root / 'a.roc'
            bad = root / 'b.roc'
            original = 'app [] { pkg: "old" }'
            good.write_text(original)
            bad.write_text('app [] {}')
            with self.assertRaisesRegex(ValueError, 'b.roc'):
                update_examples(root, 'pkg', 'new')
            self.assertEqual(good.read_text(), original)
            bad.write_text(original)
            update_examples(root, 'pkg', 'new')
            update_examples(root, 'pkg', 'new')
            self.assertEqual(good.read_text(), 'app [] { pkg: "new" }')

    def test_no_examples_fails(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaisesRegex(ValueError, 'No examples'):
                update_examples(Path(directory), 'pkg', 'new')


if __name__ == '__main__':
    unittest.main()
