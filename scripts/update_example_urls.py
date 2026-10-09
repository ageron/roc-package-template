#!/usr/bin/env python3
"""Update the configured dependency in each example to a published bundle URL."""
from __future__ import annotations

import argparse
from urllib.parse import urlsplit

from example_dependencies import ROOT, read_alias, update_examples


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--bundle-url', required=True)
    args = parser.parse_args()
    url = urlsplit(args.bundle_url)
    if url.scheme not in {'http', 'https'} or not url.netloc or not url.path.endswith('.tar.zst'):
        parser.error('--bundle-url must be an HTTP(S) package URL ending in .tar.zst')
    try:
        alias = read_alias()
        update_examples(ROOT / 'examples', alias, args.bundle_url)
    except ValueError as error:
        parser.error(str(error))
    print(f'Examples now use {alias}: "{args.bundle_url}"')


if __name__ == '__main__':
    main()
