#!/usr/bin/env bash
set -euo pipefail

root_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
output_dir="$root_dir/dist"
ROC="${ROC:-roc}"
args=()

while (($# > 0)); do
    case "$1" in
        --output-dir)
            if (($# < 2)) || [[ -z "$2" ]]; then
                echo "--output-dir requires a directory" >&2
                exit 1
            fi
            output_dir="$2"
            shift 2
            ;;
        --output-dir=*)
            output_dir="${1#--output-dir=}"
            shift
            ;;
        *)
            args+=("$1")
            shift
            ;;
    esac
done

mkdir -p "$output_dir"
output_dir="$(cd "$output_dir" && pwd)"
cd "$root_dir/package"

# Include every module, including internal modules, without a hand-maintained list.
# Keep main.roc first so consumers can import the package entry point.
roc_files=(main.roc)
while IFS= read -r -d '' file; do
    roc_files+=("${file#./}")
done < <(find . -type f -name '*.roc' ! -path './main.roc' -print0)

# macOS ships Bash 3, where an empty array under set -u needs this guard.
if ((${#args[@]} > 0)); then
    "$ROC" bundle "${roc_files[@]}" --output-dir "$output_dir" "${args[@]}"
else
    "$ROC" bundle "${roc_files[@]}" --output-dir "$output_dir"
fi
