# Second-round probe: exact bytes around the remaining failed anchors.
import sys
sys.stdout.reconfigure(encoding="utf-8", errors="backslashreplace")

text = open("REGENERATED_SOURCE.md", encoding="utf-8").read()

PROBES = [
    ("C 8.2 direction", "single-measure contribution"),
    ("C 8.4 4.46", "4.46%"),
    ("C 9.1 scarcity", "mere 11 emails"),
    ("F 9.1 labels", "Single corpus"),
    ("F 9.2 labels3", "Frozen encoders"),
    ("LayerNorm sent", "Layer normalization after the linear projection"),
    ("H3 intro applied", "Work is grouped into approach families"),
    ("3.6 heading", "3.6 Gaps in Surveyed"),
    ("gap3 region", "Class imbalance in the cited"),
]

for name, frag in PROBES:
    i = text.find(frag)
    print(f"\n===== {name} (idx {i}) =====")
    if i < 0:
        print("  NOT FOUND")
        continue
    print(repr(text[max(0, i - 200):i + 480]))

# char-level diff for the H 10 conclusion sentence
mine = ("10. Conclusion and future work This paper presented the conditional "
        "multimodal email spam detection architecture DCAT combining "
        "bidirectional cross-attention, deterministic routing, and optional "
        "early-exit computation evaluated on a natural multimodal pair of "
        "corpora (Spam Assassin), where the defining property is multimodal "
        "scarcity (11/6,046 emails) under a text-only majority (99.4%).")
i = text.find("10. Conclusion and future work")
print("\n===== H 10 char-diff =====")
if i < 0:
    print("  heading NOT FOUND")
else:
    actual = text[i:i + len(mine) + 40]
    for k, (a, b) in enumerate(zip(mine, actual)):
        if a != b:
            print(f"first divergence at {k}: mine={a!r} (U+{ord(a):04X}) actual={b!r} (U+{ord(b):04X})")
            print("mine  :", repr(mine[max(0,k-40):k+40]))
            print("actual:", repr(actual[max(0,k-40):k+40]))
            break
    else:
        print("prefix matches; actual tail:", repr(actual[len(mine)-20:]))
