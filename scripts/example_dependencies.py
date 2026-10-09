"""Identify an example's package dependency by the repository's configured alias."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
# Tokenize just enough of an app header to ignore comments and quoted contents.
TOKENS = re.compile(r'#[^\n]*|"(?:\\.|[^"\\])*"|[A-Za-z_][A-Za-z_0-9]*|[^\s]')


def read_alias(root: Path = ROOT) -> str:
    path = root / '.package-alias'
    try:
        alias = path.read_text(encoding='utf-8').strip()
    except FileNotFoundError:
        raise ValueError(f'Missing {path}; put the example package alias in this file.') from None
    if not re.fullmatch(r'[a-z][A-Za-z_0-9]*', alias) or alias in {'roc', 'platform'}:
        raise ValueError(f'{path}: expected one package alias, such as pkg.')
    return alias


def replace_dependency(source: str, alias: str, target: str) -> str:
    tokens = [m for m in TOKENS.finditer(source) if not m[0].startswith('#')]
    if len(tokens) < 3 or tokens[0][0] != 'app' or tokens[1][0] != '[':
        raise ValueError('expected an app header')
    index = 2
    depth = 1
    while index < len(tokens) and depth:
        value = tokens[index][0]
        depth += (value == '[') - (value == ']')
        index += 1
    if index >= len(tokens) or tokens[index][0] != '{':
        raise ValueError('expected an app dependency record')
    index += 1
    depth = 1
    declarations = []
    while index < len(tokens) and depth:
        value = tokens[index][0]
        if depth == 1 and value == alias and tokens[index - 1][0] in {'{', ','}:
            if index + 2 >= len(tokens) or tokens[index + 1][0] != ':':
                raise ValueError(f'expected {alias}: "package source"')
            declarations.append(tokens[index + 2])
        depth += (value == '{') - (value == '}')
        index += 1
    if depth:
        raise ValueError('unterminated app dependency record')
    if len(declarations) != 1:
        raise ValueError(f'expected exactly one {alias}: "package source" in the app header; found {len(declarations)}')
    declaration = declarations[0]
    if re.fullmatch(r'"(?:\\.|[^"\\])*"', declaration[0]) is None or declaration[0].startswith('"""'):
        raise ValueError(f'{alias} must name a quoted package source, not a platform or expression')
    return source[:declaration.start()] + json.dumps(target, ensure_ascii=False) + source[declaration.end():]


def rewritten_examples(examples_dir: Path, alias: str, target: str) -> list[tuple[Path, str]]:
    examples = sorted(examples_dir.glob('*.roc'))
    if not examples:
        raise ValueError(f'No examples found in {examples_dir}')
    result = []
    for path in examples:
        try:
            rewritten = replace_dependency(path.read_text(encoding='utf-8'), alias, target)
        except ValueError as error:
            raise ValueError(f'{path}: {error}') from error
        result.append((path, rewritten))
    return result


def update_examples(examples_dir: Path, alias: str, target: str) -> None:
    # Validate every file before changing any of them.
    for path, source in rewritten_examples(examples_dir, alias, target):
        if source != path.read_text(encoding='utf-8'):
            path.write_text(source, encoding='utf-8')
