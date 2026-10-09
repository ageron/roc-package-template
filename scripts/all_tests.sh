#!/usr/bin/env bash
set -euo pipefail

root_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$root_dir"
ROC="${ROC:-roc}"

"$ROC" version
"$ROC" fmt --check package examples

while IFS= read -r -d '' roc_file; do
    "$ROC" check "$roc_file"
    if grep -Eq '^[[:space:]]*expect([[:space:]]|$)' "$roc_file"; then
        "$ROC" test "$roc_file"
    fi
done < <(find package -type f -name '*.roc' -print0)

# Published example URLs must not hide regressions in the working package.
python3 -m unittest discover -s scripts -p test_example_dependencies.py
ROC="$ROC" python3 scripts/test_bundle_examples.py --local

"$ROC" docs package/main.roc
