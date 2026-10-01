import codecs

with codecs.open('paper/PAPER_CONTENT.md', 'r', encoding='utf-8') as f:
    text = f.read()

replacements = {
    r'_{$(has_text, has_image)$}': r'$(has\_text, has\_image)$',
    r'_{$$\text{modality}(m) = \begin{cases} \text{MULTIMODAL} & \text{if } has_text \wedge has_image \\ \text{TEXT} & \text{if } has_text \wedge \neg has_image \\ \text{IMAGE} & \text{if } \neg has_text \wedge has_image \\ \text{EMPTY} & \text{otherwise} \end{cases}$$}': r'$$\text{modality}(m) = \begin{cases} \text{MULTIMODAL} & \text{if } has\_text \wedge has\_image \\ \text{TEXT} & \text{if } has\_text \wedge \neg has\_image \\ \text{IMAGE} & \text{if } \neg has\_text \wedge has\_image \\ \text{EMPTY} & \text{otherwise} \end{cases}$$',
    r'_{$$\mathcal{L} = -\frac{1}{N} \sum_{i=1}^{N} \left[ y_i \log \sigma(\hat{z}_i) + (1 - y_i) \log(1 - \sigma(\hat{z}_i)) \right]$$}': r'$$\mathcal{L} = -\frac{1}{N} \sum_{i=1}^{N} \left[ y_i \log \sigma(\hat{z}_i) + (1 - y_i) \log(1 - \sigma(\hat{z}_i)) \right]$$',
    r'_{$\hat{z}_i$}': r'$\hat{z}_i$',
    r'_{$t$1}': r'$\sigma$',
    r'_{$t$3}': r'$w_{pos}$',
    r'_{$t$9}': r'$N_{text}$',
    
    r'_{$\mathbf{I} = \{I_1, I_2, \ldots, I_K\}$0}': r'$\mathbf{M}_{text}$',
    r'_{$\mathbf{I} = \{I_1, I_2, \ldots, I_K\}$1}': r'$B$',
    r'_{$\mathbf{I} = \{I_1, I_2, \ldots, I_K\}$2}': r'$224 \times 224$',
    r'_{$\mathbf{I} = \{I_1, I_2, \ldots, I_K\}$3}': r'$$\mathbf{H}_{img} = \text{MobileViT}(\mathbf{x}_{img})$$',
    r'_{$\mathbf{I} = \{I_1, I_2, \ldots, I_K\}$4}': r'$\mathbf{x}_{img}$',
    r'_{$\mathbf{I} = \{I_1, I_2, \ldots, I_K\}$5}': r'$N_{img}$',
    r'_{$\mathbf{I} = \{I_1, I_2, \ldots, I_K\}$6}': r'$224 \times 224$',
    r'_{$\mathbf{I} = \{I_1, I_2, \ldots, I_K\}$7}': r'$N_{img} = 49$',
    r'_{$\mathbf{I} = \{I_1, I_2, \ldots, I_K\}$8}': r'$7 \times 7$',
    r'_{$\mathbf{I} = \{I_1, I_2, \ldots, I_K\}$9}': r'$D_{img} = 256$',
    
    r'_{$y \in \{0, 1\}$4}': r'$\mathbf{W}_{img} \in \mathbb{R}^{D_{img} \times d_{model}}$',
    
    r'$$\mathbf{Z}_{text \to img} = \text{Softmax}\left(\frac{\mathbf{Q}_{img}\mathbf{K}_{text}^T}{\sqrt{d_k}}\right)\mathbf{V}_{text}$$': r'$\mathbf{Q}_{text}$',
    r'_{$y = 0$2}': r'$\mathbf{K}_{img}, \mathbf{V}_{img}$',
    
    r'$\parallel$': r'$$\mathbf{Z}_{text}^{out} = \mathbf{Z}_{text} + \text{MLP}(\mathbf{Z}_{img \to text})$$',
    r'_{$y = 0$9}': r'$$\mathbf{Z}_{img}^{out} = \mathbf{Z}_{img} + \text{MLP}(\mathbf{Z}_{text \to img})$$',
    
    r'$$\mathbf{H}_{unimodal} = \text{MeanPool}(\mathbf{Z}_{text})$$': r'$h=8$',
    r'_{$y = 1$1}': r'$d_k = 32$',
    
    r'$$p(y=1|m) = \sigma(\text{MLP}_{cls}(\mathbf{H}_{fused}))$$': r'$\mathbf{M}_{text}$',
    r'_{$y = 1$4}': r'$i$',
    
    r'_{$y = 1$7}': r'$d_{model}$',
    
    r'_{$y = 1$8}': r'$d_{model}$',
    r'_{$y = 1$9}': r'$$p(y=1|m) = \sigma(\text{MLP}_{cls}(\mathbf{H}_{fused}))$$',
    
    r'_{$(has_text, has_image)$0}': r'1. The unimodal text representation is computed: $$\mathbf{H}_{unimodal} = \text{MeanPool}(\mathbf{Z}_{text})$$',
    r'_{$(has_text, has_image)$1}': r'',
    r'_{$(has_text, has_image)$2}': r'$$p_{aux}(y=1|t) = \sigma(\text{MLP}_{aux}(\mathbf{H}_{unimodal}))$$',
    r'_{$(has_text, has_image)$3}': r'$p_{aux} \ge 0.95$',
    r'_{$(has_text, has_image)$4}': r'$p_{aux} \le 0.05$',
    
    r'_{$(has_text, has_image)$5}': r'$1 \times 10^{-4}$',
    r'_{$(has_text, has_image)$6}': r'$\mathcal{L}$',
}

for k, v in replacements.items():
    text = text.replace(k, v)

with codecs.open('paper/PAPER_CONTENT.md', 'w', encoding='utf-8') as f:
    f.write(text)
