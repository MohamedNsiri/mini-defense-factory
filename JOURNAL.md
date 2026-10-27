# Journal — Mini Defense Factory

## Acceptation des règles d'isolation (§0)

Date : 2026-10-23
Équipe : Mohamed Nsiri, Alexia Makaya, Fomi Shilavert

Nous, membres de l'équipe, avons pris connaissance des règles d'isolation
du laboratoire et nous engageons à les respecter pour toute la durée des
travaux pratiques :

1. Les réseaux du lab (172.20.0.0/24 DMZ, 172.21.0.0/24 interne) ne sont
   jamais exposés hors de la machine hôte. Aucun port du lab n'est publié
   vers le réseau physique.
2. Seul le téléchargement de l'instantané de veille (`scripts/fetch_veille.sh`)
   nécessite un accès Internet. Aucun autre trafic sortant n'est autorisé
   depuis les conteneurs du lab.
3. Les outils utilisés (Nmap, Nuclei, etc.) servent uniquement à vérifier,
   de façon non destructive, les cibles du lab (`172.20.0.10`, `.11`, `.12`,
   `172.21.0.10`, `.11`). Aucune machine hors de ce périmètre n'est scannée
   ou testée.

Signatures : <prénom nom 1>, <prénom nom 2>, <prénom nom 3>

---

## Journal des sessions

### Session TP1 — reconnaissance CVE-2021-41773
- Date : 2026-10-23
- Candidats testés : web-front-01 (172.20.0.10), web-legacy-01 (172.20.0.11), app-01 (172.21.0.10)
- Outils utilisés : nmap (exposition), nuclei (exploitabilité, non destructif)
- Résultats bruts : results/level1/nmap_dmz.txt, nmap_interne.txt, nuclei_*.jsonl
- IP contactées : 172.20.0.10, 172.20.0.11, 172.21.0.10 — toutes dans le périmètre du lab
- Aucune machine hors lab touchée
