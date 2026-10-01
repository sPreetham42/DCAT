# Builds latex/main.tex from REGENERATED_SOURCE.md (repaired human-edited manuscript).
# Preamble, table column specs, table env headers, and the four figure environments
# are reused verbatim from main_frozen_backup.tex (approved production layout).
# ALL prose comes from the repaired manuscript; nothing is rewritten here.
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

SRC = "REGENERATED_SOURCE.md"
FROZEN = "latex/main_frozen_backup.tex"
OUT = "latex/main.tex"

md = open(SRC, encoding="utf-8").read()
frozen = open(FROZEN, encoding="utf-8").read()

# ---------------------------------------------------------------- frozen bits
BS = chr(92)
title_idx = frozen.find(BS + "title{")
preamble = frozen[:title_idx]

docbeg = frozen.find(BS + "begin{document}")
title_block = frozen[title_idx:docbeg]  # \title, \author, \date

# --- author block (final): author + email only; guide line removed ----------
OLD_AUTHOR = "Preetham S" + BS + BS + "{" + BS + "normalsize" + BS + "itshape (Guide: Dr." + BS + " Prathima Mabel)}"
NEW_AUTHOR = ("Preetham S" + BS + BS + "{" + BS + "normalsize" + BS + "itshape "
              + BS + "href{mailto:spreetham6442@gmail.com}{spreetham6442@gmail.com}}")
assert OLD_AUTHOR in title_block, "guide author line not found"
title_block = title_block.replace(OLD_AUTHOR, NEW_AUTHOR)

# float package needed for [H] appendix tables
assert BS + "usepackage{adjustbox}" in preamble
preamble = preamble.replace(BS + "usepackage{adjustbox}",
                            BS + "usepackage{adjustbox}\n" + BS + "usepackage{float}", 1)

# figure environments keyed by label
# figure environments keyed by label; caption refs are remapped from the
# frozen equation-label scheme to this build's eq:N labels
EQREF_MAP = {"eq:qkv-t2i": 12, "eq:t2i": 13, "eq:qkv-i2t": 14, "eq:i2t": 15,
             "eq:ztextout": 16, "eq:zimgout": 17, "eq:routing": 3}
figenvs = {}
for m in re.finditer(re.escape(BS + "begin{figure}") + r".*?" + re.escape(BS + "end{figure}"), frozen, re.S):
    blk = m.group(0)
    lm = re.search(re.escape(BS + "label{") + r"(fig:[^}]*)\}", blk)
    if lm:
        for old, nnew in EQREF_MAP.items():
            blk = blk.replace(BS + "eqref{" + old + "}", BS + "eqref{eq:%d}" % nnew)
        figenvs[lm.group(1)] = blk

# --- figure-source repairs (visual QA findings, 2026-09-19) ----------------
# Fig 1: leftover unused node (poolmm) drew an empty box overlapping the
# cross-attention block; no arrow references it — remove the node line.
BAD_NODE = BS + "node[box, below=4.5mm of $(txtproj)!0.5!(imgproj)$, yshift=2mm, fill=gray!8] (poolmm) {" + BS + "phantom{Mean pooling}};"
blk = figenvs["fig:architecture"]
assert BAD_NODE in blk, "fig1 poolmm node not found"
figenvs["fig:architecture"] = blk.replace(BAD_NODE + "\n", "").replace(BAD_NODE, "")
# Fig 2: attention/formula boxes (~40mm wide) overlapped across the 34mm
# column gap; widen the column separation so the two streams never collide.
blk = figenvs["fig:crossattention"]
assert "right=34mm of lnT" in blk, "fig2 column distance not found"
figenvs["fig:crossattention"] = blk.replace("right=34mm of lnT", "right=46mm of lnT")
# Fig 3: modality leaf boxes (TEXT/IMAGE/MULTIMODAL) were 1mm apart and their
# labels collided; widen separations (and the EMPTY callout gap accordingly).
blk = figenvs["fig:preprocessing"]
assert "below left=5mm and 1mm of assign.south" in blk, "fig3 leaf spacing not found"
blk = blk.replace("below left=5mm and 1mm of assign.south", "below left=5mm and 8mm of assign.south")
blk = blk.replace("below right=5mm and 1mm of assign.south", "below right=5mm and 8mm of assign.south")
blk = blk.replace("right=8mm of assign, dashed", "right=13mm of assign, dashed")
figenvs["fig:preprocessing"] = blk

assert set(figenvs) == {"fig:architecture", "fig:crossattention", "fig:preprocessing", "fig:results"}, figenvs.keys()

# table env headers (everything from \begin{table} up to and including
# \begin{tabular}{...}) and appendix captions, keyed by label
def outer_brace(s, start):
    """start points at '{'; return index of its matching '}'."""
    depth = 0
    for p in range(start, len(s)):
        if s[p] == "{":
            depth += 1
        elif s[p] == "}":
            depth -= 1
            if depth == 0:
                return p
    raise ValueError("unbalanced")

# Fig 4 (results panel): rebuild so (a)/(b) are an intentionally paired pair.
# Both plot regions now span y in [0, 3.7cm] exactly (matrix bottom row bottom
# edge and axis bottom share the y=0 baseline; tops both at 3.7cm), and both
# panel labels are anchored south at the same y. Caption text is reused
# verbatim from the approved environment.
blk = figenvs["fig:results"]
ci = blk.find(BS + "caption{")
ck = outer_brace(blk, ci + len(BS + "caption{") - 1)
cap = blk[ci + len(BS + "caption{"):ck]
NEW_F4 = BS + r"""begin{figure}[t]
\centering
\begin{adjustbox}{max width=\textwidth}
\begin{tikzpicture}
% ---- panel (a): DCAT confusion matrix (weighted-primary, full test set) ----
% plot region spans y in [0, 3.7]; label row above at y=4.05
\node[font=\scriptsize] at (1.15,3.55) {Predicted ham};
\node[font=\scriptsize] at (3.40,3.55) {Predicted spam};
\node[draw, fill=cellhi, text=white, minimum width=22mm, minimum height=16mm, font=\small] at (1.15,2.55) {2196};
\node[draw, fill=celllo, minimum width=22mm, minimum height=16mm, font=\small] at (3.40,2.55) {57};
\node[draw, fill=celllo, minimum width=22mm, minimum height=16mm, font=\small] at (1.15,0.80) {25};
\node[draw, fill=cellhi, text=white, minimum width=22mm, minimum height=16mm, font=\small] at (3.40,0.80) {5073};
\node[font=\scriptsize, anchor=east] at (-0.20,2.55) {Actual ham};
\node[font=\scriptsize, anchor=east] at (-0.20,0.80) {Actual spam};
\node[font=\footnotesize\bfseries, anchor=south] at (1.45,4.05) {(a) DCAT --- weighted-primary, full test set};
% ---- panel (b): multimodal Macro-F1 comparison (Table 3 values) ----
\begin{scope}[xshift=7.2cm]
\begin{axis}[
  name=axb, anchor=south west, at={(0,0)},
  width=6.4cm, height=3.7cm,
  ybar,
  bar width=5.2pt,
  ymin=0, ymax=1.0,
  ylabel={\scriptsize MM-Macro-F1},
  ylabel style={font=\scriptsize},
  ytick={0,0.2,0.4,0.6,0.8,1.0},
  yticklabel style={font=\tiny},
  symbolic x coords={ASP, MI, Text, Image, PB, LF, NoXAttn, DCAT, EE},
  xtick=data,
  xticklabel style={font=\tiny, rotate=60, anchor=east},
  enlarge x limits=0.08,
  tick style={line width=0.3pt},
  axis line style={line width=0.4pt},
]
\addplot[fill=celllo!70!cellhi, draw=cellhi] coordinates {
  (ASP,0.4968) (MI,0.4968) (Text,0.5584) (Image,0.4968)
  (PB,0.4968) (LF,0.4968) (NoXAttn,0.8317) (DCAT,0.4968) (EE,0.4968)
};
\end{axis}
\node[font=\footnotesize\bfseries, anchor=south] at (3.2,4.05) {(b) Multimodal Macro-F1 by variant};
\end{scope}
\end{tikzpicture}
\end{adjustbox}
\caption{""" + cap + "}" + "\n" + BS + "label{fig:results}\n" + BS + "end{figure}"
figenvs["fig:results"] = NEW_F4

tabhdr = {}
for m in re.finditer(re.escape(BS + "begin{table}") + r"(?:(?!" + re.escape(BS + "begin{table}") + r").)*?" + re.escape(BS + "begin{tabular}"), frozen, re.S):
    blk = m.group(0)
    lm = re.search(re.escape(BS + "label{") + r"(tab:[^}]*)\}", blk)
    if lm:
        end = outer_brace(frozen, m.end())  # colspec may contain nested {}
        tabhdr[lm.group(1)] = frozen[m.start():end + 1]
assert len(tabhdr) == 13, sorted(tabhdr)

# bib keys in file order == reference numbers [1]..[33]
bib = open("latex/references.bib", encoding="utf-8").read()
bibkeys = re.findall(r"@\w+\{([^,\s]+)\s*,", bib)
assert len(bibkeys) == 33

# ---------------------------------------------------------------- helpers
FILE_EXTS = (".csv", ".json", ".md", ".pdf", ".eml", ".txt", ".py", ".log", ".bib", ".tex")
ROOTS = ("artifacts/", "results/", "latex/", "data/", "docs/", "experiments/", "scripts/")

def filelike(p):
    return p.endswith(FILE_EXTS) or p.startswith(ROOTS)

MATH_TOKEN = "\x00MATH%d\x00"

def protect_math(s):
    spans = []
    def repl(m):
        spans.append(m.group(0))
        return MATH_TOKEN % (len(spans) - 1)
    return re.sub(r"\$[^$]+\$", repl, s), spans

def restore_math(s, spans):
    for i, sp in enumerate(spans):
        s = s.replace(MATH_TOKEN % i, sp)
    return s

SUPER = {"\u207b": "-", "\u2070": "0", "\u00b9": "1", "\u00b2": "2",
         "\u00b3": "3", "\u2074": "4", "\u2075": "5", "\u2076": "6"}

def inline(s):
    """Markdown inline -> LaTeX for one paragraph/line (math spans untouched)."""
    s, spans = protect_math(s)
    # citations [n] / [n,m,...]
    def cite(m):
        nums = [int(x) for x in m.group(1).split(",")]
        if all(1 <= n <= 33 for n in nums):
            return BS + "citep{" + ",".join(bibkeys[n - 1] for n in nums) + "}"
        return m.group(0)
    s = re.sub(r"\[(\d{1,2}(?:\s*,\s*\d{1,2})*)\]", cite, s)
    # bold then italics
    s = re.sub(r"\*\*(.+?)\*\*", lambda m: BS + "textbf{" + m.group(1) + "}", s)
    s = re.sub(r"(?<!\*)\*([^*\n]+?)\*(?!\*)", lambda m: BS + "emph{" + m.group(1) + "}", s)
    # code spans: file-like spans (dot extension or known root dir) become
    # breakable \path; slash pairs like ham/spam or seeds 42/43/44 stay text
    def codify(m):
        raw = m.group(1)
        if filelike(raw):
            return BS + "path{" + raw + "}"
        return BS + "code{" + raw.replace("_", BS + "_").replace(", ", "," + BS + "allowbreak ") + "}"
    s = re.sub(r"`([^`]+)`", codify, s)
    # unbackticked file-like tokens (results/tables/main_results_multimodal.csv)
    s = re.sub(r"(?<![A-Za-z0-9_./{\\])([A-Za-z0-9_./-]+/[A-Za-z0-9_.-]*\.(?:csv|json|md|pdf|eml|txt|py|log|bib|tex))\b",
               lambda m: BS + "path{" + m.group(1) + "}", s)
    # unicode punctuation / symbols
    s = s.replace("\u00d7", "$" + BS + "times$")
    s = s.replace("\u2192", "$" + BS + "rightarrow$")
    s = s.replace("\u2248", "$" + BS + "approx$")
    s = s.replace("\u03b1", "$" + BS + "alpha$")
    s = s.replace("\u00b7", BS + "textperiodcentered{}")
    s = s.replace("\u2013", "--").replace("\u2014", "---").replace("\u2212", "-")
    s = re.sub("[" + "".join(SUPER) + "]+",
               lambda m: "$^{" + "".join(SUPER[c] for c in m.group(0)) + "}$", s)
    # escaping
    s = s.replace("%", BS + "%")
    s = re.sub(r"(?<!\\)&", BS + "&", s)
    s = re.sub(r"(?<!\\)_", BS + "_", s)
    s = re.sub(r"(?<!\\)#", BS + "#", s)
    # straight double quotes -> latex quotes (alternating)
    out, open_q = [], True
    for ch in s:
        if ch == '"':
            out.append("``" if open_q else "''")
            open_q = not open_q
        else:
            out.append(ch)
    s = "".join(out)
    s = restore_math(s, spans)
    # \path arguments must stay raw: strip escapes the generic escaper added
    res = []
    i = 0
    tok = BS + "path{"
    while True:
        j = s.find(tok, i)
        if j < 0:
            res.append(s[i:])
            break
        res.append(s[i:j])
        end = outer_brace(s, j + len(tok) - 1)
        inner = s[j + len(tok):end].replace(BS + "_", "_").replace(BS + "%", "%").replace(BS + "#", "#")
        res.append(tok + inner + "}")
        i = end + 1
    s = "".join(res)
    return s

def md_rows(block):
    rows = []
    for line in block.splitlines():
        if not line.strip().startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if all(re.fullmatch(r":?-{3,}:?", c) for c in cells):
            rows.append(None)  # separator
        else:
            rows.append(cells)
    return rows

# ---------------------------------------------------------------- parse MD
lines = md.splitlines()
out = []
stats = {"sec": 0, "sub": 0, "eq": 0, "tab": 0, "fig": 0, "warn": []}

i = 0
# --- title / abstract / keywords preamble ---
assert lines[0].startswith("# ")
paras = []           # collected LaTeX body chunks
mode = "head"

# skip to Abstract heading
i = lines.index("## Abstract")
abs_lines = []
kw_line = ""
i += 1
while i < len(lines) and not lines[i].startswith("## "):
    if lines[i].startswith("**Keywords:**"):
        kw_line = lines[i]
    elif lines[i].strip():
        abs_lines.append(lines[i].strip())
    i += 1
abstract = " ".join(abs_lines)
assert kw_line, "keywords line not found"
body_start = i

body = "\n".join(lines[body_start:])

# --- block pass over body ---
blocks = [b for b in body.split("\n\n") if b.strip()]
n_main_tables = 0
app_tables = {"Appendix A": "tab:appdataset", "Appendix B": "tab:apphyper", "Appendix C": "tab:lineage"}
cur_appendix = None
pending_app_caption = {}
pending_cap = None

# frozen appendix captions
for lbl in app_tables.values():
    hdr = tabhdr[lbl]
    cm = re.search(re.escape(BS + "caption{") + r"(.*?)" + re.escape("}") + r"\s*\n" + re.escape(BS + "label"), hdr, re.S)
    pending_app_caption[lbl] = cm.group(1)

tab_label_by_num = {1: "tab:composition", 2: "tab:benchmark", 3: "tab:mm",
    4: "tab:imbalance", 5: "tab:cv", 6: "tab:folds", 7: "tab:efficiency",
    8: "tab:earlyexit", 9: "tab:seeds", 10: "tab:modality"}

k = 0
while k < len(blocks):
    b = blocks[k]
    fst = b.lstrip()

    # ---- heading ----
    if fst.startswith("## "):
        h = fst[3:].strip()
        if h.startswith("Appendix "):
            letter = h.split()[1].rstrip(".")
            if letter == "A":
                out.append(BS + "appendix")
            title = h.split(". ", 1)[1] if ". " in h else h
            out.append(BS + "section{%s}%s" % (inline(title), BS + "label{app:" + letter + "}"))
            cur_appendix = "Appendix " + letter
            stats["sec"] += 1
        elif h in ("Data Availability", "Declarations"):
            out.append(BS + "section*{" + h + "}")
            cur_appendix = None
            stats["sec"] += 1
        elif h == "References":
            # bibliography is generated from references.bib; skip the MD's
            # numbered reference list entirely (it would duplicate the bib)
            break
        else:
            m = re.match(r"(\d+)\.\s+(.*)", h)
            title = m.group(2) if m else h
            out.append(BS + "section{%s}%s" % (inline(title), BS + "label{sec:%s}" % (m.group(1) if m else "x")))
            cur_appendix = None
            stats["sec"] += 1
        k += 1
        continue

    if fst.startswith("### "):
        h = fst[4:].strip()
        m = re.match(r"(\d+)\.(\d+)\s+(.*)", h)
        title = m.group(3) if m else h
        num = (m.group(1) + "." + m.group(2)) if m else "x"
        alias = ""
        if num == "6.1":
            alias = BS + "label{sec:preprocessing}"  # frozen fig.3 caption ref
        out.append(BS + "subsection{%s}%s%s" % (inline(title), BS + "label{sec:%s}" % num, alias))
        stats["sub"] += 1
        k += 1
        continue

    # ---- figure marker block: replace with frozen figure env ----
    if fst.startswith("[FIGURE"):
        fm = re.match(r"\[FIGURE (\d)", fst)
        n = int(fm.group(1))
        env = {1: "fig:architecture", 2: "fig:crossattention",
               3: "fig:preprocessing", 4: "fig:results"}[n]
        out.append(figenvs[env])
        stats["fig"] += 1
        # consume the spec block: subsequent meta paragraphs (any of the
        # author-edit variants: bold or plain Caption/Placement/Note/Source lines)
        spec_re = re.compile(r"^(\*\*)?\s*(Caption|Placement|Note|Notes|Data source|Source)\b")
        j = k + 1
        while j < len(blocks):
            nx = blocks[j].lstrip()
            if spec_re.match(nx) or "graphics are" in nx or nx.startswith("[FIGURE"):
                j += 1
            else:
                break
        k = j
        continue

    # ---- equation block ----
    em = re.match(r"\[Equation (\d+)\]\s*\n\s*\$\$(.*?)\$\$\s*$", b, re.S)
    eq_body = None
    if em:
        n = int(em.group(1))
        eq_body = em.group(2)
        k_next = k + 1
    elif re.fullmatch(r"\[Equation (\d+)\]", fst) and k + 1 < len(blocks):
        em2 = re.fullmatch(r"\$\$(.*?)\$\$\s*", blocks[k + 1].strip(), re.S)
        if em2:
            n = int(re.fullmatch(r"\[Equation (\d+)\]", fst).group(1))
            eq_body = em2.group(1)
            k_next = k + 2
    if eq_body is not None:
        body_eq = re.sub(re.escape(BS + "tag") + r"\{[^}]*\}", "", eq_body).strip()
        out.append(BS + "begin{equation}" + BS + "label{eq:%d}\n%s\n" % (n, body_eq) + BS + "end{equation}")
        stats["eq"] += 1
        k = k_next
        continue

    # ---- pending table caption (author-edit may separate caption from table) ----
    capm = re.match(r"\*\*Table (\d+)\.\s*(.*?)\*\*\s*$", fst, re.S)
    if capm and "|" not in b:
        pending_cap = (int(capm.group(1)), capm.group(2).replace("\n", " "))
        k += 1
        continue

    # ---- markdown table (+ attached *Source/*Note paragraphs) ----
    if fst.startswith("|"):
        rows = md_rows(b)
        note_blocks = []
        j = k + 1
        while j < len(blocks):
            nx = blocks[j].lstrip()
            if re.match(r"^\*(Source|Note)", nx):
                note_blocks.append(nx)
                j += 1
            else:
                break
        # locate caption: pending stash first, else nearest preceding block
        cap = None
        num = None
        if pending_cap is not None:
            num, cap = pending_cap
            pending_cap = None
        else:
            for kk in range(k - 1, max(-1, k - 4), -1):
                cm = re.match(r"\*\*Table (\d+)\.\s*(.*?)\*\*\s*$", blocks[kk].strip(), re.S)
                if cm:
                    cap = cm.group(2).replace("\n", " ")
                    num = int(cm.group(1))
                    break
        if cur_appendix:
            lbl = app_tables[cur_appendix]
            hdr = tabhdr[lbl]
            # appendix tables are placed inline ([H]) in their dedicated
            # sections: no float deferral, no drift into References
            assert BS + "begin{table}[h]" in hdr, lbl
            hdr = hdr.replace(BS + "begin{table}[h]", BS + "begin{table}[H]", 1)
            cap = pending_app_caption[lbl]
            cap = inline(re.sub(re.escape(BS + "code") + r"\{([^}]*)\}", r"`\1`", cap))
        else:
            lbl = tab_label_by_num[num]
            hdr = tabhdr[lbl]
        # replace caption text inside hdr by brace scanning
        ci = hdr.find(BS + "caption{")
        if ci >= 0:
            depth = 0
            for p in range(ci + len(BS + "caption{"), len(hdr)):
                if hdr[p] == "{":
                    depth += 1
                elif hdr[p] == "}":
                    if depth == 0:
                        end = p
                        break
                    depth -= 1
            hdr = hdr[:ci] + BS + "caption{" + cap + "}" + hdr[end + 1:]
        body_rows = []
        seen_sep = False
        for r in rows:
            if r is None:
                body_rows.append(BS + "midrule")
                seen_sep = True
                continue
            cells = [inline(c) for c in r]
            body_rows.append(" & ".join(cells) + " " + BS + BS)
        closer = BS + "end{tabular}"
        if lbl == "tab:lineage":
            closer += "}"  # closes the frozen \resizebox{\textwidth}{!}{ wrapper
        out.append(hdr + BS + "toprule\n" + "\n".join(body_rows) + "\n" + BS + "bottomrule\n" + closer)
        for nb in note_blocks:
            content = nb.strip()
            if content.startswith("*") and content.endswith("*") and not content.startswith("**"):
                content = content[1:-1]
            out.append("{\\footnotesize\\itshape " + inline(content) + "\\par}")
        out.append(BS + "end{table}")
        stats["tab"] += 1
        k = j
        continue

    # ---- lists ----
    # single glued block: "1. **A:** ... 2. **B:** ..." inside one paragraph
    if re.search(r"\S 1\. \*\*", fst) and re.search(r" 2\. \*\*", fst):
        parts = re.split(r"(?=\s\d\. \*\*)", fst.strip())
        parts = [p.strip() for p in parts if p.strip()]
        if len(parts) >= 4:
            chunks = [BS + "begin{enumerate}[leftmargin=*,itemsep=1.5pt]"]
            for p in parts:
                mm = re.match(r"(\d+)\.\s+(.*)", p)
                chunks.append(BS + "item[" + mm.group(1) + ".] " + inline(mm.group(2)))
            chunks.append(BS + "end{enumerate}")
            out.append("\n".join(chunks))
            stats["warn"].append("split glued enumerate (5.1)")
            k += 1
            continue

    if re.match(r"^(-|\d+\.)\s", fst) and "\n" in b or re.match(r"^(-|\d+\.)\s", fst):
        items = [l for l in b.splitlines() if l.strip()]
        numbered = items[0].lstrip().startswith(("1.", "2.", "3.", "4.", "5.", "6.", "7."))
        env = "enumerate" if numbered else "itemize"
        chunks = [BS + "begin{" + env + "}[leftmargin=*,itemsep=1.5pt]"]
        for it in items:
            it = it.strip()
            mnum = re.match(r"(\d+)\.\s+(.*)", it)
            if numbered and mnum:
                chunks.append(BS + "item[" + mnum.group(1) + ".] " + inline(mnum.group(2)))
            else:
                chunks.append(BS + "item " + inline(re.sub(r"^-\s+", "", it)))
        chunks.append(BS + "end{" + env + "}")
        out.append("\n".join(chunks))
        k += 1
        continue

    # ---- plain paragraph (may contain bold-led run-in headings) ----
    text = " ".join(l.strip() for l in b.splitlines())
    out.append(inline(text))
    k += 1

# ---------------------------------------------------------------- assemble
kw_text = inline(kw_line.replace("**Keywords:**", ""))
doc = []
doc.append(preamble)
doc.append("% --- tolerance for long artifact paths ----------------------------")
doc.append(BS + "emergencystretch=3em % raised 1.5->3em: absorbs final 4.2pt tokenizer-list overfull (production pass)")
doc.append("")
doc.append(title_block)
doc.append(BS + "begin{document}")
doc.append(BS + "maketitle")
doc.append(BS + "thispagestyle{fancy}")
doc.append("% ------------------------------- abstract ------" + "----------------------------")
doc.append(BS + "begin{abstract}")
doc.append(BS + "noindent")
doc.append(inline(abstract))
doc.append(BS + "end{abstract}")
doc.append("")
doc.append(BS + "vspace{2pt}")
doc.append(BS + "noindent{\\small " + kw_text + "}")
doc.append("")
doc.append("% ============================ body ============================")
doc.append("\n\n".join(out))
doc.append("")
# appendix tables are [H] inline: the float queue is always empty here, so the
# bibliography starts immediately after the last appendix material (no gaps).
doc.append(BS + "bibliographystyle{unsrtnat}")
doc.append(BS + "bibliography{references}")
doc.append(BS + "end{document}")

tex = "\n".join(doc) + "\n"
open(OUT, "w", encoding="utf-8", newline="\n").write(tex)

# ---------------------------------------------------------------- report
print("sections:", stats["sec"], "| subsections:", stats["sub"])
print("equations:", stats["eq"], "| tables:", stats["tab"], "| figures:", stats["fig"])
cites = set()
for m in re.finditer(re.escape(BS + "citep{") + r"([^}]*)\}", tex):
    cites.update(x.strip() for x in m.group(1).split(","))
print("distinct cite keys:", len(cites))
leftover = re.findall(r"\[\d{1,2}(?:,\s*\d{1,2})*\]", re.sub(r"\[Equation \d+\]|\[FIGURE \d", "", md))
print("leftover numeric brackets in MD (excl. eq/fig markers):", leftover[:10])
bad_cites = re.findall(re.escape(BS + "citep{") + r"([^}]*)\}", tex)
flat = []
for g in bad_cites:
    flat += [x.strip() for x in g.split(",")]
unknown = [x for x in flat if x not in bibkeys]
print("unknown cite keys:", unknown[:10])
eqs_out = len(re.findall(re.escape(BS + "begin{equation}"), tex))
tabs_out = len(re.findall(re.escape(BS + "begin{table}"), tex))
figs_out = len(re.findall(re.escape(BS + "begin{figure}"), tex))
assert eqs_out == stats["eq"] == 21, eqs_out
assert tabs_out == stats["tab"] == 13, tabs_out
assert figs_out == stats["fig"] == 4, figs_out
print("wrote", OUT, len(tex.splitlines()), "lines")
