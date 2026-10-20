# Frozen threat-intel snapshot
Run `scripts/fetch_veille.sh` ONCE, then commit the files. Never refresh during an
evaluation: the agent must always see the same alerts.
Expected files: kev.json, epss_CVE-2021-41773.json, certfr_feed.xml
