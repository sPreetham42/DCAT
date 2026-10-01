# Final verification of REGENERATED_SOURCE.md (repaired human-edited manuscript).
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
T = open("REGENERATED_SOURCE.md", encoding="utf-8").read()
ok = lambda b: "PASS" if b else "FAIL"
BS = chr(92)
res = []

# 1. all 21 equations have $$ bodies after the marker
missing = [n for n in range(1, 22)
           if not re.search(r"\[Equation %d\]\n\n\$\$[^$]" % n, T)]
res.append(("21 equations with bodies", not missing, missing))

# 2. debris scan (all zero expected)
debris = {p: T.count(p) for p in [BS + "1\n", "1800:1", "4.46", "Res Net", "Mobile Net",
    "# ###", "#####", "2.1. Conditional", "gentrification", "econometric",
    "EFS", "UMass", "thermodynamic", "Timothy Hosp", "five emails", "4 of 4",
    "p = 2.49 10", "0.001 significance"]}
res.append(("zero debris", all(v == 0 for v in debris.values()), debris))

# 3. artifact-verified dataset counts present (pass 5)
counts = {v: T.count(v) for v in ["75,419", "73,206", "7,542", "60,335", "7,867", "7,351", "6,046"]}
res.append(("dataset counts", all(v > 0 for v in counts.values()), counts))

# 4. glue separators gone
glue = len(re.findall(r"[a-z]\. ###", T)) + len(re.findall(r" ### ", T))
res.append(("no glue separators", glue == 0, glue))

# 5. headings: approved ## sections
secs = re.findall(r"^## (.+)$", T, re.M)
res.append(("approved ## sections", len(secs) >= 10, secs))

# 6. key verified values present
vals = ["0.9862", "0.9869", "0.9871", "0.8317", "0.4968", "0.7077", "0.5453",
        "0.7478", "2.49", "3.34", "4.45", "0.63", "24.82", "12.8B", "12.7B",
        "73,309,090"]
missing_v = [v for v in vals if v not in T]
res.append(("key values", not missing_v, missing_v))

# 7. figures / tables / references
figs = re.findall(r"\[FIGURE \d", T)
res.append(("4 figure specs", len(figs) == 4, figs))
res.append(("33 refs [1]..[33]", all(("[%d]" % i) in T for i in range(1, 34)), None))

# 8. no human-editing markers left
res.append(("no edit markers", "HUMAN EDITING:" not in T, None))

# 9. no LaTeX layout code (chr(92)-built to survive any transport quirk)
lat = [p for p in [BS + "documentclass", BS + "usepackage",
                   BS + "begin{tikzpicture", BS + "begin{table}",
                   BS + "begin{figure}", BS + "includegraphics",
                   BS + "begin{document}"] if p in T]
res.append(("no LaTeX code", not lat, lat))

# 10. word count
res.append(("word count > 12k", len(T.split()) > 12000, len(T.split())))

fails = 0
for name, cond, info in res:
    if not cond:
        fails += 1
    print(ok(cond), "|", name, "|", info)
print("\nTOTAL FAILS:", fails)
