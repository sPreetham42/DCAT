# Third-round probe: exact bytes for the remaining repair anchors, from both
# the edited manuscript (damage) and the pristine baseline (approved wording).
import sys
sys.stdout.reconfigure(encoding="utf-8", errors="backslashreplace")

EDIT = open("HUMAN_EDITABLE_MANUSCRIPT.md", encoding="utf-8").read()
PRIS = open("pristine_baseline_tmp.md", encoding="utf-8").read()
REG = open("REGENERATED_SOURCE.md", encoding="utf-8").read()


def show(text, frag, before=150, after=900, label=""):
    i = text.find(frag)
    print(f"\n===== {label} :: {frag[:40]!r} (idx {i}) =====")
    if i < 0:
        print("  NOT FOUND")
        return
    print(repr(text[max(0, i - before):i + after]))


# --- edited manuscript: regions whose exact damaged bytes I still need
show(EDIT, "8.2 Signal, Scarcity", before=100, after=1400, label="EDIT 8.2 region")
show(EDIT, "6.2 Number of datasets", before=60, after=1100, label="EDIT 6.2 debris")
show(EDIT, "[FIGURE 3 - PREPROCESSING FLOW]", before=40, after=1500, label="EDIT fig3 block")
show(EDIT, "5.9 Inference Pipeline", before=40, after=1200, label="EDIT 5.9 list")

# --- pristine: approved wording for the damaged regions
for frag in ["Summary of Gaps", "gaps emerge", "Class imbalance in the multimodal",
             "5.9 Inference Pipeline", "[FIGURE 3 - PREPROCESSING FLOW]",
             "Layer normalization after the linear projection",
             "single-measure", "On the multimodal test subset",
             "approach families", "identical-theory"]:
    show(PRIS, frag, before=120, after=700, label="PRISTINE")

# --- post-run-1 sanity: leftover debris patterns
print("\n===== POST-RUN-1 DEBRIS SCAN =====")
BANNED = ["gentrification", "functional form is as essential", "EFS is the first",
          "reorganisation", "Timothy Hosp", "1800", "4.46%", "9.84%",
          "0.001 significance", "five emails", "4 of 4", "Spam Assassin",
          "Res Net", "Mobile Net", "[Equations 11, 12]", "2.1. Conditional computation",
          "# ### ", "effected significantly", "D img is the MobileViT"]
for b in BANNED:
    n = REG.count(b)
    print(f"  {b!r}: {n}")
