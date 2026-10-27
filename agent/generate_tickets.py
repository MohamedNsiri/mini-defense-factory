
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CMDB = ROOT / "cmdb.csv"
RESULTS = ROOT / "results" / "level1"
VEILLE = ROOT / "veille" / "instantane"
TICKETS = ROOT / "tickets"

CVE = "CVE-2021-41773"
VERSION_VULNERABLE = "2.4.49"


def lire_fichier(chemin):
    if chemin.exists():
        return chemin.read_text(encoding="utf-8", errors="replace")
    return ""


def main():
    TICKETS.mkdir(exist_ok=True)

    # Lire les informations de veille
    epss_fichier = VEILLE / f"epss_{CVE}.json"
    epss_data = json.loads(lire_fichier(epss_fichier) or "{}")
    epss = float(epss_data.get("data", [{}])[0].get("epss", 0))

    kev_data = json.loads(lire_fichier(VEILLE / "kev.json") or "{}")
    kev = CVE in json.dumps(kev_data)

    # Lire les résultats des scans
    nmap_dmz = lire_fichier(RESULTS / "nmap_dmz.txt")
    nmap_interne = lire_fichier(RESULTS / "nmap_interne.txt")

    with CMDB.open(encoding="utf-8-sig", newline="") as fichier:
        machines = list(csv.DictReader(fichier))

    for machine in machines:
        asset = machine["asset"]
        ip = machine["ip"]
        version = machine["version"]
        service = machine["service"]
        criticite = machine["criticite"]
        responsable = machine["responsable"]
        maintenance = machine["fenetre_maintenance"]
        zone = machine["zone"]

        affected = (
            service == "Apache HTTP Server"
            and version == VERSION_VULNERABLE
        )

        # Vérifier si l'adresse IP apparaît dans les résultats Nmap.
        scan = nmap_dmz if zone == "DMZ" else nmap_interne
        expose = ip in scan and "80/tcp" in scan

        # Seul un résultat Nuclei positif confirme l'exploitation
        # de la vulnérabilité dans ce laboratoire.
        nuclei_file = RESULTS / f"nuclei_{ip}.jsonl"
        nuclei = lire_fichier(nuclei_file)
        exploitable = (
            True if affected and CVE in nuclei
            else None if affected and not expose
            else False
        )

        if exploitable is True and expose:
            conclusion = "urgent"
        elif affected and not expose:
            conclusion = "a_planifier"
        elif affected:
            conclusion = "a_documenter"
        else:
            conclusion = "aucune_action"

        bonus = {
            "critique": 10,
            "haute": 7,
            "moyenne": 4,
            "basse": 0,
        }.get(criticite.lower(), 0)

        score = round(
            40 * (exploitable is True)
            + 20 * kev
            + 20 * epss
            + 10 * expose
            + bonus
        )
        score = min(100, score)

        evidence = [
            f"CMDB : {asset}, IP {ip}, service {service}, version {version}.",
            f"Nmap : {'IP et port 80 trouvés dans le scan' if expose else 'exposition non confirmée par la règle simplifiée du script'}.",
            f"Nuclei : {'CVE confirmée dans le fichier de résultats' if exploitable is True else 'aucune confirmation positive trouvée dans le fichier'}.",
            f"Veille EPSS : score {epss}, date {epss_data.get('data', [{}])[0].get('date', 'inconnue')}.",
            f"CISA KEV : {'identifiant présent dans le fichier' if kev else 'identifiant non trouvé dans le fichier'}.",
        ]

        if conclusion == "urgent":
            action = "Prioriser la correction, vérifier les journaux et planifier la mise à jour."
        elif conclusion == "a_planifier":
            action = f"Vérifier l'exposition depuis les réseaux autorisés et planifier une correction. Fenêtre : {maintenance}."
        elif conclusion == "a_documenter":
            action = "Analyser les preuves et la configuration avant de conclure. Refaire un test autorisé si nécessaire."
        else:
            action = "Vérifier la version et conserver les preuves. Aucune correction liée à cette CVE n'est indiquée par les données actuelles."

        ticket = {
            "asset": asset,
            "cve": CVE,
            "conclusion": conclusion,
            "affected": affected,
            "expose": expose,
            "exploitable": exploitable,
            "kev": kev,
            "epss": epss,
            "score": score,
            "evidence": evidence,
            "action": action,
            "responsable": responsable,
            "fenetre_maintenance": maintenance,
            "confiance": (
                "Automatisation initiale : vérifier les fichiers Nmap et Nuclei. "
                "Une absence de résultat ne prouve pas l'absence de vulnérabilité."
            ),
        }

        # Créer le ticket JSON
        json_path = TICKETS / f"{asset}.json"
        json_path.write_text(
            json.dumps(ticket, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

        # Créer le ticket Markdown
        md = f"""# Ticket - {asset} - {CVE}

| Champ | Valeur |
|---|---|
| Asset | {asset} ({ip}) |
| Zone | {zone} |
| Responsable | {responsable} |
| Fenêtre de maintenance | {maintenance} |
| Criticité | {criticite} |
| Conclusion | **{conclusion}** |
| Score d'urgence | {score} / 100 |

## Résultats
- Affectée : {affected}
- Exposée (Nmap) : {expose}
- Exploitable confirmée (Nuclei) : {exploitable}
- Présente dans CISA KEV : {kev}
- EPSS : {epss}

## Preuves
""" + "\n".join(f"- {item}" for item in evidence) + f"""

## Action recommandée
{action}

## Confiance et limites
{ticket["confiance"]}
"""
        (TICKETS / f"{asset}.md").write_text(md, encoding="utf-8")

        print(f"[OK] {asset}: {conclusion}, score {score}/100")

    print(f"\nTickets générés dans : {TICKETS}")


if __name__ == "__main__":
    main()


