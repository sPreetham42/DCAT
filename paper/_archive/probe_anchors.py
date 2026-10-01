# Prints the exact current text around each fix anchor that failed to match,
# so the repair entries can be corrected byte-for-byte.
import re

SRC = "HUMAN_EDITABLE_MANUSCRIPT.md"
text = open(SRC, encoding="utf-8").read()

PROBES = [
    ("H 2.4", "2.4 Content Representations for Images"),
    ("H 2.6", "2.6 Conditional Computation and Early Exits"),
    ("H 3.5 tail", "3.6 Gaps in Surveyed Literature"),
    ("H 4", "4. Problem Formulation"),
    ("H 6.2", "6.2 Number of datasets"),
    ("H 10", "10. Conclusion and future work"),
    ("X gap3", "Class imbalance in the cited studies"),
    ("X 3intro families", "three approach families"),
    ("S 5.4 tail", "D img is the MobileViT feature dimension"),
    ("S 5.9 list", "5.9 Inference Pipeline"),
    ("S fig3", "[FIGURE 3 - PREPROCESSING FLOW]"),
    ("C 8.2 direction", "single-measure contribution of Full-DCAT"),
    ("C 8.4 4.46", "4.46% of the messages"),
    ("C 9.1 scarcity", "mere 11 emails"),
    ("F 9.1 labels", "Single corpus. All experiments"),
    ("F 9.2 labels3", "Frozen encoders. DistilBERT"),
]

for name, frag in PROBES:
    i = text.find(frag)
    print(f"\n===== {name} (idx {i}) =====")
    if i < 0:
        # try a shorter fragment
        i2 = text.find(frag.split()[0])
        print(f"  primary fragment NOT FOUND; first-word idx {i2}")
        if i2 >= 0:
            print(repr(text[max(0, i2 - 150):i2 + 400]))
        continue
    lo, hi = max(0, i - 120), i + 420
    print(repr(text[lo:hi]))
