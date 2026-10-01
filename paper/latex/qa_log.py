import re

log = open('build/main.log', encoding='utf-8', errors='replace').read()

BS = chr(92)  # single backslash, avoids all escaping ambiguity

events = re.findall(r'\[(\d+)[\s\]]|Overfull ' + BS + BS + r'hbox \(([\d.]+)pt too wide\)', log)
page = None
overs = []
for p, o in events:
    if p:
        page = int(p)
    elif o:
        overs.append((page, float(o)))

print("Overfull hbox events > 2pt (page, excess pt):")
for pg, pt in overs:
    if pt > 2:
        print(f"  page {pg}: {pt}pt")
print(f"total overfull={len(overs)}, worst={max((o for _, o in overs), default=0):.1f}pt")
n_under = len(re.findall('Underfull ' + BS + BS + r'[hv]box', log))
print("Underfull boxes:", n_under)
n_glyph = log.count('Missing character')
print("Missing characters:", n_glyph)
