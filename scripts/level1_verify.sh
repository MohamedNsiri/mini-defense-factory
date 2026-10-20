#!/usr/bin/env bash
# Level 1: Nmap (exposure) + Nuclei (exploitability), run FROM the observer.
set -euo pipefail
cd "$(dirname "$0")/.."
OUT=results/level1; mkdir -p "$OUT"
CVE="CVE-2021-41773"

echo "== 1. Exposure: Nmap from the observer =="
docker exec observateur nmap -sV -p 80 -n --host-timeout 20s 172.20.0.0/24 -oN /results/level1/nmap_dmz.txt
# The internal range must show NO host up (observer is not attached to it)
docker exec observateur nmap -sn -n --host-timeout 5s 172.21.0.10-11 -oN /results/level1/nmap_interne.txt || true

echo "== 2. Exploitability: Nuclei ($CVE), non-destructive =="
for ip in 172.20.0.10 172.20.0.11 172.20.0.12 172.21.0.10; do
  echo "-- $ip"
  docker exec observateur nuclei -u "http://$ip" -id "$CVE" -duc -silent -timeout 5 \
    -jsonl -o "/results/level1/nuclei_${ip}.jsonl" || true
  [ -s "$OUT/nuclei_${ip}.jsonl" ] && echo "   => MATCH (exploitable)" || echo "   => no match / unreachable"
done
echo "Results in $OUT/"
