# Catalogue equation-block states + glued headings in REGENERATED_SOURCE.md.
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
T = open("REGENERATED_SOURCE.md", encoding="utf-8").read()

print("=== EQUATION REGION CATALOGUE ===")
for n in range(1, 22):
    m = re.search(rf"\[Equation {n}\]", T)
    if not m:
        print(f"Eq {n:2}: MISSING MARKER")
        continue
    i = m.start()
    after = T[i:i + 240].replace("\n", "\\n")
    print(f"Eq {n:2} @{i}: {after!r}")

print("\n=== GLUED / MALFORMED HEADING CATALOGUE ===")
lines = T.splitlines()
for k, ln in enumerate(lines):
    if "### ###" in ln or re.search(r"\S ### \d", ln):
        print(f"L{k+1}: {ln[:150]!r}")
    elif re.match(r"^#{1,3} \d+\.\d.*\S.*\S {2,}", ln):
        print(f"L{k+1} (glued-h3?): {ln[:150]!r}")

print("\n=== H-LEVEL SHAPES PRESENT ===")
for pat, label in [
    (r"(?m)^# \d", "hash1 numbered"),
    (r"(?m)^## \d+\.\d", "hash2 x.y (wrong)"),
    (r"(?m)^### \d+\.\d", "hash3 x.y"),
    (r"(?m)^## \d+\. ", "hash2 'N. '"),
    (r"(?m)^# \d+\.\d", "hash1 x.y (wrong)"),
]:
    print(f"  {label}: {len(re.findall(pat, T))}")
