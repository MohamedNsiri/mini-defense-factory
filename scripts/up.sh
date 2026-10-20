#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
docker compose up -d --build
sleep 5
docker compose ps
echo
echo "Check that the 'a documenter' config is really disabled:"
docker exec web-legacy-01 sh -c "grep -A4 '<Directory />' /usr/local/apache2/conf/httpd.conf" || true
echo "Check the vulnerable one is really enabled:"
docker exec web-front-01 sh -c "grep -A4 '<Directory />' /usr/local/apache2/conf/httpd.conf" || true
