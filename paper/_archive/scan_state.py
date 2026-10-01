# Ground-truth scan of REGENERATED_SOURCE.md after repair pass 1.
# Comprehensive debris inventory + exact-byte probes of the 17 failed anchors.
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

T = open("REGENERATED_SOURCE.md", encoding="utf-8").read()

print("=== A. DEBRIS / INTEGRITY SCAN ===")
DEBRIS = [
    "gentrification", "Wooldridge", "functional form is as essential",
    "EFS is the first", "reorganisation", "Timothy Hosp",
    "Number of datasets, sets", "statisticist", "1800", "4.46%", "9.84%",
    "0.001 significance", "five emails", "4 of 4", "Spam Assassin",
    "Res Net", "Mobile Net", "[Equations 11, 12]", "2.1. Conditional",
    "effected significantly", "Image-identificationCNNs", "D img is",
    "identical-theory", "3.2.1. Sets", "approach families",
]
for p in DEBRIS:
    print(f"  {p!r:42} {T.count(p)}")

print("\n=== B. STRUCTURE INVENTORY ===")
h1 = [ln for ln in T.splitlines() if re.match(r"^# \d", ln)]
h2 = [ln for ln in T.splitlines() if re.match(r"^## ", ln)]
h3 = [ln for ln in T.splitlines() if re.match(r"^### ", ln)]
hglue = [ln for ln in T.splitlines() if ln.startswith("# ###")]
print(f"H2 (##): {len(h2)}")
for ln in h2:
    print(f"   {ln[:80]}")
print(f"H3 (###): {len(h3)}")
for ln in h3:
    print(f"   {ln[:80]}")
print(f"glued '# ###' lines: {len(hglue)}")
for ln in hglue:
    print(f"   {ln[:80]}")
print(f"other '# ' headings: {h1}")

eqs = re.findall(r"\[Equation (\d+)\]", T)
print(f"\n[Equation n] markers: {len(eqs)} -> {sorted(set(int(e) for e in eqs))}")
bodies = len(re.findall(r"^\$\$", T, flags=re.M)) // 2
print(f"$$ display blocks: {bodies}")
figs = re.findall(r"\[FIGURE (\d+)", T)
print(f"[FIGURE n] markers: {figs}")
tabs = re.findall(r"\*\*Table (\d+)\.", T)
print(f"**Table n.** captions: {tabs}")
refs = re.findall(r"^\[(\d+)\] ", T, flags=re.M)
print(f"reference list entries: {len(refs)} -> {refs[:5]}...{refs[-3:]}")
cites = sorted(set(int(c) for c in re.findall(r"\[(\d{1,2})\]", T)))
print(f"distinct [n] cites in body: {len(cites)}")

print("\n=== C. FAILED-ANCHOR PROBES (exact bytes) ===")
PROBES = [
    ("2.4 heading", "Content Representations for Images"),
    ("2.6 heading", "Conditional Computation and Early Exits"),
    ("3.6 Gaps", "Gaps in Surveyed Literature"),
    ("3.5 tail", "pooled out-of-sample predictions"),
    ("H10", "10. Conclusion and future work"),
    ("8.2 direction", "single-measure contribution"),
    ("8.2 after-H82", "On the multimodal test subset,"),
    ("8.4 4.46", "4.46"),
    ("9.1 scarcity", "a mere 11 emails"),
    ("9.1 labels", "Single corpus"),
    ("9.2 labels3", "Frozen encoders"),
    ("Res Net all", "Res Net"),
    ("fig3 spec end", "the above specifications are the approved ones"),
    ("5.9 list", "5.9 Inference Pipeline"),
    ("gap3 end", 'visual "token'),
    ("econometrics", "The relationship between the variables could be linear"),
    ("# 4.1", "# 4.1 Task Definition"),
    ("# 5.5", "# 5.5 Bidirectional"),
]
for name, pat in PROBES:
    idxs = [m.start() for m in re.finditer(re.escape(pat), T)]
    print(f"\n--- {name} :: {pat!r} x{len(idxs)} ---")
    for i in idxs[:3]:
        seg = T[max(0, i - 120):i + 380]
        print(f"  @{i}: {seg!r}")
