# Development

[← README](../README.md)

Install the new Roc compiler release named in `.roc-version` from
[roc-lang/nightlies](https://github.com/roc-lang/nightlies/releases), plus
Python 3.10 or newer. Bash is used by the shell scripts. The example uses
Roc’s built-in host; no external platform or Zig installation is needed.

```sh
roc examples/getting-started.roc
./scripts/all_tests.sh
python3 scripts/test_bundle_examples.py
scripts/bundle.sh --output-dir dist
```

Set `ROC=/absolute/path/to/roc` to use a different compiler with either test
script or the bundler. Checks cover formatting, type checking, `expect` tests,
example execution and builds, and documentation generation. The bundle test
serves a real archive over localhost, replaces the examples' local package
path with its URL, then checks, tests, runs, builds and executes those examples.
It can also test an existing archive:

```sh
python3 scripts/test_bundle_examples.py --bundle-path dist/HASH.tar.zst
```

Examples under `examples/*.roc` are runnable apps. Keep them noninteractive so
CI can run them unattended. Generated files go in `dist/`, `generated-docs/`,
and `.roc-package-tmp/`, all ignored by Git.

## Package layout

Add public modules to `package/main.roc`. Bundling includes every `.roc` file
under `package/`, including internal modules; keep examples and development
scripts outside that directory. If your package needs non-Roc assets, extend
`scripts/bundle.sh` to include them explicitly.

Keep `"../package/main.roc"` as the package dependency in each example;
the bundle tests replace this path with the archive URL. The dependency
alias (`pkg` in the template) can be renamed freely.
