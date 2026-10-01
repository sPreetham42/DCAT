import re

def fix_math():
    with open('paper/main.tex', 'r', encoding='utf-8') as f:
        text = f.read()

    bad_math = r'\textit{{$$\text{modality}(m) = \begin{cases} \text{MULTIMODAL} \& \text{if } has}text \wedge has\textit{image \\ \text{TEXT} \& \text{if } has}text \wedge \neg has\textit{image \\ \text{IMAGE} \& \text{if } \neg has}text \wedge has\_image \\ \text{EMPTY} \& \text{otherwise} \end{cases}$$}'
    
    good_math = r'$$\text{modality}(m) = \begin{cases} \text{MULTIMODAL} & \text{if } has\_text \wedge has\_image \\ \text{TEXT} & \text{if } has\_text \wedge \neg has\_image \\ \text{IMAGE} & \text{if } \neg has\_text \wedge has\_image \\ \text{EMPTY} & \text{otherwise} \end{cases}$$'
    
    if bad_math in text:
        text = text.replace(bad_math, good_math)
        print("Replaced bad cases block.")
    else:
        print("Warning: Bad math not found exactly. Trying regex.")
        # Try regex if exact match fails
        text = re.sub(r'\\textit\{\{\$\$\\text\{modality\}.*?\\end\{cases\}\$\$\}', good_math, text, flags=re.DOTALL)

    # Also replace \textit{{$(has}text, has_image)$}
    text = text.replace(r'\textit{{$(has}text, has_image)$}', r'$(has\_text, has\_image)$')
    text = text.replace(r'\textit{{$(has}text, has\_image)$}', r'$(has\_text, has\_image)$')
    
    with open('paper/main.tex', 'w', encoding='utf-8') as f:
        f.write(text)

if __name__ == '__main__':
    fix_math()
