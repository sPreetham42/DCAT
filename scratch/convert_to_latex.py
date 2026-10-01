import re

def parse_markdown_to_latex(md_content, template_content):
    # Extract template preamble and bibliography if possible
    preamble = []
    for line in template_content.split('\n'):
        if r'\begin{document}' in line:
            preamble.append(line)
            break
        preamble.append(line)
    preamble = '\n'.join(preamble)
    
    # Extract title, authors, abstract from md
    title_match = re.search(r'# (.*?)\n', md_content)
    title = title_match.group(1) if title_match else "DCAT"
    
    abstract_match = re.search(r'## Abstract\n\n(.*?)\n\n\*\*Keywords:\*\* (.*?)\n', md_content, re.DOTALL)
    abstract = abstract_match.group(1).strip() if abstract_match else ""
    keywords = abstract_match.group(2).strip() if abstract_match else ""
    
    latex = preamble + "\n\n"
    latex += r"""%% ─── TITLE ──────────────────────────────────────────────────────────────────
\title{
    \textbf{""" + title + r"""}
}

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

%% ─── ABSTRACT ───────────────────────────────────────────────────────────────
\begin{abstract}
""" + abstract + r"""
\end{abstract}

\begin{IEEEkeywords}
""" + keywords + r"""
\end{IEEEkeywords}

"""
    
    # Hardcoded mapping of [REFERENCE NEEDED] indices (0-indexed in text sequence)
    # The list below represents what citation key to use for the i-th occurrence.
    # We mapped them manually based on the context.
    cit_map = [
        r'\textbf{[[REF_MISSING]]}', # 00: lure content
        r'\cite{ref2}', # 01: communication channel
        r'\cite{ref3}', # 02: joint text-image classification
        r'\textbf{[[REF_MISSING]]}', # 03: MMTD framework intro
        r'\textbf{[[REF_MISSING]]}', # 04: intermediate layer concatenation
        r'\textbf{[[REF_MISSING]]}', # 05: attention-based fusion
        r'\textbf{[[REF_MISSING]]}', # 06: gating mechanisms
        r'\cite{ref1}', # 07: SpamAssassin
        r'\textbf{[[REF_MISSING]]}', # 08: Naive Bayes
        r'\textbf{[[REF_MISSING]]}', # 09: SVM
        r'\textbf{[[REF_MISSING]]}', # 10: Random Forests
        r'\textbf{[[REF_MISSING]]}', # 11: character-level
        r'\textbf{[[REF_MISSING]]}', # 12: word-level
        r'\textbf{[[REF_MISSING]]}', # 13: LSTM
        r'\cite{ref7}', # 14: BERT
        r'\textbf{[[REF_MISSING]]}', # 15: RoBERTa
        r'\cite{ref4}', # 16: DistilBERT
        r'\cite{ref4}', # 17: DistilBERT again
        r'\cite{ref15}', # 18: visual text
        r'\textbf{[[REF_MISSING]]}', # 19: MMTD framework related work
        r'\cite{ref3}', # 20: MDL-SPAM
        r'\cite{ref3}', # 21: missing modality
        r'\textbf{[[REF_MISSING]]}', # 22: Attention-based multimodal fusion
        r'\textbf{[[REF_MISSING]]}', # 23: gating networks
        r'\textbf{[[REF_MISSING]]}', # 24: machine translation
        r'\cite{ref8}', # 25: ViLBERT
        r'\cite{ref9}', # 26: LXMERT
        r'\cite{ref10}', # 27: CLIP
        r'\cite{ref8}', # 28: ViLBERT co-attention
        r'\cite{ref16}', # 29: text classification early exit
        r'\cite{ref4}', # 30: DistilBERT-base-uncased
        r'\cite{ref5}', # 31: MobileViT-small
        r'\cite{ref6}', # 32: timm library
        r'\cite{ref12}', # 33: training stability
        r'\cite{ref1}', # 34: public email corpus
        r'\textbf{[[REF_MISSING]]}', # 35: MMTD archetype
        r'\cite{ref11}', # 36: McNemar test
    ]
    
    # Parse references from the markdown
    references = []
    ref_section = md_content.find('## References')
    if ref_section != -1:
        ref_lines = md_content[ref_section:].split('\n')
        for line in ref_lines:
            if re.match(r'^\d+\.\s+(.*)', line):
                ref = re.match(r'^\d+\.\s+(.*)', line).group(1)
                references.append(ref)
                
    body_start = md_content.find('## 1. Introduction')
    if body_start == -1:
        body_start = 0
    body = md_content[body_start:ref_section if ref_section != -1 else len(md_content)]
    
    lines = body.split('\n')
    out_lines = []
    i = 0
    ref_occurrence = 0
    
    table_counter = 1
    figure_counter = 1
    
    while i < len(lines):
        line = lines[i]
        
        # If this is an image line, process it specifically without running italic replacements on it
        if line.startswith('- `results/figures/'):
            path_match = re.search(r'`(results/figures/.*?)`:(.*)', line)
            if path_match:
                path_raw = path_match.group(1)
                # Fix path for LaTeX (must be relative to paper dir)
                path_raw = '../' + path_raw
                caption = path_match.group(2).strip()
                out_lines.append(r'\begin{figure}[htbp]')
                out_lines.append(r'\centering')
                out_lines.append(r'\includegraphics[width=\columnwidth]{' + path_raw + r'}')
                out_lines.append(r'\caption{' + caption + r'}')
                out_lines.append(r'\label{fig:' + str(figure_counter) + r'}')
                out_lines.append(r'\end{figure}')
                figure_counter += 1
                i += 1
                continue
                
        # If it's a [FIGURE:] line
        if line.startswith('[FIGURE:'):
            fig_name = line.replace('[FIGURE:', '').replace(']', '').strip()
            out_lines.append(r'\begin{figure}[htbp]')
            out_lines.append(r'\centering')
            out_lines.append(r'\caption{' + fig_name + r'}')
            out_lines.append(r'\label{fig:' + str(figure_counter) + r'}')
            out_lines.append(r'\end{figure}')
            figure_counter += 1
            i += 1
            continue

        # Tables
        if line.startswith('|') and i+1 < len(lines) and '---' in lines[i+1]:
            headers = [h.strip() for h in line.split('|')[1:-1]]
            
            # Check for preceding caption
            caption = ""
            for cap_i in range(len(out_lines)-1, max(0, len(out_lines)-5), -1):
                if out_lines[cap_i].startswith(r'\textbf{Table'):
                    caption = out_lines[cap_i].replace(r'\textbf{', '').replace('}', '').strip()
                    del out_lines[cap_i]
                    break
                    
            out_lines.append(r'\begin{table}[htbp]')
            out_lines.append(r'\centering')
            out_lines.append(r'\renewcommand{\arraystretch}{1.2}')
            if caption:
                # Remove "Table X: " from caption so latex auto numbers it
                caption = re.sub(r'^Table \d+:?\s*', '', caption)
                out_lines.append(r'\caption{' + caption + r'}')
            out_lines.append(r'\label{tab:' + str(table_counter) + r'}')
            
            align = 'c' * len(headers)
            out_lines.append(r'\begin{tabular}{' + align + '}')
            out_lines.append(r'\toprule')
            out_lines.append(' & '.join([h for h in headers]) + r' \\')
            out_lines.append(r'\midrule')
            i += 2
            while i < len(lines) and lines[i].startswith('|'):
                row = [c.strip() for c in lines[i].split('|')[1:-1]]
                row = [r.replace('%', r'\%').replace('&', r'\&').replace('_', r'\_') for r in row]
                out_lines.append(' & '.join(row) + r' \\')
                i += 1
            out_lines.append(r'\bottomrule')
            out_lines.append(r'\end{tabular}')
            out_lines.append(r'\end{table}')
            table_counter += 1
            continue
            
        # Replace Headings
        line = re.sub(r'^#### (.*?)$', r'\\subsubsection{\1}', line)
        line = re.sub(r'^### (.*?)$', r'\\subsection{\1}', line)
        line = re.sub(r'^## (.*?)$', r'\\section{\1}', line)
        
        # Replace Bold and Italic
        line = re.sub(r'\*\*(.*?)\*\*', r'\\textbf{\1}', line)
        # disabled italics
        
        # Replace percentages and ampersands
        line = line.replace('%', r'\%').replace('&', r'\&')
        
        # Replace dynamic Table/Figure cross references in text
        # Assumes they match exactly the numbers generated sequentially.
        line = re.sub(r'Table (\d+)', r'Table~\\ref{tab:\1}', line)
        line = re.sub(r'Figure (\d+)', r'Figure~\\ref{fig:\1}', line)
        
        # Replace [REFERENCE NEEDED]
        if '[REFERENCE NEEDED]' in line:
            line = line.replace('[REFERENCE NEEDED]', '{[REFERENCE NEEDED]}')
            ref_occurrence += line.count('{[REFERENCE NEEDED]}')
            
        line = line.replace('[[REF_MISSING]]', '[REFERENCE NEEDED]')
                
        # Equations
        if line.strip() == '$$' or (line.startswith('$$') and line.endswith('$$')):
            eq = line.replace('$$', '').strip()
            if not eq: # Multiline equation block
                out_lines.append(r'\begin{equation}')
                i += 1
                while i < len(lines) and lines[i].strip() != '$$':
                    out_lines.append(lines[i].strip())
                    i += 1
                out_lines.append(r'\end{equation}')
                i += 1
                continue
            else:
                out_lines.append(r'\begin{equation}')
                out_lines.append(eq)
                out_lines.append(r'\end{equation}')
                i += 1
                continue
                
        # Inline equations (we should not escape underscores inside math)
        parts = line.split('$')
        for j in range(0, len(parts), 2): # Text parts
            parts[j] = parts[j].replace('_', r'\_')
        line = '$'.join(parts)
        
        out_lines.append(line)
        i += 1
        
    latex += '\n'.join(out_lines)
    
    # Append bibliography
    latex += r"""
%% ═══════════════════════════════════════════════════════════════════════════
\begin{thebibliography}{00}
%% ═══════════════════════════════════════════════════════════════════════════

"""
    for i, ref in enumerate(references):
        ref = re.sub(r'(https?://[^\s]+)', r'\\url{\1}', ref)
        latex += r"\bibitem{ref" + str(i+1) + "}\n" + ref + "\n\n"
        
    latex += r"""\end{thebibliography}

\end{document}
"""
    return latex

if __name__ == "__main__":
    with open('paper/PAPER_CONTENT.md', 'r', encoding='utf-8') as f:
        md = f.read()
    with open('paper/template.tex', 'r', encoding='utf-8') as f:
        template = f.read()
        
    latex = parse_markdown_to_latex(md, template)
    
    with open('paper/main.tex', 'w', encoding='utf-8') as f:
        f.write(latex)
    print("Wrote paper/main.tex")
