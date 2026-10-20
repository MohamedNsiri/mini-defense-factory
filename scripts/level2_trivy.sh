#!/usr/bin/env bash
# Level 2: image composition scan with Trivy (needs Internet for the vuln DB).
set -euo pipefail
cd "$(dirname "$0")/.."
OUT=results/level2; mkdir -p "$OUT"
for img in vulhub/httpd:2.4.49 httpd:2.4.51; do
  name=$(echo "$img" | tr '/:' '__')
  docker run --rm -v /var/run/docker.sock:/var/run/docker.sock -v "$PWD/$OUT:/out" \
    aquasec/trivy:latest image --format json -o "/out/trivy_${name}.json" "$img"
done
echo "Trivy reports in $OUT/ - import them into DefectDojo."
