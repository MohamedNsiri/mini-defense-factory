#!/usr/bin/env bash
# Level 2: DefectDojo via its official docker compose (cloned OUTSIDE this repo).
set -euo pipefail
cd "$(dirname "$0")/../.."
[ -d django-DefectDojo ] || git clone --depth 1 https://github.com/DefectDojo/django-DefectDojo.git
cd django-DefectDojo
./dc-build.sh && ./dc-up.sh postgres-redis
echo "UI: http://localhost:8080 - admin password:"
docker compose logs initializer 2>/dev/null | grep "Admin password" || true
echo "Then: create a product 'Mini Defense Factory' and import results/level1 (Nuclei JSON), nmap XML, results/level2 (Trivy JSON), and the agent tickets."
