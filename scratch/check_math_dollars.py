import codecs
import re

with codecs.open('paper/main.tex', 'r', encoding='utf-8') as f:
    text = f.read()

text = re.sub(r'(?<!\\)%.*', '', text) # remove comments
text = re.sub(r'\\\$', '', text) # remove escaped dollars
text = re.sub(r'\\begin\{equation\}.*?\\end\{equation\}', '', text, flags=re.DOTALL)

double_dollars = len(re.findall(r'\$\$', text))
single_dollars = len(re.findall(r'(?<!\$)\$(?!\$)', text))

print(f'single dollars: {single_dollars}')
if single_dollars % 2 != 0:
    print('WARNING: Unbalanced single dollars!')
