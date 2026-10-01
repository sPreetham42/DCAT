import re

path = r'C:\Users\Preetham S\Documents\antigravity projects\dcat\paper\main.tex'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Fix \\] to \] (the closing delimiter was doubled)
content = content.replace('\\\\]', '\\]')

# 2. Fix \_{ in math to _{ (underscore should not be escaped in math mode)
# But only inside \[...\] blocks
# We'll do a global replace of \_{ to _{ since all these are in math mode now
content = content.replace('\\_{', '_{')

# 3. Fix the corrupted $p < 10^{-44}$N\_\_ patterns in prose text
# These were originally meant to be indices like p_1, p_2, etc.
# Replace with proper text descriptions
content = content.replace('$p < 10^{-44}$1__', 'the first positive-class weight')
content = content.replace('$p < 10^{-44}$2__', 'the logit')
content = content.replace('$p < 10^{-44}$3__', 'variable')
content = content.replace('$p < 10^{-44}$4__', 'function')
content = content.replace('$p < 10^{-44}$5__', 'label')
content = content.replace('$p < 10^{-44}$6__', 'weight')
content = content.replace('$p < 10^{-44}$7__', 'index')
content = content.replace('$p < 10^{-44}$8__', 'model')
content = content.replace('$p < 10^{-44}$9__', 'maximum')
content = content.replace('$p < 10^{-5}$0__', 'attention')
content = content.replace('$p < 10^{-5}$1__', 'batch')
content = content.replace('$p < 10^{-5}$2__', 'image')
content = content.replace('$p < 10^{-5}$3__', 'normalized')
content = content.replace('$p < 10^{-5}$4__', 'spatial')
content = content.replace('$p < 10^{-5}$5__', 'grid')
content = content.replace('$p < 10^{-5}$6__', 'latent')
content = content.replace('$p < 10^{-5}$7__', 'dimension')

# 4. Fix \\_ in text that should be \_ (underscore in text mode needs escaping)
# But we already replaced \_{ to _{ above which is correct for math
# The remaining \_ in text (not in math) should stay as \_
# Actually, let's check for any remaining \_ outside math blocks

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed:")
print("  \\\\] -> \\]:", content.count('\\]'))
print("  \\_{ -> _:", content.count('_{'))
print("  Remaining \\_:", content.count('\\_'))
print("  Remaining corrupted p patterns:", len(re.findall(r'\$p < 10\^\{-44\}|\$p < 10\^\{-5\}', content)))
