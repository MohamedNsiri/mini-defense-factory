#!/usr/bin/env bash
# The only step needing Internet. Run once, then commit veille/instantane/.
set -euo pipefail
cd "$(dirname "$0")/../veille/instantane"
CVE="CVE-2021-41773"
curl -fsSL "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json" -o kev.json
curl -fsSL "https://api.first.org/data/v1/epss?cve=${CVE}" -o "epss_${CVE}.json"
curl -fsSL "https://www.cert.ssi.gouv.fr/alerte/feed/" -o certfr_feed.xml
date -u +"snapshot taken: %Y-%m-%dT%H:%M:%SZ" > SNAPSHOT_DATE.txt
echo "Snapshot saved:"; ls -la
