import re
with open('paper/main.tex', 'r', encoding='utf-8') as f:
    text = f.read()

def fix_table(match):
    lines = match.group(0).strip().split('\n')
    if len(lines) < 2: return match.group(0)
    out = [r'\begin{table*}[htbp]', r'\centering', r'\renewcommand{\arraystretch}{1.2}']
    
    rows = []
    for line in lines:
        if line.startswith('|---'): continue
        cells = [c.strip() for c in line.split('|')[1:-1]]
        esc_cells = [c.replace('%', r'\%').replace('&', r'\&').replace('_', r'\_').replace('#', r'\#') for c in cells]
        rows.append(' & '.join(esc_cells) + r' \\')
    
    if not rows: return match.group(0)
    
    cols = rows[0].count('&') + 1
    out.append(r'\begin{tabular}{' + 'c'*cols + '}')
    out.append(r'\toprule')
    out.append(rows[0])
    out.append(r'\midrule')
    for r in rows[1:]: out.append(r)
    out.append(r'\bottomrule')
    out.append(r'\end{tabular}')
    out.append(r'\end{table*}')
    return '\n'.join(out) + '\n'

text = re.sub(r'(?:^\|.*\|\s*$\n)+', fix_table, text, flags=re.MULTILINE)

# The unicode times character might be present. Let's find it by character code just to be safe
# \u00D7 is the multiplication sign
text = re.sub(r'(\d+(?:\.\d+)?)\s*\u00D7\s*10\^\{([^\}]+)\}', r'$\1 \\times 10^{\2}$', text)
text = re.sub(r'(p < 10\^\{[^\}]+\})', r'$\1$', text)
text = text.replace('\u00D7', r'$\times$')

# Check if there are any `Table ??` manually inserted in the text if we missed \ref
text = re.sub(r'Table (\d+)', r'Table~\ref{tab:\1}', text)
text = re.sub(r'Figure (\d+)', r'Figure~\ref{fig:\1}', text)

# Prevent escaping inside \ref
text = re.sub(r'\\ref\{tab:(\d+)\}', r'\\ref{tab:\1}', text)

with open('paper/main.tex', 'w', encoding='utf-8') as f:
    f.write(text)
