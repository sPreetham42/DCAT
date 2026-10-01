import re

log = open('build/main.log', encoding='utf-8', errors='replace').read()
BS = chr(92)
lines = log.splitlines()

page = 0
for i, ln in enumerate(lines):
    m = re.search(r'\[(\d+)[\s\]]', ln)
    if m:
        page = max(page, int(m.group(1)))
    if 'Overfull' in ln and 'hbox' in ln:
        pt = re.search(r'\(([\d.]+)pt', ln)
        ctx = ' | '.join(l.strip()[:70] for l in lines[i + 1:i + 4])
        print(f"p{page} [{pt.group(1) if pt else '?'}pt] {ctx}")
