# Roc package template

A minimal Roc package with tests, examples, cross-platform CI, automated
releases, documentation publishing, and compiler-update PRs.

## Get started

1. Create a repository from this template.
2. Replace the `package/Example.roc` module with your own module(s). List public modules in `package/main.roc`.
3. Replace the `examples/getting-started.roc` example, and add more if needed.
4. Replace this README with your package's documentation.

## Run and test

Install [Roc](https://github.com/roc-lang/nightlies/releases) at the version in [.roc-version](.roc-version) and Python 3.10+.

```sh
roc examples/getting-started.roc
./scripts/all_tests.sh
python3 scripts/test_bundle_examples.py
```

## Publish and maintain

Configure GitHub once using the [setup guide](docs/maintaining.md#github-setup).
Then run **Actions → Release** with a new tag such as `v0.1.0`.
The **Update Roc** CI workflow automatically proposes tested PRs every week to update the Roc compiler.

- [Development](docs/development.md): package layout, bundling, and local checks.
- [Releases and maintenance](docs/maintaining.md): GitHub setup, releases, docs, and compiler updates.
