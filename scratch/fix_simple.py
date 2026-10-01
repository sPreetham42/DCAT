import codecs
import re

with codecs.open('paper/main.tex', 'r', encoding='utf-8') as f:
    text = f.read()

# Fix table and double escape
text = text.replace(r'\\_', r'\_')
text = text.replace(r'\\%', r'\%')
text = text.replace(r'\\&', r'\&')
text = text.replace(r'\\#', r'\#')

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
        
        if not rows:
            continue
        out.extend([r'\begin{table*}[htbp]', r'\centering', r'\renewcommand{\arraystretch}{1.2}'])
        
        parsed_rows = []
        for r in rows:
            cells = [c.strip() for c in r.split('|')[1:-1]]
            esc_cells = []
            for c in cells:
                c = c.replace(r'\_', '_').replace(r'\%', '%').replace(r'\&', '&').replace(r'\#', '#')
                c = c.replace('%', r'\%').replace('&', r'\&').replace('_', r'\_').replace('#', r'\#')
                
                c = re.sub(r'(\d+(?:\.\d+)?)\s*[\u00D7]\s*10\^\{([^\}]+)\}', r'$\1 \\times 10^{\2}$', c)
                c = re.sub(r'(p < 10\^\{[^\}]+\})', r'$\1$', c)
                c = c.replace('\u00D7', r'$\times$')
                esc_cells.append(c)
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
        l = lines[i]
        l = re.sub(r'(\d+(?:\.\d+)?)\s*[\u00D7]\s*10\^\{([^\}]+)\}', r'$\1 \\times 10^{\2}$', l)
        l = re.sub(r'(p < 10\^\{[^\}]+\})', r'$\1$', l)
        l = l.replace('\u00D7', r'$\times$')
        
        l = re.sub(r'Table (\d+)', r'Table~\ref{tab:\1}', l)
        l = re.sub(r'Figure (\d+)', r'Figure~\ref{fig:\1}', l)
        l = re.sub(r'\\ref\{tab:(\d+)\}', r'\\ref{tab:\1}', l) 
        
        out.append(l)
        i += 1

text = '\n'.join(out)
text = text.replace(r'Table~\ref{tab:\ref{tab:', r'Table~\ref{tab:')
text = text.replace('\u03B1', r'$\alpha$')
text = re.sub(r'(?<!\\)\$\$\$', '$', text)
text = re.sub(r'(?<!\\)\$\$', '$', text)

with codecs.open('paper/main.tex', 'w', encoding='utf-8') as f:
    f.write(text)
