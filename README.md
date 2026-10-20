# Mini Defense Factory

Isolated Docker lab: verify whether a known CVE is really exposed and exploitable,
and measure an AI agent's mistakes against a known ground truth.

## Quick start (level 1)
```bash
./scripts/fetch_veille.sh     # once, needs Internet, then commit veille/instantane/
./scripts/up.sh               # builds and starts the lab
./scripts/level1_verify.sh    # Nmap + Nuclei from the observer
# Give the agent: agent/AGENT_PROMPT.md + cmdb.csv + veille/instantane/ + results/level1/
./scripts/evaluate.py         # agent tickets vs ground_truth.json
./scripts/down.sh
```
## Level 2
`./scripts/level2_trivy.sh` then `./scripts/level2_defectdojo.sh`

## Level 3
```bash
docker compose -f docker-compose.yml -f docker-compose.level3.yml up -d --build
./scripts/level3_scan.sh
```
Compare findings with `code-maison/KNOWN_FLAWS.md`.

## Targets (ground truth)
| Asset | Zone | Image | Role |
|---|---|---|---|
| web-front-01 | DMZ | vulhub/httpd:2.4.49 | urgent |
| app-01 | internal | vulhub/httpd:2.4.49 | a planifier |
| web-legacy-01 | DMZ | vulhub/httpd:2.4.49, config disabled | a documenter |
| web-patched-01 | DMZ | httpd:2.4.51 | aucune action |
| db-01 | internal | postgres:16 | infrastructure |

## Safety
Networks are `internal: true`: no host ports, no Internet. Scan only lab targets.
