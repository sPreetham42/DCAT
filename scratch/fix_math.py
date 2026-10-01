import re

def fix_math(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Fix unicode
    content = content.replace("≤", "$\\leq$")
    content = content.replace("≥", "$\\geq$")
    content = content.replace("~4\\times", "$\\sim 4\\times$")
    content = content.replace("p < 10^{-44}", "$p < 10^{-44}$")
    content = content.replace("p < 10^{-20}", "$p < 10^{-20}$")
    content = content.replace("1 \\times^{-4}$", "$1 \\times 10^{-4}$")
    content = content.replace("2.49 \\times^{-45}$", "$2.49 \\times 10^{-45}$")
    content = content.replace("3.34 \\times^{-6}$", "$3.34 \\times 10^{-6}$")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

fix_math('paper/PAPER_CONTENT.md')
fix_math('paper/main.tex')
print("Math fix complete.")
