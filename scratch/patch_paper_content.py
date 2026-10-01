import re
import json

def patch_paper_content():
    with open('paper/PAPER_CONTENT.md', 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Math Restoration Map
    math_reps = {
        r'_{$\hat{z}}i$}': r'$\hat{z}_i$',
        r'_{$t$0}': r'$m$',
        r'}{$t$1}': r' $t$',
        r'_{$t$2}': r'$y_i$',
        r'}{$t$3}': r' $w_{pos}$',
        r'_{$t$4}': r'$$\mathcal{L}_{weighted} = -\frac{1}{N} \sum_{i=1}^{N} \left[ w_{pos} \cdot y_i \log \sigma(\hat{z}_i) + (1 - y_i) \log(1 - \sigma(\hat{z}_i)) \right]$$',
        r'_{$t$5}': r'$w_{pos} = \frac{N_{ham}}{N_{spam}}$',
        r'_{$t$6}': r'$d_{model}$',
        r'_{$t$7}': r'$$\mathbf{H}_{text} = \text{DistilBERT}(\mathbf{x}_{text})$$',
        r'_{$t$8}': r'$\mathbf{x}_{text}$',
        r'}{$t$9}': r' $N_{text}$',
        
        r'_{$\mathbf{I} = \{I}1, I_{2, \ldots, I}K\}$0}': r'$\mathbf{M}_{text}$',
        r'_{$\mathbf{I} = \{I}1, I_{2, \ldots, I}K\}$1}': r'$B$',
        r'_{$\mathbf{I} = \{I}1, I_{2, \ldots, I}K\}$2}': r'$224 \times 224$',
        r'_{$\mathbf{I} = \{I}1, I_{2, \ldots, I}K\}$3}': r'$$\mathbf{H}_{img} = \text{MobileViT}(\mathbf{x}_{img})$$',
        r'_{$\mathbf{I} = \{I}1, I_{2, \ldots, I}K\}$4}': r'$\mathbf{x}_{img}$',
        r'_{$\mathbf{I} = \{I}1, I_{2, \ldots, I}K\}$5}': r'$N_{img}$',
        r'_{$\mathbf{I} = \{I}1, I_{2, \ldots, I}K\}$6}': r'$224 \times 224$',
        r'_{$\mathbf{I} = \{I}1, I_{2, \ldots, I}K\}$7}': r'$N_{img} = 49$',
        r'_{$\mathbf{I} = \{I}1, I_{2, \ldots, I}K\}$8}': r'$7 \times 7$',
        r'_{$\mathbf{I} = \{I}1, I_{2, \ldots, I}K\}$9}': r'$D_{img} = 256$',
        
        r'_{$y \in \{0, 1\}$0}': r'$d_{model}$',
        r'_{$y \in \{0, 1\}$1}': r'$$\mathbf{Z}_{text} = \text{LayerNorm}(\mathbf{H}_{text} \mathbf{W}_{text} + \mathbf{b}_{text})$$',
        r'_{$y \in \{0, 1\}$2}': r'$$\mathbf{Z}_{img} = \text{LayerNorm}(\mathbf{H}_{img} \mathbf{W}_{img} + \mathbf{b}_{img})$$',
        r'_{$y \in \{0, 1\}$3}': r'$\mathbf{W}_{text} \in \mathbb{R}^{768 \times d_{model}}$',
        r'}{$y \in \{0, 1\}$4}': r' $\mathbf{W}_{img} \in \mathbb{R}^{D_{img} \times d_{model}}$',
        r'_{$y \in \{0, 1\}$5}': r'$d_{model} = 256$',
        
        r'_{$y \in \{0, 1\}$6}': r'$L$',
        r'_{$y \in \{0, 1\}$7}': r'$$\mathbf{Q}_{text} = \mathbf{Z}_{text}\mathbf{W}_{Q,text}, \quad \mathbf{K}_{img} = \mathbf{Z}_{img}\mathbf{W}_{K,img}, \quad \mathbf{V}_{img} = \mathbf{Z}_{img}\mathbf{W}_{V,img}$$',
        
        r'_{$y \in \{0, 1\}$8}': r'$\mathbf{Z}_{img \to text}$',
        r'_{$y \in \{0, 1\}$9}': r'$$\mathbf{Z}_{img \to text} = \text{Softmax}\left(\frac{\mathbf{Q}_{text}\mathbf{K}_{img}^T}{\sqrt{d_k}}\right)\mathbf{V}_{img}$$',
        
        r'_{$y = 0$0}': r'$$\mathbf{Q}_{img} = \mathbf{Z}_{img}\mathbf{W}_{Q,img}, \quad \mathbf{K}_{text} = \mathbf{Z}_{text}\mathbf{W}_{K,text}, \quad \mathbf{V}_{text} = \mathbf{Z}_{text}\mathbf{W}_{V,text}$$',
        r'_{$y = 0$1}': r'$$\mathbf{Z}_{text \to img} = \text{Softmax}\left(\frac{\mathbf{Q}_{img}\mathbf{K}_{text}^T}{\sqrt{d_k}}\right)\mathbf{V}_{text}$$',
        
        r'_{$y = 0$3}': r'$$\mathbf{Z}_{text}^{out} = \mathbf{Z}_{text} + \text{MLP}(\mathbf{Z}_{img \to text})$$',
        r'_{$y = 0$4}': r'$$\mathbf{Z}_{img}^{out} = \mathbf{Z}_{img} + \text{MLP}(\mathbf{Z}_{text \to img})$$',
        r'_{$y = 0$5}': r'$\text{MLP}$',
        r'_{$y = 0$6}': r'$d_{model}$',
        r'_{$y = 0$7}': r'$$\mathbf{H}_{fused} = [\text{MeanPool}(\mathbf{Z}_{text}^{out}) \parallel \text{MeanPool}(\mathbf{Z}_{img}^{out})]$$',
        r'_{$y = 0$8}': r'$\parallel$',
        r'_{$y = 1$0}': r'$$\mathbf{H}_{unimodal} = \text{MeanPool}(\mathbf{Z}_{text})$$',
        r'_{$y = 1$2}': r'$$\mathbf{H}_{unimodal} = \text{MeanPool}(\mathbf{Z}_{img})$$',
        r'_{$y = 1$3}': r'$$p(y=1|m) = \sigma(\text{MLP}_{cls}(\mathbf{H}_{fused}))$$',
        r'_{$y = 1$5}': r'$$p(y=1|m) = \sigma(\text{MLP}_{cls}(\mathbf{H}_{unimodal}))$$',
        r'_{$y = 1$6}': r'$\sigma$',
        
        r'_{$(has}text, has\_image)$0}': r'$\mathbf{H}_{fused}$',
        r'_{$(has}text, has\_image)$1}': r'$\mathbf{H}_{unimodal}$',
        r'_{$(has}text, has\_image)$2}': r'$0.5$',
        r'_{$(has}text, has\_image)$3}': r'$\hat{y} = 1$ if $p(y=1|m) \ge 0.5$ else $0$',
        
        r'_{$(has}text, has\_image)$4}': r'$\text{MLP}_{aux}$',
        r'_{$(has}text, has\_image)$5}': r'$\mathbf{Z}_{text}$',
        r'_{$(has}text, has\_image)$6}': r'$$p_{aux}(y=1|t) = \sigma(\text{MLP}_{aux}(\text{MeanPool}(\mathbf{Z}_{text})))$$',

        r'_{$\mathcal{L} = -\frac{1}{N} \sum}': r'$$\mathcal{L} = -\frac{1}{N} \sum_{i=1}^{N} \left[ y_i \log \sigma(\hat{z}_i) + (1 - y_i) \log(1 - \sigma(\hat{z}_i)) \right]$$',
    }

    # Replace all math corruption
    for old, new in math_reps.items():
        content = content.replace(old, new)
        
    # Extra math fixes
    content = content.replace(r'$$i=1}^{N} \left[ y_{i \log \sigma(\hat{z}}i) + (1 - y_{i) \log(1 - \sigma(\hat{z}}i)) \right]$$', '')
    content = content.replace(r'^{N} \left[ y_{i \log \sigma(\hat{z}}i) + (1 - y_{i) \log(1 - \sigma(\hat{z}}i)) \right]$$', '')

    content = content.replace('_{$m$}', '$m$')
    content = content.replace('_{$t$}', '$t$')
    content = content.replace('_{$y = 0$}', '$y=0$')
    content = content.replace('_{$y = 1$}', '$y=1$')
    content = content.replace('_{$y \in \{0, 1\}$}', '$y \in \{0, 1\}$')
    content = content.replace(r'_{$\mathbf{I} = \{I_1, I_2, \ldots, I_K\}$}', r'$\mathbf{I} = \{I_1, I_2, \ldots, I_K\}$')

    # Remove conversion artifacts
    content = content.replace('_length = 256`, `truncation = longest_', 'length = 256`, `truncation = longest_first`')
    content = content.replace('*length*', 'length')
    content = content.replace('*longestf irst*', 'longest_first')
    content = content.replace('*timm*', 'timm')
    content = content.replace('*.eml*', '.eml')
    content = content.replace('\_', '_')
    
    # Update facts
    
    # 1. Dataset sizes
    content = content.replace('The SpamAssassin subset of the processed corpus contains 6,046 emails after preprocessing.', 
                              'The SpamAssassin subset of the processed corpus, used for primary evaluation, contains 6,046 emails after preprocessing.')
    
    # 2. Multimodal table description
    content = content.replace(
        'Table 11: Multimodal Cross-Validation Results',
        'Table 11: Multimodal Cross-Validation Results (Evaluated on a separate 7,867-sample multimodal OOF subset harvested from the full corpus)'
    )
    
    content = content.replace('The multimodal dataset is approximately balanced', 'The multimodal dataset is moderately imbalanced')
    content = content.replace('the utter absence of multimodal emails', 'the extreme scarcity of multimodal emails')

    # 3. Leakage Audit
    content = content.replace('We conducted a comprehensive dataset leakage audit to ensure no data contamination', 
                              'We conducted a preliminary dataset leakage audit on a toy subset to check for potential data contamination pipelines')
    content = content.replace('This guarantees that the model evaluation reflects true generalization',
                              'This provides an initial indication that the model evaluation reflects generalization')
    
    # 4. Model variants
    content = content.replace('Seven model variants were evaluated', 'Nine model variants were evaluated')
    
    # 5. Early exit
    content = content.replace('classified as spam via text', 'classified as spam or ham with high confidence (probability > 0.95 or < 0.05) based on text alone')
    content = content.replace('a negligible improvement', 'a slight per-sample latency improvement (2.70ms to 2.68ms)')
    content = content.replace('the total-time measurement (Table 9) shows a slight increase', 'the total-time batch measurement shows an increase (from 59.9ms to 74.7ms)')
    
    # Replace references to placeholders (no bold)
    content = content.replace('**[REFERENCE NEEDED]**', '[REFERENCE NEEDED]')

    with open('paper/PAPER_CONTENT.md', 'w', encoding='utf-8') as f:
        f.write(content)
        
    print("Patched PAPER_CONTENT.md successfully")

if __name__ == '__main__':
    patch_paper_content()
