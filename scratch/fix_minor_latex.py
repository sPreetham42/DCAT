import sys

def fix_minor_latex():
    with open('paper/main.tex', 'r', encoding='utf-8') as f:
        tex = f.read()

    tex = tex.replace(r'w\_spam = N}{\text{ham}} / N_{\text{spam}}$', r'$w_{spam} = N_{ham} / N_{spam}$')
    tex = tex.replace('≤', r'$\le$')
    tex = tex.replace('×', r'$\times$')

    with open('paper/main.tex', 'w', encoding='utf-8') as f:
        f.write(tex)
    print("Done")

if __name__ == '__main__':
    fix_minor_latex()
