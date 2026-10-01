# Comprehensive verification of REGENERATED_SOURCE.md after all repair passes.
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
T = open("REGENERATED_SOURCE.md", encoding="utf-8").read()
ok = True


def chk(name, cond, extra=""):
    global ok
    print(f"[{'PASS' if cond else 'FAIL'}] {name} {extra}")
    if not cond:
        ok = False


print("=== 1. STRUCTURE ===")
h2 = re.findall(r"(?m)^## (.+)$", T)
h3 = re.findall(r"(?m)^### (.+)$", T)
print("H2:", h2)
chk("10 numbered sections present",
    all(any(h.startswith(f"{n}.") for h in h2) for n in range(1, 11)))
chk("no glued '# ###' lines", not re.search(r"(?m)^# ###", T))
chk("no '#####' levels", not re.search(r"(?m)^#####", T))
chk("no '# N.N' wrong-level subsections", not re.search(r"(?m)^# \d+\.\d", T))
chk("no '## N.N' wrong-level subsections", not re.search(r"(?m)^## \d+\.\d", T))
chk("no '### N.' wrong-level top sections", not re.search(r"(?m)^### \d+\. ", T))
chk("no bare 'N. Title' lines left",
    not re.search(r"(?m)^\d+\. (Introduction|Background|Related Work|Problem Formulation|The DCAT|Experimental|Results|Discussion|Limitations|Conclusion)", T))
# heading-glue detection: heading line that contains ' ### ' or ends with prose then heading
chk("no mid-line heading glue", not re.search(r"[a-z)\.]\s### ", T), "(patterns checked below)")
glue = re.findall(r"[^\n#]{40,} ### ", T)
print("  glue-like matches:", len(glue))
for g in glue[:5]:
    print("   ", g[:90])

print("\n=== 2. EQUATIONS ===")
eqs = sorted(set(int(x) for x in re.findall(r"\[Equation (\d+)\]", T)))
chk("21 equations, sequential 1-21", eqs == list(range(1, 22)), str(eqs))
bodies = len(re.findall(r"(?m)^\$\$", T)) // 2
chk("21 display-math blocks", bodies == 21, f"found {bodies}")

print("\n=== 3. TABLES / FIGURES / REFERENCES ===")
tabs = re.findall(r"\*\*Table (\d+)\.", T)
chk("10 main tables", [int(x) for x in tabs] == list(range(1, 11)), str(tabs))
figs = re.findall(r"\[FIGURE (\d+)", T)
chk("4 figures", [int(x) for x in figs] == [1, 2, 3, 4], str(figs))
refs = re.findall(r"(?m)^\[(\d+)\] ", T)
chk("33 references", [int(x) for x in refs] == list(range(1, 34)), f"n={len(refs)}")

print("\n=== 4. DEBRIS / FABRICATION SCAN ===")
for p in ["gentrification", "Wooldridge", "functional form is as essential", "EFS is the first",
          "reorganisation", "Timothy Hosp", "Number of datasets", "statisticist", "1800",
          "4.46%", "9.84%", "0.001 significance", "five emails", "4 of 4", "Spam Assassin",
          "Res Net", "Mobile Net", "[Equations 11, 12]", "2.1. Conditional",
          "effected significantly", "Image-identificationCNNs", "identical-theory",
          "3.2.1. Sets", "#####"]:
    n = T.count(p)
    chk(f"debris {p!r} == 0", n == 0, f"(found {n})")

print("\n=== 5. KEY VALUE PRESENCE ===")
VALUES = ["0.9862", "0.9869", "0.9871", "0.8317", "0.4968", "0.7077", "0.5453", "0.7478",
          "0.6253", "0.9880", "2.49 × 10⁻⁴⁵", "3.34 × 10⁻⁶", "4.45%", "0.63%", "24.82%",
          "12.8B", "12.7B", "73,309,090", "7,867", "7,351", "155", "2196", "5,073",
          "6,046", "4,150", "1,896", "73,206", "75,419"]
for v in VALUES:
    n = T.count(v)
    chk(f"value {v!r} present", n >= 1, f"(x{n})")

print("\n=== 6. CAVEAT PRESENCE ===")
CAV = ["disclosed rather than silently reconciled", "pilot sample", "0.9855",
       "transcription", "n = 7,351", "pooled out-of-fold"]
for c in CAV:
    n = T.count(c)
    chk(f"caveat {c!r}", n >= 1, f"(x{n})")

print("\n=== 7. BACK MATTER ===")
for s in ["## Data Availability", "## Declarations", "Competing interests",
          "## Appendix A", "## Appendix B", "## Appendix C", "## References"]:
    chk(f"back matter {s!r}", s in T)

print("\n=== 8. REAL BIBLIOGRAPHIC IDS (no ref1/ref2) ===")
chk("no 'ref1'", "ref1" not in T)
chk("no 'ref2'", "ref2" not in T)

print("\n" + ("ALL CHECKS PASS" if ok else "*** FAILURES PRESENT ***"))
sys.exit(0 if ok else 1)
