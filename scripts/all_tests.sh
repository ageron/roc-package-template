#!/usr/bin/env bash
set -euo pipefail

root_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$root_dir"
ROC="${ROC:-roc}"
mkdir -p dist/examples

"$ROC" version
"$ROC" fmt --check package examples

while IFS= read -r -d '' roc_file; do
    "$ROC" check "$roc_file"
    if grep -Eq '^[[:space:]]*expect([[:space:]]|$)' "$roc_file"; then
        "$ROC" test "$roc_file"
    fi
done < <(find package -type f -name '*.roc' -print0)

for roc_file in examples/*.roc; do
    "$ROC" check "$roc_file"
    "$ROC" test "$roc_file"
    "$ROC" "$roc_file"
    "$ROC" build "$roc_file" --output="dist/examples/$(basename "${roc_file%.roc}")"
done

"$ROC" docs package/main.roc
