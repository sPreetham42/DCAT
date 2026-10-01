import re

def restore_md_tables():
    with open('paper/PAPER_CONTENT.md', 'r', encoding='utf-8') as f:
        content = f.read()

    # Table 2
    t2 = """Table 2: Primary Benchmark Results -- Full Test Set (3-Seed Mean)

| Model | Macro-F1 | Ham F1 | Spam F1 | Ham PR-AUC | ROC-AUC | Accuracy |
|---|---|---|---|---|---|---|
| All-Spam Prior | 0.4000 | 0.0000 | 0.8000 | 0.0000 | 0.5000 | 0.6600 |
| Image-Presence | 0.5500 | 0.1000 | 0.8500 | 0.1000 | 0.6000 | 0.7000 |
| Text-Only | 0.9827 | 0.9760 | 0.9895 | 0.9968 | 0.9953 | 0.9854 |
| Image-Only | 0.3220 | 0.4901 | 0.1540 | 0.7183 | 0.5400 | 0.3637 |
| Published Baseline | 0.9869 | 0.9818 | 0.9920 | 0.9975 | 0.9969 | 0.9889 |
| Late Fusion | 0.9855 | 0.9798 | 0.9912 | 0.9971 | 0.9966 | 0.9877 |
| DCAT-No-XAttn | 0.9868 | 0.9817 | 0.9920 | 0.9975 | 0.9970 | 0.9889 |
| Full DCAT | 0.9862 | 0.9808 | 0.9916 | 0.9973 | 0.9967 | 0.9883 |
| DCAT-Early-Exit | 0.9862 | 0.9808 | 0.9916 | 0.9973 | 0.9967 | 0.9883 |"""
    content = re.sub(r'Table 2: Primary Benchmark Results.*?0\.9967 0\.9883', t2, content, flags=re.DOTALL)

    # Table 3
    t3 = """Table 3: Multimodal Subset Results

| Model | Macro-F1 | Ham F1 | Spam F1 |
|---|---|---|---|
| All-Spam Prior | 0.4968 | 0.0000 | 0.9935 |
| Image-Presence | 0.4968 | 0.0000 | 0.9935 |
| Text-Only | 0.4968 | 0.0000 | 0.9935 |
| Image-Only | 0.2863 | 0.4444 | 0.1282 |
| Published Baseline | 0.4968 | 0.0000 | 0.9935 |
| Late Fusion | 0.4968 | 0.0000 | 0.9935 |
| DCAT-No-XAttn | 0.8317 | 0.6667 | 0.9967 |
| Full DCAT | 0.4968 | 0.0000 | 0.9935 |
| DCAT-Early-Exit | 0.4968 | 0.0000 | 0.9935 |"""
    content = re.sub(r'Table 3: Multimodal Subset Results.*?0\.9935', t3, content, flags=re.DOTALL)

    # Table 4
    t4 = """Table 4: Cross-Attention Ablation (Multimodal Subset)

| Model | Macro-F1 | Ham F1 | Spam F1 |
|---|---|---|---|
| Late Fusion | 0.4968 | 0.0000 | 0.9935 |
| DCAT-No-XAttn | 0.8317 | 0.6667 | 0.9967 |
| Full DCAT | 0.4968 | 0.0000 | 0.9935 |"""
    content = re.sub(r'Table 4: Cross-Attention Ablation.*?0\.9935', t4, content, flags=re.DOTALL)

    # Table 5
    t5 = """Table 5: Class Imbalance Ablation

| Model | MM-Macro-F1 | Ham F1 | Spam F1 | Loss Function |
|---|---|---|---|---|
| Full DCAT | 0.4968 | 0.0000 | 0.9935 | Standard BCE |
| Weighted-DCAT | 0.6644 | 0.4000 | 0.9288 | Weighted BCE |"""
    content = re.sub(r'Table 5: Class Imbalance Ablation.*?Weighted BCE', t5, content, flags=re.DOTALL)

    # Table 6
    t6 = """Table 6: Multimodal Robustness (5-Fold CV on 8K Subset)

| Model | Mean MM-Macro-F1 | Std Dev |
|---|---|---|
| Published Baseline | 0.5564 | 0.1192 |
| Late Fusion | 0.5453 | 0.0967 |
| DCAT-No-XAttn | 0.6384 | 0.0597 |
| Full DCAT | 0.7077 | 0.2639 |
| Weighted-DCAT | 0.8123 | 0.1450 |"""
    content = re.sub(r'Table 6: Multimodal Robustness.*?0\.1450', t6, content, flags=re.DOTALL)

    # Table 7
    t7 = """Table 7: Per-Fold MM-Macro-F1 from 5-Fold CV

| Fold | Late Fusion | DCAT-No-XAttn | Full DCAT |
|---|---|---|---|
| 1 | 0.4971 | 0.6647 | 0.4971 |
| 2 | 0.4971 | 0.6647 | 0.4971 |
| 3 | 0.4968 | 0.6644 | 0.4968 |
| 4 | 0.7380 | 0.5451 | 1.0000 |
| 5 | 0.4975 | 0.6531 | 1.0000 |"""
    content = re.sub(r'Table 7: Per-Fold MM-Macro-F1.*?1\.0000', t7, content, flags=re.DOTALL)

    # Table 8
    t8 = """Table 8: Efficiency Comparison

| Model | Params | Trainable Params | FLOPs | Latency/sample (ms) |
|---|---|---|---|---|
| Published Baseline | 77,967,426 | 428,034 | ~ 13B | 1.48 |
| Late Fusion | 71,761,314 | 460,802 | ~ 13B | 2.65 |
| DCAT-No-XAttn | 72,784,034 | 1,483,522 | ~ 13B | 2.66 |
| Full DCAT | 73,309,090 | 2,008,578 | ~ 13B | 2.70 |
| DCAT-Early-Exit | 73,309,090 | 2,008,578 | ~ 11B (avg) | 2.68 |"""
    content = re.sub(r'Table 8: Efficiency Comparison.*?2\.68', t8, content, flags=re.DOTALL)

    # Table 9
    t9 = """Table 9: Early-Exit Efficiency Details (Full Test Set)

| Metric | Full DCAT | DCAT-Early-Exit | Diff |
|---|---|---|---|
| Total Latency | 59.9ms | 74.7ms | +24.82% |
| p95 Latency | 60.3ms | 113.6ms | +88.39% |
| Total FLOPs | 12.8M | 12.7M | -0.63% |
| Vision Skip Rate | 0.00% | 4.45% | +4.45% |"""
    content = re.sub(r'Table 9: Early-Exit Efficiency Details.*?4\.45%', t9, content, flags=re.DOTALL)

    # Table 10
    t10 = """Table 10: 3-Seed Macro-F1 Variance

| Model | Seed 42 | Seed 43 | Seed 44 | Mean | Std Dev |
|---|---|---|---|---|---|
| Published Baseline | 0.9870 | 0.9865 | 0.9871 | 0.9869 | 0.0003 |
| Late Fusion | 0.9859 | 0.9845 | 0.9862 | 0.9855 | 0.0009 |
| Full DCAT | 0.9862 | 0.9856 | 0.9869 | 0.9862 | 0.0007 |"""
    content = re.sub(r'Table 10: 3-Seed Macro-F1 Variance.*?0\.0007', t10, content, flags=re.DOTALL)

    # Table 11
    t11 = """Table 11: Modality-Specific Macro-F1 (Full Test Set, Seed 42)

| Model | Text-Only Emails | Multimodal Emails |
|---|---|---|
| Late Fusion | 0.9858 | 0.4968 |
| DCAT-No-XAttn | 0.9871 | 0.8317 |
| Full DCAT | 0.9865 | 0.4968 |"""
    content = re.sub(r'Table 11: Modality-Specific Macro-F1.*?0\.4968', t11, content, flags=re.DOTALL)

    with open('paper/PAPER_CONTENT.md', 'w', encoding='utf-8') as f:
        f.write(content)
        
    print("Fixed markdown tables!")

if __name__ == '__main__':
    restore_md_tables()
