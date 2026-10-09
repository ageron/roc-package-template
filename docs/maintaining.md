# Releases and maintenance

[← README](../README.md)

## GitHub setup

- Enable GitHub Actions. Tests run on pushes and pull requests on Linux (x64/ARM64), macOS (Intel/Apple Silicon),
  and Windows (x64), including tests against an actual package archive.
- In **Settings → Pages**, select **GitHub Actions** as the publishing source.
  Allow the `github-pages` environment to deploy from your release branches and
  tags if you use environment protection rules.
- To enable automatic compiler-update and release-example PRs, turn on **Allow GitHub Actions to
  create and approve pull requests** under **Settings → Actions → General**.
  The workflow creates PRs; it does not approve or merge them. Repository or
  organization policies may need to allow this setting.

No personal access token is required. Workflows use the repository's built-in
`GITHUB_TOKEN` with permissions scoped to each job.

## Release a version

Run **Actions → Release → Run workflow**, select the branch to release, and
enter a new tag such as `v0.1.0`. The workflow checks the sources, builds a
content-addressed `.tar.zst` archive, tests that same archive on all five
OS/architecture combinations, and creates a GitHub release at the selected commit. It
attaches the documentation built during those checks as `package-docs.tar.gz`,
then deploys that exact documentation to Pages.

After publishing, it updates the alias configured in `.package-alias` to the
new archive URL and validates the examples on all five runners. Only after
all checks pass does it open a follow-up PR against the release branch. Review
and merge it yourself. Failed validation leaves the release published but
creates no example-update PR. Rerun failed jobs to retry; the branch is reused
within the same workflow run. These bot PRs link their validation run because
`GITHUB_TOKEN` does not trigger ordinary PR checks.

Release notes include a ready-to-copy import URL. Use the package archive's
download URL in your consumers' app headers:

```roc
pkg: "https://github.com/OWNER/REPOSITORY/releases/download/v0.1.0/HASH.tar.zst"
```

The release build and archive tests also run on pull requests, without
publishing. **Deploy release docs** can redeploy the latest release or a selected tag
without reinstalling Roc. Releases published manually must also attach
`package-docs.tar.gz` to use this workflow. The Release workflow calls it explicitly because events
created using `GITHUB_TOKEN` do not start ordinary downstream workflows.

## Update Roc

`.roc-version` is the single compiler pin used by all workflows through
`.github/actions/setup-roc/action.yml`. The **Update Roc** workflow checks for
a newer nightly weekly; it can also be run manually with an optional exact
nightly tag. It runs the full five-runner test suite with the candidate before
opening or updating a PR on `codex/update-roc-nightly`.

If checks fail, the pin stays unchanged and the workflow logs show what needs
to be fixed. You can also edit `.roc-version` in a normal PR. If you later add an external
platform to your examples, check its compiler compatibility during upgrades.

Update PRs created with `GITHUB_TOKEN` do not automatically trigger the normal
PR workflows. The update workflow therefore runs the same tests explicitly
before creating the PR and links that validation run in its description. If
branch protection requires PR-triggered checks, configure a GitHub App token
for PR creation or arrange the required checks accordingly.

The workflows build and publish artifacts only; they never merge compiler
updates automatically.

## CI behavior

CI builds one archive on Linux and tests those exact bytes on every
runner, including Windows. Releases are serialized across branches;
stale PR validation runs are cancelled. Missing artifacts fail the build.

The docs site serves one release at its root. Historical versioned docs
and API compatibility checks with `roc bump` are optional extensions,
not enabled by this template. Local checks substitute the working package
into temporary example copies, even when checked-in examples use release URLs.
