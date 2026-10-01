path = r'C:\Users\Preetham S\Documents\antigravity projects\dcat\paper\main.tex'
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Fix line 158 (index 157) - architecture overview
lines[157] = '3. Modality Projector: maps the two encoder outputs into a shared latent space of dimension $d_{model}$ using linear projections followed by Layer Normalization.\n'

# Fix line 168 (index 167) - tokenization
lines[167] = 'The tokenized input is truncated or padded to 256 tokens. $M$ denotes the corresponding attention mask, and $B$ denotes the batch size.\n'

# Fix line 170 (index 169) - vision encoder
lines[169] = 'The vision encoder uses MobileViT-small~\\cite{ref5}, accessed through the \\texttt{timm} library~\\cite{ref6}. Images are resized to $224 \\times 224$ pixels before encoding.\n'

# Fix line 175 (index 174) - vision encoder features
lines[174] = 'Here, $\\mathbf{H}_{img}$ represents the normalized image tensor. $N_{spatial}$ denotes the number of spatial tokens produced by the encoder. For the evaluated configuration, the feature map corresponds to a spatial grid. The vision encoder parameters are frozen during training.\n'

# Fix line 177 (index 176) - modality projector
lines[176] = 'The projector maps text and image features into a shared $d_{model}$-dimensional latent space:\n'

# Fix line 192 (index 191) - with d_model
if len(lines) > 191:
    if '{model}' in lines[191] or '10^{-5}' in lines[191]:
        lines[191] = 'with $d_{model}$.\n'

# Fix line 213 (index 212) - missing \\] closing
if len(lines) > 212:
    if '\\]' not in lines[212] and 'math{Z}' in lines[212]:
        lines[212] = lines[212].rstrip() + '\n\\]\n'

with open(path, 'w', encoding='utf-8') as f:
    f.writelines(lines)

print('Fixed lines directly')
