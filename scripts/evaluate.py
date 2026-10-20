#!/usr/bin/env python3
"""Compare the agent's tickets/*.json with ground_truth.json."""
import json, pathlib, sys
root = pathlib.Path(__file__).resolve().parent.parent
truth = json.loads((root / "ground_truth.json").read_text())["cibles"]
ok = 0
lines = ["| Asset | Expected | Agent | Exposed | Exploitable | Result |", "|---|---|---|---|---|---|"]
for asset, exp in truth.items():
    f = root / "tickets" / f"{asset}.json"
    if not f.exists():
        lines.append(f"| {asset} | {exp['conclusion']} | MISSING | | | FAIL |"); continue
    t = json.loads(f.read_text())
    good = (t.get("conclusion") == exp["conclusion"] and t.get("expose") == exp["expose"]
            and t.get("exploitable") == exp["exploitable"])
    ok += good
    lines.append(f"| {asset} | {exp['conclusion']} | {t.get('conclusion')} | {t.get('expose')} | "
                 f"{t.get('exploitable')} | {'OK' if good else 'FAIL'} |")
lines.append(f"\nScore: {ok}/{len(truth)}")
out = "\n".join(lines)
print(out)
(root / "results").mkdir(exist_ok=True)
(root / "results" / "evaluation.md").write_text(out + "\n")
sys.exit(0 if ok == len(truth) else 1)
