# REPAIR PASS 6: unglue [Equation 7]/[Equation 8] markers from preceding prose,
# split glued "$$...$$<prose>" bodies (Eqs 4, 19, 20, 21) into body + prose blocks.
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
F = "REGENERATED_SOURCE.md"
T = open(F, encoding="utf-8").read()
n0 = len(T)

FIXES = [
    ("Eq7 marker unglue", "hidden states: [Equation 7]",
     "hidden states:\n\n[Equation 7]"),
    ("Eq8 marker unglue", "feature representations: [Equation 8]",
     "feature representations:\n\n[Equation 8]"),
    ("Eq4 body split", "$$where $\\hat{z}_i$ is the predicted logit",
     "$$\n\nwhere $\\hat{z}_i$ is the predicted logit"),
    ("Eq19 body split", "\\right), $$ where",
     "\\right), $$\n\nwhere"),
    ("Eq20 body split", "$$ and the exit rule is",
     "$$\n\nand the exit rule is"),
    ("Eq21 body split", "$$ For values in between",
     "$$\n\nFor values in between"),
]
for name, old, new in FIXES:
    c = T.count(old)
    if c == 1:
        T = T.replace(old, new)
        print("OK  ", name)
    elif c == 0:
        print("SKIP", name, "(already applied)")
    else:
        print("FAIL", name, "count =", c)
        sys.exit(1)

# safety: no other marker glued mid-line
glued = re.findall(r"[^\n]\[Equation \d+\]", T)
print("remaining glued markers:", glued)
assert not glued

T = re.sub("\n{3,}", "\n\n", T)
open(F, "w", encoding="utf-8", newline="\n").write(T)
print("pass 6 complete; delta chars:", len(T) - n0)
