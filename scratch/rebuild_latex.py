import re
import os

def convert(md_path, template_path, out_path):
    with open(md_path, 'r', encoding='utf-8') as f:
        md = f.read()
    with open(template_path, 'r', encoding='utf-8') as f:
        template = f.read()

    preamble = []
    for line in template.split('\n'):
        if r'\begin{document}' in line:
            preamble.append(line)
            break
        preamble.append(line)
    preamble = '\n'.join(preamble)

    title_block = r"""%% ─── TITLE ──────────────────────────────────────────────────────────────────
\title{\textbf{DCAT: Dynamic Cross-Attention Transformer for Conditional Multimodal Email Spam Detection}}

%% ─── AUTHORS ────────────────────────────────────────────────────────────────
\author{
    \IEEEauthorblockN{Preetham S}
    \IEEEauthorblockA{
        Department of Information Science and Engineering \\
        Dayananda Sagar College of Engineering, Bengaluru -- 560078, India \\
        preetham.s@dsce.edu.in
    }
    \and
    \IEEEauthorblockN{Guide:}
    \IEEEauthorblockA{
        Department of Information Science and Engineering \\
        Dayananda Sagar College of Engineering, Bengaluru -- 560078, India \\
        
    }
}
\maketitle
"""
    
    abstract_match = re.search(r'## Abstract\n\n(.*?)\n\n\*\*Keywords:\*\*(.*?)\n', md, re.DOTALL)
    if not abstract_match:
        abstract_match = re.search(r'## Abstract\n\n(.*?)\n\n\*\*', md, re.DOTALL)
        keywords = "Spam Detection, Multimodal, Cross-Attention, Early Exit"
    else:
        keywords = abstract_match.group(2).strip()
    abstract = abstract_match.group(1).strip()
    
    abstract = re.sub(r'(p < 10\^\{[^\}]+\})', r'$\1$', abstract)
    abstract = re.sub(r'(\d+(?:\.\d+)?) [×x] 10\^\{([^\}]+)\}', r'$\1 \\times 10^{\2}$', abstract)
    abstract = abstract.replace('%', r'\%')
    
    abstract_block = r"""%% ─── ABSTRACT ───────────────────────────────────────────────────────────────
\begin{abstract}
""" + abstract + r"""
\end{abstract}
\begin{IEEEkeywords}
""" + keywords + r"""
\end{IEEEkeywords}
"""

    latex = preamble + "\n\n" + title_block + abstract_block + "\n"

    ref_section = md.find('## References')
    body = md[md.find('## 1. Introduction'):ref_section if ref_section != -1 else len(md)]
    
    references = []
    if ref_section != -1:
        for line in md[ref_section:].split('\n'):
            if re.match(r'^\d+\.\s+(.*)', line):
                references.append(re.match(r'^\d+\.\s+(.*)', line).group(1))

    tokens = {}
    counter = 0

    def repl_math_block(m):
        nonlocal counter
        k = f"XQXMATHBLOCK{counter}XQX"
        tokens[k] = m.group(1)
        counter += 1
        return k

    def repl_inline_math(m):
        nonlocal counter
        k = f"XQXINLINEMATH{counter}XQX"
        tokens[k] = m.group(1)
        counter += 1
        return k

    body = re.sub(r'(\$\$.*?\$\$)', repl_math_block, body, flags=re.DOTALL)
    body = re.sub(r'(\$[^\n\$]+?\$)', repl_inline_math, body)

    body = re.sub(r'(\d+(?:\.\d+)?) [×x] 10\^\{([^\}]+)\}', r'$\1 \\times 10^{\2}$', body)
    body = re.sub(r'(p < 10\^\{[^\}]+\})', r'$\1$', body)

    lines = body.split('\n')
    out_lines = []
    i = 0
    fig_num = 1
    
    while i < len(lines):
        line = lines[i]
        
        # Check if it's a captioned table
        tbl_match = re.match(r'^Table (\d+): (.*)', line)
        if tbl_match:
            label = tbl_match.group(1)
            caption = tbl_match.group(2).strip()
            i += 1
            # Skip empty lines immediately following
            while i < len(lines) and not lines[i].strip():
                i += 1
            
            rows = []
            while i < len(lines) and lines[i].strip():
                if not lines[i].startswith('|---'):
                    rows.append(lines[i].strip())
                i += 1
            
            out_lines.extend([
                r'\begin{table*}[htbp]' if (len(rows) > 0 and len(rows[0]) > 80) else r'\begin{table}[htbp]',
                r'\centering',
                r'\renewcommand{\arraystretch}{1.2}',
                r'\caption{' + caption + r'}',
                r'\label{tab:' + label + r'}'
            ])
            
            if rows:
                processed_rows = []
                for r in rows:
                    if r.startswith('|'):
                        cells = [c.strip() for c in r.split('|')[1:-1]]
                    else:
                        cells = [c.strip() for c in re.split(r'\s{2,}|\t', r)]
                        if len(cells) == 1 and ' ' in cells[0]:
                            cells = cells[0].split()
                    
                    esc_cells = [c.replace('%', r'\%').replace('&', r'\&').replace('_', r'\_').replace('#', r'\#') for c in cells]
                    processed_rows.append(' & '.join(esc_cells) + r' \\')
                
                cols = processed_rows[0].count('&') + 1
                out_lines.extend([
                    r'\begin{tabular}{' + 'c' * cols + '}',
                    r'\toprule',
                    processed_rows[0],
                    r'\midrule'
                ])
                for pr in processed_rows[1:]:
                    out_lines.append(pr)
                out_lines.extend([
                    r'\bottomrule',
                    r'\end{tabular}'
                ])
            out_lines.append(r'\end{table*}' if (len(rows) > 0 and len(rows[0]) > 80) else r'\end{table}')
            continue

        # Check if it's an uncaptioned table
        if line.startswith('|') and i+1 < len(lines) and lines[i+1].startswith('|---'):
            rows = []
            while i < len(lines) and lines[i].startswith('|'):
                if not lines[i].startswith('|---'):
                    rows.append(lines[i].strip())
                i += 1
                
            out_lines.extend([
                r'\begin{table*}[htbp]' if len(rows[0]) > 80 else r'\begin{table}[htbp]',
                r'\centering',
                r'\renewcommand{\arraystretch}{1.2}'
            ])
            processed_rows = []
            for r in rows:
                cells = [c.strip() for c in r.split('|')[1:-1]]
                esc_cells = [c.replace('%', r'\%').replace('&', r'\&').replace('_', r'\_').replace('#', r'\#') for c in cells]
                processed_rows.append(' & '.join(esc_cells) + r' \\')
            
            cols = processed_rows[0].count('&') + 1
            out_lines.extend([
                r'\begin{tabular}{' + 'c' * cols + '}',
                r'\toprule',
                processed_rows[0],
                r'\midrule'
            ])
            for pr in processed_rows[1:]:
                out_lines.append(pr)
            out_lines.extend([
                r'\bottomrule',
                r'\end{tabular}',
                r'\end{table*}' if len(rows[0]) > 80 else r'\end{table}'
            ])
            continue

        # Figures
        if line.startswith('- `results/figures/'):
            path_match = re.search(r'`(results/figures/.*?)`:(.*)', line)
            if path_match:
                path_raw = path_match.group(1)
                caption = path_match.group(2).strip()
                label = str(fig_num)
                for back in range(1, 4):
                    if i >= back and lines[i-back].startswith('Figure '):
                        fig_m = re.match(r'^Figure (\d+):', lines[i-back])
                        if fig_m:
                            label = fig_m.group(1)
                            for idx in range(len(out_lines)-1, max(0, len(out_lines)-4), -1):
                                if out_lines[idx].startswith('Figure ' + label):
                                    del out_lines[idx]
                                    break
                            break
                            
                out_lines.extend([
                    r'\begin{figure}[htbp]',
                    r'\centering',
                    r'\includegraphics[width=\columnwidth]{' + path_raw + r'}',
                    r'\caption{' + caption + r'}',
                    r'\label{fig:' + label + r'}',
                    r'\end{figure}'
                ])
                fig_num += 1
                i += 1
                continue
                
        # Headings
        if line.startswith('#### '):
            out_lines.append(r'\subsubsection*{' + line[5:].strip() + r'}')
        elif line.startswith('### '):
            out_lines.append(r'\subsection{' + line[4:].strip() + r'}')
        elif line.startswith('## '):
            out_lines.append(r'\section{' + line[3:].strip() + r'}')
        else:
            l = line
            if not l.startswith('Figure '):
                l = l.replace('_', r'\_').replace('#', r'\#')
            
            l = re.sub(r'\*\*(.*?)\*\*', r'\\textbf{\1}', l)
            l = re.sub(r'`(.*?)`', r'\\texttt{\1}', l)
            l = re.sub(r'Table (\d+)', r'Table~\\ref{tab:\1}', l)
            l = re.sub(r'Figure (\d+)', r'Figure~\\ref{fig:\1}', l)
            
            if l.startswith('Figure ') and l.endswith(':'):
                l = ''
                
            if l:
                out_lines.append(l)
            
        i += 1

    res = '\n'.join(out_lines)
    for k, v in tokens.items():
        if k.startswith('XQXMATHBLOCK'):
            eq = v.strip().strip('$').strip()
            res = res.replace(k, f"\\begin{{equation}}\n{eq}\n\\end{{equation}}")
        else:
            res = res.replace(k, v)
            
    latex += res

    latex += r"""
%% ═══════════════════════════════════════════════════════════════════════════
\begin{thebibliography}{00}
%% ═══════════════════════════════════════════════════════════════════════════

"""
    for j, ref in enumerate(references):
        ref = re.sub(r'(https?://[^\s]+)', r'\\url{\1}', ref)
        latex += r"\bibitem{ref" + str(j+1) + "}\n" + ref + "\n\n"
        
    latex += r"""\end{thebibliography}
\end{document}
"""
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(latex)

convert('paper/PAPER_CONTENT.md', 'paper/template.tex', 'paper/main.tex')
