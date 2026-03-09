from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / 'versions.json'
VERSION_PATTERN = re.compile(r'^(\d+)\.(\d+)\.(\d+)$')
EXCLUDED_FILES = {'README.md', 'index.html', 'versions.json', '.nojekyll'}
EXCLUDED_DIRS = {'.git', '.github', 'scripts'}


def parse_version(filename: str) -> tuple[int, int, int] | None:
    match = VERSION_PATTERN.match(filename)

    if not match:
        return None

    return tuple(int(part) for part in match.groups())


def build_entry(file_path: Path) -> dict:
    filename = file_path.name
    version = parse_version(filename)

    return {
        'name': filename,
        'path': filename,
        'isVersion': version is not None,
        'version': list(version) if version is not None else None,
    }


def sort_key(entry: dict) -> tuple:
    version = entry['version']

    if version is not None:
        major, minor, patch = version
        return (0, -major, -minor, -patch, entry['name'])

    return (1, 0, 0, 0, entry['name'].lower())


def main() -> None:
    files = []

    for item in ROOT.iterdir():
        if item.is_dir() and item.name in EXCLUDED_DIRS:
            continue

        if item.is_file() and item.name in EXCLUDED_FILES:
            continue

        if item.is_file() and not item.name.startswith('.'):
            files.append(build_entry(item))

    files.sort(key=sort_key)

    OUTPUT.write_text(json.dumps(files, ensure_ascii=False, indent=2), encoding='utf-8')


if __name__ == '__main__':
  main()