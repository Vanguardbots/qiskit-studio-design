#!/bin/bash
#
# A script to recursively find and test Helm charts in a directory.
# All temporary files and downloaded binaries are stored in ./.cache/helm_test_runner/

set -o pipefail # Fails a pipeline if any command fails

# --- Configuration ---
CACHE_DIR=".cache/helm_test_runner"
BIN_DIR="$CACHE_DIR/bin"
TEMP_DIR="$CACHE_DIR/tmp"
KUBECONFORM_VERSION="v0.6.6"
KUBECONFORM_PATH="$BIN_DIR/kubeconform"
SEARCH_DIR=${1:-.} # Default to current directory if no argument is provided

# --- Create cache directories ---
mkdir -p "$BIN_DIR"
mkdir -p "$TEMP_DIR"

# --- Color Codes for Output ---
C_RESET=$'\033[0m'
C_RED=$'\033[0;31m'
C_GREEN=$'\033[0;32m'
C_YELLOW=$'\033[0;33m'
C_BLUE=$'\033[0;34m'
C_BOLD=$'\033[1m'
C_RED_BOLD=$'\033[1;31m'

# --- Counters for Summary ---
declare -i total_tests=0; declare -i passed_tests=0; declare -i failed_tests=0
declare -i charts_found=0; declare -i lint_issues_found=0; declare -i total_symlinks_found=0

# --- Helper Functions for Pretty Printing ---
print_info() { echo "${C_BLUE}INFO: $1${C_RESET}"; }
print_pass() { echo "    ${C_GREEN}└─ STATUS: PASS${C_RESET}"; }
print_fail() { echo "    ${C_RED}└─ STATUS: FAIL${C_RESET}"; }
print_warn() { echo "    ${C_YELLOW}└─ STATUS: SKIPPED${C_RESET}"; }
print_header() { echo -e "\n${C_BOLD}${C_BLUE}🔎 Testing Chart: $1${C_RESET}"; }
print_line() { printf -- '-%.0s' {1..80}; printf '\n'; }

# --- Cleanup trap for temporary files ---
trap 'rm -rf "$TEMP_DIR"' EXIT

# --- Kubeconform Setup Function ---
setup_kubeconform() {
    if [ -x "$KUBECONFORM_PATH" ]; then return; fi
    print_info "Kubeconform not found. Downloading to $BIN_DIR..."
    local os; os=$(uname -s | tr '[:upper:]' '[:lower:]')
    local arch; arch=$(uname -m); case "$arch" in x86_64) arch="amd64" ;; arm64 | aarch64) arch="arm64" ;; esac
    if [ -z "$os" ] || [ -z "$arch" ]; then echo "${C_RED}Unsupported OS/Arch: $(uname -s)/$(uname -m)${C_RESET}"; exit 1; fi
    local url="https://github.com/yannh/kubeconform/releases/download/${KUBECONFORM_VERSION}/kubeconform-${os}-${arch}.tar.gz"
    print_info "Downloading from $url"
    if ! curl -sL "$url" | tar -xz -C "$BIN_DIR"; then echo "${C_RED}Failed to download or extract Kubeconform.${C_RESET}"; exit 1; fi
    if [ ! -x "$KUBECONFORM_PATH" ]; then echo "${C_RED}Kubeconform executable not found after download.${C_RESET}"; exit 1; fi
    print_info "Kubeconform setup complete."
}

# --- Lint Check Function ---
run_lint_check() {
    local chart_dir=$1
    echo "  - Lint Check"
    local lint_cmd="helm lint \"$chart_dir\""
    echo "    ${C_YELLOW}└─ COMMAND:${C_RESET} $lint_cmd"

    local lint_output; lint_output=$(eval "$lint_cmd" 2>&1)
    # FIX: Save the exit code of helm lint IMMEDIATELY after it runs.
    local lint_exit_code=$?

    local symlink_count; symlink_count=$(echo "$lint_output" | grep -c "found symbolic link" || true)
    if [ "$symlink_count" -gt 0 ]; then
        ((total_symlinks_found+=symlink_count))
    fi

    # FIX: Check the saved exit code, not the exit code of the symlink count command.
    if [ $lint_exit_code -ne 0 ]; then
        print_fail
        echo "      ${C_RED}└─ REASON: Helm lint found issues.${C_RESET}"
        ((lint_issues_found++))
        echo "$lint_output" \
            | sed '/walk\.go.*found symbolic link/s/^/[INFO] /' \
            | sed "s/\[ERROR\]/${C_RED_BOLD}&${C_RED}/g" \
            | sed "s/\[WARNING\]/${C_YELLOW}&${C_RED}/g" \
            | sed "s/\[INFO\]/${C_BLUE}&${C_RED}/g" \
            | sed "s/^/          ${C_RED}| ${C_RESET}/"
    else
        print_pass
    fi
}

# --- Validation Test Function ---
run_test() {
    local chart_dir=$1; local display_name=$2; local values_file_arg=$3
    ((total_tests++))
    echo "  - Validation Test Case: ${C_BOLD}$display_name${C_RESET}"
    local helm_cmd="helm template test-release \"$chart_dir\" $values_file_arg"
    local full_log_cmd="$helm_cmd | $KUBECONFORM_PATH -strict -summary"
    echo "    ${C_YELLOW}└─ COMMAND:${C_RESET} $full_log_cmd"
    local helm_stderr_file; helm_stderr_file=$(mktemp "$TEMP_DIR/helm_stderr_XXXXXX")
    local template_output; template_output=$(eval "$helm_cmd" 2> "$helm_stderr_file")
    local helm_exit_code=$?

    local other_warnings; other_warnings=$(grep -v "found symbolic link" "$helm_stderr_file")
    if [ -n "$other_warnings" ]; then
        echo "      ${C_YELLOW}└─ HELM WARNINGS:${C_RESET}"
        echo "$other_warnings" | sed "s/^/          ${C_YELLOW}| ${C_RESET}/"
    fi

    if [ $helm_exit_code -ne 0 ]; then
        print_fail; echo "      ${C_RED}└─ REASON: Helm template command failed (see warnings above).${C_RESET}";
        ((failed_tests++)); return
    fi
    if [ -z "$template_output" ]; then
        print_warn; echo "      ${C_YELLOW}└─ REASON: Helm template produced no output.${C_RESET}";
        ((total_tests--)); return
    fi
    local validation_output; validation_output=$(echo "$template_output" | "$KUBECONFORM_PATH" -strict -summary 2>&1)
    if [ $? -ne 0 ]; then
        print_fail; echo "      ${C_RED}└─ REASON: Kubeconform validation failed.${C_RESET}";
        echo "$validation_output" | sed "s/^/          ${C_RED}| ${C_RESET}/" >&2
        ((failed_tests++)); return
    fi
    print_pass; ((passed_tests++))
}

# --- Main Script Logic ---
print_line; print_info "Starting Helm Chart Test Runner"
print_info "All temp files and binaries will be stored in ./$CACHE_DIR"
print_info "Searching for charts in: $(realpath "$SEARCH_DIR" 2>/dev/null || echo "$SEARCH_DIR")"; print_line
setup_kubeconform

while IFS= read -r -d $'\0' chart_yaml_path; do
    ((charts_found++))
    chart_dir=$(dirname "$chart_yaml_path"); chart_name=$(basename "$chart_dir")
    print_header "$chart_name (in $chart_dir)"
    run_lint_check "$chart_dir"
    run_test "$chart_dir" "default values" ""
    while IFS= read -r -d $'\0' values_file; do
        run_test "$chart_dir" "$(basename "$values_file")" "-f \"$values_file\""
    done < <(find "$chart_dir" -maxdepth 1 \( -name "values-*.yaml" -o -name "*.values.yaml" -o -name "values-*.yml" -o -name "*.values.yml" \) -print0)
done < <(find "$SEARCH_DIR" -name "Chart.yaml" -print0)

# --- Final Summary ---
print_line; echo "${C_BOLD}Test Summary${C_RESET}"; print_line
echo "Charts Found:       ${C_BLUE}$charts_found${C_RESET}"
echo "Total Tests Run:    ${C_BLUE}$total_tests${C_RESET}"
echo "  ${C_GREEN}Passed:           $passed_tests${C_RESET}"
echo "  ${C_RED}Failed:           $failed_tests${C_RESET}"; print_line
echo "${C_BOLD}Informational Checks${C_RESET}"; print_line
echo "Lint Issues Found:  ${C_YELLOW}$lint_issues_found${C_RESET}"
echo "Symlinks Detected:  ${C_YELLOW}$total_symlinks_found${C_RESET}"; print_line

if [ "$failed_tests" -gt 0 ]; then exit 1; fi
