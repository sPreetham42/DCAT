import codecs
with codecs.open('paper/main.tex', 'r', encoding='utf-8') as f:
    text = f.read()

b = text.count(r'\begin{equation}')
e = text.count(r'\end{equation}')
print(f'begin: {b}, end: {e}')
