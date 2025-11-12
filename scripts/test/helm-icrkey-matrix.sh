#!/usr/bin/env bash
set -euo pipefail

CHART_DIR="charts/qiskit-studio"
REL="qas"

# Work in a temp dir to store large helm outputs and avoid writing to stdout (prevents SIGPIPE 141)
TMPDIR=$(mktemp -d -t icrkey-matrix.XXXXXX)
cleanup() { rm -rf "$TMPDIR"; }
trap cleanup EXIT

pass() { echo "[PASS] $1"; }
fail() { echo "[FAIL] $1"; exit 1; }

# Case 1: values-local.yaml + alias -> auto secret rendered, default name
case1="$TMPDIR/case1.yaml"
helm template "$REL" "$CHART_DIR" -f "$CHART_DIR/values-local.yaml" --set-string icrkey=TESTKEY > "$case1"
# Prefer fixed-string match on the rendered source header; if not found, fall back to a structural check
if ! grep -Fq "# Source: qiskit-studio/templates/image-pull-secret.yaml" "$case1"; then
	# Fallback: detect a Secret document of type dockerconfigjson (our auto ICR secret)
	awk 'BEGIN{RS="\n---\n"} /kind: Secret/ && /type: kubernetes.io\/dockerconfigjson/ {found=1} END{exit found?0:1}' "$case1" || fail "Case1: auto secret not rendered"
fi
name=$(awk '/kind: Secret/{flag=1}flag && /metadata:/{print;getline;print;exit}' "$case1" | awk -F": " '/name:/{print $2}')
[[ "$name" =~ -icrkey$ ]] || fail "Case1: secret name does not end with -icrkey: $name"
grep -q "imagePullSecrets:" "$case1" || fail "Case1: imagePullSecrets block missing"
grep -q -- "- name: $name" "$case1" || fail "Case1: imagePullSecrets not wired to $name"
pass "Case1"

# Case 2: values-local.yaml without alias -> no auto secret
case2="$TMPDIR/case2.yaml"
helm template "$REL" "$CHART_DIR" -f "$CHART_DIR/values-local.yaml" > "$case2"
! grep -q "^# Source: qiskit-studio/templates/image-pull-secret.yaml" "$case2" || fail "Case2: unexpected auto secret rendered"
pass "Case2"

# Case 3: values-local-ingress.yaml + alias -> auto secret rendered
case3="$TMPDIR/case3.yaml"
helm template "$REL" "$CHART_DIR" -f "$CHART_DIR/values-local-ingress.yaml" --set-string icrkey=TESTKEY > "$case3"
if ! grep -Fq "# Source: qiskit-studio/templates/image-pull-secret.yaml" "$case3"; then
	awk 'BEGIN{RS="\n---\n"} /kind: Secret/ && /type: kubernetes.io\/dockerconfigjson/ {found=1} END{exit found?0:1}' "$case3" || fail "Case3: auto secret not rendered for ingress profile"
fi
pass "Case3"

# Case 4: alias + custom name override -> secret created with custom name and wired
case4="$TMPDIR/case4.yaml"
helm template "$REL" "$CHART_DIR" -f "$CHART_DIR/values-local.yaml" --set-string icrkey=TESTKEY --set global.imagePullSecrets.name=customname > "$case4"
grep -q "name: customname" "$case4" || fail "Case4: customname not found in secret metadata"
grep -q "imagePullSecrets:" "$case4" || fail "Case4: imagePullSecrets block missing"
grep -q -- "- name: customname" "$case4" || fail "Case4: imagePullSecrets not wired to customname"
pass "Case4"

# Case 5: legacy create=true path -> legacy template renders; our auto secret skipped
case5="$TMPDIR/case5.yaml"
helm template "$REL" "$CHART_DIR" --set global.imagePullSecrets.create=true --set global.imagePullSecrets.name=mysec --set-string global.imagePullSecrets.value=dummy > "$case5"
grep -q "^# Source: qiskit-studio/templates/imagepullsecret.yaml" "$case5" || fail "Case5: legacy imagepullsecret.yaml not rendered"
! grep -q "^# Source: qiskit-studio/templates/image-pull-secret.yaml" "$case5" || fail "Case5: auto secret should be skipped when create=true"
pass "Case5"

# Case 6: Skip - removed reference to cloud-specific values file
echo "[SKIP] Case6: Skipping cloud profile test"

# Case 7: pre-existing secret name provided in values -> workloads should reference it, no auto create
case7="$TMPDIR/case7.yaml"
helm template "$REL" "$CHART_DIR" -f "$CHART_DIR/values-local.yaml" --set global.imagePullSecrets.name=icrkey > "$case7"
! grep -q "^# Source: qiskit-studio/templates/image-pull-secret.yaml" "$case7" || fail "Case7: auto secret should not render when name provided without key"
grep -q "imagePullSecrets:" "$case7" || fail "Case7: imagePullSecrets block missing"
grep -q -- "- name: icrkey" "$case7" || fail "Case7: workloads not referencing provided name"
pass "Case7"

echo "All icrkey matrix tests passed."