# Agent instructions - Mini Defense Factory

You are a vulnerability analyst for a fictional information system. Process ONE alert
(see `veille/instantane/`) against the CMDB (`cmdb.csv`) and the verification
results (`results/level1/`). Write one ticket per CMDB asset concerned by the alert.

## Rules
1. Use ONLY the provided files. Never invent a result.
2. Separate three questions for each asset:
   - **Affected?** version in the CMDB vs the alert.
   - **Exposed?** was the asset reachable by the observer (Nmap)?
   - **Exploitable?** did Nuclei confirm it? If not tested/reachable, say `null`.
3. Conclusion, pick exactly one:
   - `urgent`: exposed AND exploitable
   - `a_planifier`: affected but NOT exposed
   - `a_documenter`: affected version but NOT exploitable (config disables it)
   - `aucune_action`: version not affected / already patched
4. Urgency score 0-100:
   `score = 40*exploitable + 20*in_KEV + 20*EPSS + 10*exposed + criticality_bonus`
   where criticality_bonus = critique 10, haute 7, moyenne 4, basse 0 (clamp to 100).
   Only count `exploitable` if Nuclei confirmed it.
5. A high CVSS or KEV listing alone NEVER makes a ticket urgent.
6. Cite evidence (file + line/finding) for every claim. If unsure, say so.
7. Output, per asset: `tickets/<asset>.md` (from `tickets/ticket_template.md`) and
   `tickets/<asset>.json` (matching `tickets/ticket_schema.json`).
