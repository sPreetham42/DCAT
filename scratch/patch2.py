import re

with open('paper/main.tex', 'r', encoding='utf-8') as f:
    text = f.read()

lines = text.split('\n')
out = []
i = 0
while i < len(lines):
    if lines[i].startswith('|'):
        rows = []
        while i < len(lines) and lines[i].startswith('|'):
            if not lines[i].startswith('|---'):
                rows.append(lines[i])
            i += 1
        
        # Convert rows
        if not rows:
            continue
        out.extend([r'\begin{table*}[htbp]', r'\centering', r'\renewcommand{\arraystretch}{1.2}'])
        
        parsed_rows = []
        for r in rows:
            cells = [c.strip() for c in r.split('|')[1:-1]]
            esc_cells = [c.replace('%', r'\%').replace('&', r'\&').replace('_', r'\_').replace('#', r'\#') for c in cells]
            parsed_rows.append(' & '.join(esc_cells) + r' \\')
            
        cols = parsed_rows[0].count('&') + 1
        out.append(r'\begin{tabular}{' + 'c'*cols + '}')
        out.append(r'\toprule')
        out.append(parsed_rows[0])
        out.append(r'\midrule')
        for pr in parsed_rows[1:]:
            out.append(pr)
        out.append(r'\bottomrule')
        out.append(r'\end{tabular}')
        out.append(r'\end{table*}')
    else:
        # replace any remaining x character or p < 10^
        l = lines[i]
        # unicode '' might actually be 0xFFFD if reading failed, but we read utf-8.
        # Let's replace any char that looks like a multiplication sign
        l = re.sub(r'(\d+(?:\.\d+)?)\s*[×\u00D7\u2715\u22C5\ufffd]\s*10\^\{([^\}]+)\}', r'$\1 \\times 10^{\2}$', l)
        l = re.sub(r'(p < 10\^\{[^\}]+\})', r'$\1$', l)
        # Any naked '×'
        l = l.replace('×', r'$\times$').replace('\u00D7', r'$\times$').replace('\ufffd', r'$\times$')
        
        # Also replace undefined references if they are hardcoded
        l = re.sub(r'Table (\d+)', r'Table~\ref{tab:\1}', l)
        l = re.sub(r'Figure (\d+)', r'Figure~\ref{fig:\1}', l)
        l = re.sub(r'\\ref\{tab:(\d+)\}', r'\\ref{tab:\1}', l) # prevent double escape
        
        out.append(l)
        i += 1

text = '\n'.join(out)

# Prevent issues with double \ref
text = text.replace(r'Table~\ref{tab:\ref{tab:', r'Table~\ref{tab:')

with open('paper/main.tex', 'w', encoding='utf-8') as f:
    f.write(text)
