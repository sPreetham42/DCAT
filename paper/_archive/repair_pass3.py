# REPAIR PASS 3 — final residual fixes for REGENERATED_SOURCE.md
# Targets verified against current bytes after pass 2.
import re
import sys

F = "REGENERATED_SOURCE.md"
text = open(F, encoding="utf-8").read()

FIXES = []


def fix(name, old, new, count=1):
    FIXES.append((name, old, new, count, False))


def fixre(name, pat, new, count=1):
    FIXES.append((name, pat, new, count, True))


# 2.5 heading level (##### -> ###)
fix("H 2.5 lvl", "##### 2.5 Attention and Cross-Modal Attention",
    "### 2.5 Attention and Cross-Modal Attention")

# 9.2 label punctuation (labels already bold from pass 1)
fix("H 9.2 a", "**Frozen encoders.** DistilBERT and MobileViT are frozen, they were not fine-tuned on the domain data.",
    "**Frozen encoders.** DistilBERT and MobileViT are frozen; they were not fine-tuned on the domain data.")
fix("H 9.2 b", "fused after crossattention; we did not test other fusion methods.",
    "fused after cross-attention; we did not test other fusion methods.")

# 6.2 debris paste (regex-tolerant tail: single newline before 'Table 1')
fixre("H 6.2",
      r"6\.2 Number of datasets, sets and set leakage3\.2\.1\. Sets3\.2\.2\.1\. Leakage3\.2\.2\. Data sets3\.2\.2\.4\. Sequence and set setsThere are five datasets included in the dataset:12,1234 as well as the training, validation, and testing datasets\.12,12,12,2,12,2,3,12,123\.12\.16\.5,12,2,4\.12,124\.1\.4,23,4\.15,22,22\.2\.12,3\.23,42,52,1\.3,4A fundamental distinction of the series is that the mixed data sets and the train, validation, and test data are \(to varying degrees\) distributed – i\.e\., not randomly distributed\.12,12,12,2,12,2,3,4Distribution of the data sets \(usage within the training, validation, and test sets\)\.12,12,1253\.1,2,1,2,1,26,3,3,34,2,6\.2\.2\.2\.6\.2\.2\.8\.8\.2\.3\.9\.9\.2\.3\.10\.10\.2\.3\.11\.11\.2\.1\.3\.2\.2\.4\.3\.2\.4\.3\.2\.4\.3\.2\.4\.3\.2\.4\.3\.2\.4\.3\.2\.1\.14\.14\.15\.8\.\nTable 1 shows the structure of the processed corpus\.",
      "### 6.2 Dataset Composition, Splits, and Leakage Control\n\nTable 1 shows the structure of the processed corpus.")

log = []
failed = []
for name, old, new, expected, is_re in FIXES:
    if is_re:
        text, n = re.subn(old, lambda m, _n=new: _n, text, flags=re.S)
    else:
        n = text.count(old)
        if n:
            text = text.replace(old, new)
    log.append((name, n, expected))
    if n != expected:
        failed.append((name, n, expected))

text = re.sub(r"\n{3,}", "\n\n", text)
open(F, "w", encoding="utf-8", newline="\n").write(text)

for name, n, exp in log:
    status = "OK " if n == exp else "FAIL"
    print(f"[{status}] {name}: applied {n} (expected {exp})")
if failed:
    print(f"\n{len(failed)} FIXES NEED ATTENTION:")
    for name, n, exp in failed:
        print(f"  - {name}: got {n}, expected {exp}")
    sys.exit(1)
print(f"\nAll {len(FIXES)} pass-3 fixes applied. Wrote {F} ({len(text.split())} words)")
