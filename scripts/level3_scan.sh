#!/usr/bin/env bash
# Level 3: SAST (Semgrep) + DAST (OWASP ZAP baseline) on the home-made app.
# OpenVAS/Greenbone: run it separately with the official Greenbone community
# containers (https://greenbone.github.io/docs/latest/22.4/container/) and attach
# it to the 'mdf_dmz' network. It is heavy: use the 32 GB machine.
set -euo pipefail
cd "$(dirname "$0")/.."
OUT=results/level3; mkdir -p "$OUT"

echo "== Semgrep (static) =="
docker run --rm -v "$PWD/code-maison:/src" returntocorp/semgrep:latest \
  semgrep scan --config auto --json -o /src/../semgrep.json /src 2>/dev/null \
  || docker run --rm -v "$PWD:/work" -w /work returntocorp/semgrep:latest \
     semgrep scan --config auto --json -o results/level3/semgrep.json code-maison

echo "== OWASP ZAP baseline (dynamic) on the mdf_dmz network =="
docker run --rm --network mdf_dmz -v "$PWD/$OUT:/zap/wrk:rw" ghcr.io/zaproxy/zaproxy:stable \
  zap-baseline.py -t http://172.20.0.20:5000 -J zap.json -r zap.html -I || true
echo "Reports in $OUT/"
