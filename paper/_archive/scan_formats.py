# Format inventory of REGENERATED_SOURCE.md for the MD->LaTeX converter.
import re
import sys
from collections import Counter

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
T = open("REGENERATED_SOURCE.md", encoding="utf-8").read()
L = T.splitlines()

print("=== citation bracket patterns ===")
cits = re.findall(r"\[[0-9][0-9, \-]*\]", T)
print("count:", len(cits), "| distinct:", sorted(set(cits))[:40])

print("\n=== unicode non-ascii inventory ===")
uni = Counter(ch for ch in T if ord(ch) > 127)
for ch, n in uni.most_common(40):
    print(f"U+{ord(ch):04X} {ch!r} x{n}")

print("\n=== bold-line types (whole-line **...**) ===")
bl = Counter()
for l in L:
    if l.startswith("**") and l.rstrip().endswith("**"):
        key = l.split(".")[0][:34]
        bl[key] += 1
for k, v in bl.most_common(30):
    print(v, repr(k))

print("\n=== ### headings (all 50) ===")
for i, l in enumerate(L, 1):
    if l.startswith("### "):
        print(i, repr(l[:80]))

print("\n=== #### count ===", len([l for l in L if l.startswith("#### ")]))

print("\n=== numbered-list first words ===")
nl = [l for l in L if re.match(r"^\d+\. ", l)]
print("count:", len(nl))
for l in nl[:18]:
    print(" ", repr(l[:70]))

print("\n=== table cells containing markup ===")
for i, l in enumerate(L, 1):
    if l.startswith("|") and ("**" in l or "$" in l or "×" in l):
        print(i, repr(l[:100]))

print("\n=== note/source lines ===")
for i, l in enumerate(L, 1):
    if re.match(r"^\*?(Source|Note|Notes)\b", l) or l.startswith("**Source"):
        print(i, repr(l[:110]))

print("\n=== figure spec block line types ===")
i = next(i for i, l in enumerate(L) if l.startswith("[FIGURE 4"))
for j in range(i, i + 10):
    print(j + 1, repr(L[j][:105]))

print("\n=== equations with multi-line bodies (cases/aligned?) ===")
for n in range(1, 22):
    m = re.search(r"\[Equation %d\]\n\n\$\$(.*?)\$\$" % n, T, re.S)
    if m:
        b = m.group(1)
        flags = []
        if "&" in b: flags.append("&")
        if "\\\\" in b: flags.append("\\\\")
        if "\\begin" in b: flags.append("\\begin")
        if flags:
            print(f"Eq {n}: {flags}")

print("\n=== html comments remaining ===", len(re.findall(r"<!--", T)))
print("=== hr lines ===", len([l for l in L if re.match(r"^-{3,}$", l)]))
print("=== backtick spans ===", len(re.findall(r"`[^`]+`", T)))
print("sample:", re.findall(r"`[^`]+`", T)[:6])
