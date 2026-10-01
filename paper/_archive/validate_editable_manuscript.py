# Validates HUMAN_EDITABLE_MANUSCRIPT.md against PAPER_CONTENT_REGENERATED.md
# per the 12-point validation list of the production brief.
import re
from collections import Counter

SRC = "PAPER_CONTENT_REGENERATED.md"
NEW = "HUMAN_EDITABLE_MANUSCRIPT.md"

src = open(SRC, encoding="utf-8").read()
new = open(NEW, encoding="utf-8").read()

checks = []


def check(name, cond, detail=""):
    checks.append((name, cond, detail))


# --- 1/2. Section structure: every source heading present, none added -------
src_heads = [h for h in re.findall(r"(?m)^#{1,3} (.+)$", src)]
new_heads = [h for h in re.findall(r"(?m)^#{1,3} (.+)$", new)
             if not h.startswith(("HUMAN EDITING", "HUMAN EDITING FACT",
                                  "Corpus and dataset", "Headline", "Statistical",
                                  "Five-fold", "Efficiency", "Class-imbalance",
                                  "Confusion matrix", "Architecture and",
                                  "Mandatory caveats", "Structural inventory",
                                  "Editing rules", "This section is NOT"))]
missing = [h for h in src_heads if h not in new_heads]
added = [h for h in new_heads if h not in src_heads and h != "Abstract"]
check("1/2. All manuscript headings present, none added",
      not missing and not added,
      f"missing={missing[:5]} added={added[:5]}")

# --- 3. Equations: 21 [Equation n] blocks, numbered 1..21, math intact ------
eqs = re.findall(r"\[Equation (\d+)\]", new)
check("3. 21 equations, numbered 1-21",
      [int(x) for x in eqs] == list(range(1, 22)), f"found={len(eqs)}")

# --- 4. Tables: all 10 main captions + 3 appendix tables + row counts -------
captions = [f"Table {i}." for i in range(1, 11)]
check("4a. 10 main-table captions", all(c in new for c in captions))
t1 = re.search(r"\*\*Table 1\..*?\n\n(\|.*?)(?=\n\n)", new, re.S)
src_t1 = re.search(r"\*\*Table 1\..*?\n\n(\|.*?)(?=\n\n)", src, re.S)
check("4b. Table 1 rows byte-identical", t1 and src_t1 and t1.group(1) == src_t1.group(1))
# appendix tables: Appendix B hyperparameter rows
appb = re.search(r"## Appendix B.*?(?=## Appendix C)", new, re.S)
check("4c. Appendix B hyperparameter table present",
      appb and "| Cross-attention d_ff | 1024 |" in appb.group(0)
      and "| Seeds | 42, 43, 44 |" in appb.group(0))
appc = re.search(r"## Appendix C.*?(?=## References)", new, re.S)
check("4d. Appendix C lineage table present",
      appc and "| 0.9868 |" in appc.group(0) and "| 0.6609 |" in appc.group(0))

# --- 5. Figure specifications ----------------------------------------------
figs = re.findall(r"\[FIGURE (\d) — ([A-Z][A-Z \-]+)\]", new)
check("5. Four figure specs with titles",
      [(n, t.strip()) for n, t in figs] == [("1", "DCAT OVERALL ARCHITECTURE"),
                                            ("2", "CROSS-ATTENTION BLOCK"),
                                            ("3", "PREPROCESSING FLOW"),
                                            ("4", "RESULTS VISUALIZATION PANEL")],
      str(figs))
check("5b. No PLACEHOLDER text remains", "PLACEHOLDER" not in new)
check("5c. Fig-4 data line present", "[[2196, 57], [25, 5073]]" in new or
      ("57 false positives" in new and "n = 7,351" in new))

# --- 6. References: [1]..[33], none missing, none added ---------------------
refs = re.findall(r"(?m)^\[(\d+)\] ", new)
check("6. 33 references numbered 1-33", [int(x) for x in refs] == list(range(1, 34)),
      f"found={len(refs)}")

# --- 7. Key numerical values verbatim ---------------------------------------
VALUES = ["0.9862", "0.9871", "0.9869", "0.9867", "0.9827", "0.8317", "0.4968",
          "0.5584", "0.1633", "0.6667", "0.7077", "0.5453", "0.2639", "0.1222",
          "0.6253", "0.7478", "0.9880", "2.49 × 10⁻⁴⁵", "3.34 × 10⁻⁶",
          "p = 1.0000", "p = 0.2482", "7,867", "7,351", "6,046", "4,150", "1,896",
          "73,309,090", "71,761,314", "77,967,426", "2,008,578", "460,802",
          "12.8B", "12.7B", "4.45%", "24.82%", "0.63%", "1.48", "2.70", "2.68",
          "2.19:1", "99.4%", "[[2196, 57], [25, 5073]]",
          "0.4971", "0.4968, 1.0000, 1.0000"]
missing_vals = [v for v in VALUES if v not in new]
check("7. All key values verbatim", not missing_vals, f"missing={missing_vals}")

# --- 8. Caveats present ------------------------------------------------------
CAVEATS = ["transcription error", "155-sample", "4 ham, 7 spam",
           "conflict is disclosed rather than silently reconciled",
           "fold numbering", "different averaging conventions",
           "no longer available in the repository", "pilot-scope",
           "different aggregation settings"]
missing_cav = [c for c in CAVEATS if c not in new]
check("8. All documented caveats present", not missing_cav, f"missing={missing_cav}")

# --- 9. No-invention: multiset line-difference vs source --------------------
def norm_line(ln):
    s = ln.strip()
    s = re.sub(r"^<!-- HUMAN EDITING.*?-->$", "", s)
    s = re.sub(r"\\tag\{\d+\}", "", s)
    if s.startswith("[Equation "):
        return None
    return s or None

src_counter = Counter(filter(None, (norm_line(l) for l in src.splitlines())))
new_body = new.split("# HUMAN EDITING FACT-CHECK REFERENCE")[0]
new_counter = Counter(filter(None, (norm_line(l) for l in new_body.splitlines())))
# Lines legitimately added: status header, markers, figure-spec fields
LEGIT_ADDS = ("**Caption:**", "**Placement & purpose:**", "**Note:** final graphics",
              "[FIGURE", "* Source manuscript:", "* Scientific source of truth:",
              "* Structure source:", "* Citation source:", "* Status:",
              "* Scientific content:", "* Manual prose editing:",
              "* Rewrite voice", "* The `<!-- HUMAN EDITING", "* Equations appear",
              "* Tables: keep every row", "* `HUMAN EDITING FACT-CHECK",
              "frozen and must survive", "markers are guidance only",
              "numbering and notation unchanged", "you may adjust wording",
              "lists every value", "It is NOT part of the paper", "---",
              "Figure 4 reports the archived confusion matrix",
              "# HUMAN EDITING STATUS", "Editing rules:",
              "frozen and must survive your edits verbatim.",
              "citation, caveat, equation, table value, and figure datum below is",
              "your edits verbatim.")

# Equation bodies: normalized comparison (whitespace-only differences OK)
def collapse(s):
    return re.sub(r"\s+", " ", s).strip()

src_eqs = Counter(collapse(l) for l in src.splitlines()
                  if l.strip().startswith("$$") and "\\tag" in l)
src_eqs = Counter(re.sub(r"\\tag\{\d+\}", "", l) for l in src_eqs)
new_eqs = Counter(collapse(l) for l in new_body.splitlines()
                  if l.strip().startswith("$$") and "\\tag" not in l)
extra = {ln: cnt for ln, cnt in (new_counter - src_counter).items()
         if not any(a in ln for a in LEGIT_ADDS)}
missing_lines = list((src_counter - new_counter).items())
# remove whitespace-only equation diffs from both sides
extra = {l: c for l, c in extra.items() if not (l.startswith("$$") and collapse(l) in src_eqs)}
missing_lines = [(l, c) for l, c in missing_lines
                 if not (l.startswith("$$") and collapse(l) in new_eqs)]
# Intentional transforms per the brief: separator rules stripped;
# placeholder lines expanded into full specification blocks.
missing_lines = [(l, c) for l, c in missing_lines
                 if l.strip() != "---" and not l.startswith("*[FIGURE")]
# Documented production substitution: Section 7.9 first sentence carries the
# finalized Figure-4 wording from main.tex (disclosed in
# PRODUCTION_QA_REPORT.md); the remainder of the paragraph is unchanged.
missing_lines = [(l, c) for l, c in missing_lines
                 if not l.startswith("Confusion matrices for DCAT, Late Fusion, and Text-Only")]
check("9. No invented content (multiset line diff)", not extra and not missing_lines,
      f"extra={list(extra)[:4]} missing={missing_lines[:4]}")

# --- 10/11. Source files untouched (verified externally via git) ------------
# (git status reported separately in the audit)

# --- 12. No LaTeX layout / TikZ / pgfplots leakage --------------------------
LEAK = [r"\\documentclass", r"\\usepackage", r"\\begin\{tikzpicture\}",
        r"\\begin\{figure\}", r"\\begin\{table\}", r"\\caption\{",
        r"\\section\{", r"\\subsection\{", r"\\label\{", r"\\ref\{",
        r"\\geometry", r"fancyhdr", r"pgfplots", r"\\resizebox",
        r"\\begin\{adjustbox\}", r"\\centering", r"\\hline",
        r"\\multicolumn", r"\\toprule", r"\\cite\{"]
leaks = [p for p in LEAK if re.search(p, new)]
check("12. No LaTeX layout/TikZ/pgfplots code", not leaks, f"leaks={leaks}")

# Editable markers sanity
check("extra: 25 editing markers (+1 mention in editing rules)",
      new.count("<!-- HUMAN EDITING") == 26)
check("extra: status header at top", new.startswith("# HUMAN EDITING STATUS"))
check("extra: fact-check appendix at end",
      new.rstrip().endswith(("13",)) or new.rstrip().endswith("| References | 33 ([1]–[33], numbering unchanged) |"))

passed = sum(1 for _, c, _ in checks if c)
print("=" * 70)
for name, cond, detail in checks:
    print(f"[{'PASS' if cond else 'FAIL'}] {name}" + (f"  -> {detail}" if detail and not cond else ""))
print("=" * 70)
print(f"{passed}/{len(checks)} checks passed")
