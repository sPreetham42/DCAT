# Probe the exact current text around the 17 failed anchors in REGENERATED_SOURCE.md.
import re

T = open("REGENERATED_SOURCE.md", encoding="utf-8").read()

ANCHORS = [
    ("2.4", "2.4"),
    ("2.6", "2.6"),
    ("3.5 tail", "approach"),
    ("4", "4. Problem Formulation"),
    ("6.2", "6.2"),
    ("10", "10. Conclusion"),
    ("gap3", "Class imbalance"),
    ("3intro families", "families"),
    ("5.4 tail", "Layer normalization"),
    ("5.9 list", "5.9"),
    ("fig3", "[FIGURE 3"),
    ("8.2 direction", "opposite"),
    ("8.4 4.46", "4.46"),
    ("9.1 scarcity", "scarcity"),
    ("9.1 labels", "9.1"),
    ("9.2 labels3", "9.2"),
    ("1800", "1800"),
    ("Res Net", "Res Net"),
    ("effected significantly", "effected"),
    ("4 of 4", "4 of 4"),
]

for name, pat in ANCHORS:
    i = T.find(pat)
    print(f"\n===== {name} :: {pat!r} (idx {i}) =====")
    if i >= 0:
        print(repr(T[max(0, i - 260):i + 320]))
