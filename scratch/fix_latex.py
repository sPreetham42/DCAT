import sys

def fix_latex():
    with open('paper/main.tex', 'r', encoding='utf-8') as f:
        tex = f.read()

    # The exact strings found in the file:
    reps = {
        r'\textit{{$$\mathcal{L} = -\frac{1}{N} \sum}{i=1}^{N} \left[ y\textit{i \log \sigma(\hat{z}}i) + (1 - y\textit{i) \log(1 - \sigma(\hat{z}}i)) \right]$$}':
        r'$$\mathcal{L} = -\frac{1}{N} \sum_{i=1}^{N} \left[ y_i \log \sigma(\hat{z}_i) + (1 - y_i) \log(1 - \sigma(\hat{z}_i)) \right]$$',

        r'\textit{{$\hat{z}}i$}': r'$\hat{z}_i$',
        r'\textit{{$t$0}': r'$m$',
        r'}{$t$1}': r' $t$',
        r'\textit{{$t$2}': r'$y_i$',
        r'}{$t$3}': r' $w_{pos}$',
        r'\_{$t$4}': r'$$\mathcal{L}_{weighted} = -\frac{1}{N} \sum_{i=1}^{N} \left[ w_{pos} \cdot y_i \log \sigma(\hat{z}_i) + (1 - y_i) \log(1 - \sigma(\hat{z}_i)) \right]$$',
        r'\_{$t$5}': r'$w_{pos} = \frac{N_{ham}}{N_{spam}}$',
        r'\_{$t$6}': r'$d_{model}$',
        r'\_{$t$7}': r'$$\mathbf{H}_{text} = \text{DistilBERT}(\mathbf{x}_{text})$$',
        r'\textit{{$t$8}': r'$\mathbf{x}_{text}$',
        r'}{$t$9}': r' $N_{text}$',
        
        r'\textit{{$\mathbf{I} = \{I}1, I\textit{2, \ldots, I}K\}$0}': r'$\mathbf{M}_{text}$',
        r'\textit{{$\mathbf{I} = \{I}1, I\textit{2, \ldots, I}K\}$1}': r'$B$',
        r'\textit{{$\mathbf{I} = \{I}1, I\textit{2, \ldots, I}K\}$2}': r'$224 \times 224$',
        r'\textit{{$\mathbf{I} = \{I}1, I\textit{2, \ldots, I}K\}$3}': r'$$\mathbf{H}_{img} = \text{MobileViT}(\mathbf{x}_{img})$$',
        r'\textit{{$\mathbf{I} = \{I}1, I\textit{2, \ldots, I}K\}$4}': r'$\mathbf{x}_{img}$',
        r'\textit{{$\mathbf{I} = \{I}1, I\textit{2, \ldots, I}K\}$5}': r'$N_{img}$',
        r'\textit{{$\mathbf{I} = \{I}1, I\textit{2, \ldots, I}K\}$6}': r'$224 \times 224$',
        r'\textit{{$\mathbf{I} = \{I}1, I\textit{2, \ldots, I}K\}$7}': r'$N_{img} = 49$',
        r'\textit{{$\mathbf{I} = \{I}1, I\textit{2, \ldots, I}K\}$8}': r'$7 \times 7$',
        r'\textit{{$\mathbf{I} = \{I}1, I\textit{2, \ldots, I}K\}$9}': r'$D_{img} = 256$',
        
        r'\_{$y \in \{0, 1\}$0}': r'$d_{model}$',
        r'\_{$y \in \{0, 1\}$1}': r'$$\mathbf{Z}_{text} = \text{LayerNorm}(\mathbf{H}_{text} \mathbf{W}_{text} + \mathbf{b}_{text})$$',
        r'\_{$y \in \{0, 1\}$2}': r'$$\mathbf{Z}_{img} = \text{LayerNorm}(\mathbf{H}_{img} \mathbf{W}_{img} + \mathbf{b}_{img})$$',
        r'\textit{{$y \in \{0, 1\}$3}': r'$\mathbf{W}_{text} \in \mathbb{R}^{768 \times d_{model}}$',
        r'}{$y \in \{0, 1\}$4}': r' $\mathbf{W}_{img} \in \mathbb{R}^{D_{img} \times d_{model}}$',
        r'\_{$y \in \{0, 1\}$5}': r'$d_{model} = 256$',
        
        r'\_{$y \in \{0, 1\}$6}': r'$L$',
        
        r'\_{$y = 0$0}': r'$$\mathbf{Q}_{text} = \mathbf{Z}_{text}\mathbf{W}_{Q,text}, \quad \mathbf{K}_{img} = \mathbf{Z}_{img}\mathbf{W}_{K,img}, \quad \mathbf{V}_{img} = \mathbf{Z}_{img}\mathbf{W}_{V,img}$$',
        r'\textit{{$y = 0$1}': r'$\mathbf{Z}_{img \to text}$',
        r'\_{$y = 0$3}': r'$$\mathbf{Z}_{img \to text} = \text{Softmax}\left(\frac{\mathbf{Q}_{text}\mathbf{K}_{img}^T}{\sqrt{d_k}}\right)\mathbf{V}_{img}$$',
        r'\_{$y = 0$4}': r'$$\mathbf{Q}_{img} = \mathbf{Z}_{img}\mathbf{W}_{Q,img}, \quad \mathbf{K}_{text} = \mathbf{Z}_{text}\mathbf{W}_{K,text}, \quad \mathbf{V}_{text} = \mathbf{Z}_{text}\mathbf{W}_{V,text}$$',
        r'\_{$y = 0$5}': r'$$\mathbf{Z}_{text \to img} = \text{Softmax}\left(\frac{\mathbf{Q}_{img}\mathbf{K}_{text}^T}{\sqrt{d_k}}\right)\mathbf{V}_{text}$$',
        r'\_{$y = 0$6}': r'$$\mathbf{Z}_{text}^{out} = \mathbf{Z}_{text} + \text{MLP}(\mathbf{Z}_{img \to text})$$',
        r'\_{$y = 0$7}': r'$$\mathbf{Z}_{img}^{out} = \mathbf{Z}_{img} + \text{MLP}(\mathbf{Z}_{text \to img})$$',
        r'\textit{{$y = 0$8}': r'$\text{MLP}$',
        r'\textit{{$y = 1$0}': r'$d_{model}$',
        r'\_{$y = 1$2}': r'$$\mathbf{H}_{fused} = [\text{MeanPool}(\mathbf{Z}_{text}^{out}) \parallel \text{MeanPool}(\mathbf{Z}_{img}^{out})]$$',
        r'\textit{{$y = 1$3}': r'$\parallel$',
        r'\_{$y = 1$5}': r'$$\mathbf{H}_{unimodal} = \text{MeanPool}(\mathbf{Z}_{text})$$',
        r'\_{$y = 1$6}': r'$$\mathbf{H}_{unimodal} = \text{MeanPool}(\mathbf{Z}_{img})$$',
        r'\_{$y = 1$7}': r'$$p(y=1|m) = \sigma(\text{MLP}_{cls}(\mathbf{H}_{fused}))$$',
        r'\_{$y = 1$8}': r'$$p(y=1|m) = \sigma(\text{MLP}_{cls}(\mathbf{H}_{unimodal}))$$',
        r'\_{$y = 1$9}': r'$\sigma$',
        
        r'\textit{{$(has\}text, has\_image)$0}': r'$\mathbf{H}_{fused}$',
        r'\textit{{$(has\}text, has\_image)$1}': r'$\mathbf{H}_{unimodal}$',
        r'\textit{{$(has\}text, has\_image)$2}': r'$0.5$',
        r'\textit{{$(has\}text, has\_image)$3}': r'$\hat{y} = 1$ if $p(y=1|m) \ge 0.5$ else $0$',
        
        r'\textit{{$(has\}text, has\_image)$4}': r'$\text{MLP}_{aux}$',
        r'\textit{{$(has\}text, has\_image)$5}': r'$\mathbf{Z}_{text}$',
        r'\textit{{$(has\}text, has\_image)$6}': r'$$p_{aux}(y=1|t) = \sigma(\text{MLP}_{aux}(\text{MeanPool}(\mathbf{Z}_{text})))$$',
        
        r'\textit{{\text{late}}': r'\_late',
        r'\textit{{\text{spam}}': r'\_spam',
        r'\textit{analysis/dcat}': r'\_analysis/dcat\_',
        r'\textit{analysis/late}': r'\_analysis/late\_',
        r'\textit{results}': r'\_results',
        r'\textit{results/primary}': r'\_results/primary\_',
        r'\textit{results/imbalance}': r'\_results/imbalance\_',
        r'\textit{results/multimodal}': r'\_results/multimodal\_',
        r'\textit{cv/cv}': r'\_cv/cv\_',
        r'\textit{results/efficiency}': r'\_results/efficiency\_',
        r'\textit{t + \mathbf{z}}': r'\_t + \mathbf{z}\_',
        r'\textit{RESULTS}': r'\_RESULTS',
        r'\textit{OF}': r'\_OF',
        r'\textit{results/results}': r'\_results/results\_',
        r'\textit{length = 256`, `truncation = longest}': r'_length = 256`, `truncation = longest_',
    }

    # Loop line by line to accurately patch without missing multi-line edges
    for old, new in reps.items():
        if old in tex:
            tex = tex.replace(old, new)
        else:
            print(f"Warning: Not found: {old}")
            
    with open('paper/main.tex', 'w', encoding='utf-8') as f:
        f.write(tex)
    print("Done")

if __name__ == '__main__':
    fix_latex()
