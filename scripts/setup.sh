#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."

for cmd in docker curl; do
  command -v "$cmd" >/dev/null 2>&1 || { echo "ERREUR: '$cmd' introuvable. Installe-le avant de continuer."; exit 1; }
done
docker compose version >/dev/null 2>&1 || { echo "ERREUR: 'docker compose' introuvable."; exit 1; }

echo "== 1/5: threat-intel snapshot =="
if [ -f veille/instantane/kev.json ]; then
  echo "snapshot already present, skipping (delete veille/instantane/*.json to refetch)"
else
  mkdir -p veille/instantane
  ./scripts/fetch_veille.sh
fi

echo
echo "== 2/5: building the observer and the base vulnerable targets =="
docker compose build observateur web-front-01 app-01

echo
echo "== 3/5: building the target that depends on web-front-01 =="
docker compose build web-legacy-01

echo
echo "== 4/5: pulling the remaining pre-built images =="
docker compose pull web-patched-01 db-01

echo
echo "== 5/5: starting the lab =="
mkdir -p results/level1 results/level2 results/level3
docker compose up -d
sleep 5
docker compose ps

echo
echo "Setup complete. Run ./scripts/status.sh to verify everything works."
