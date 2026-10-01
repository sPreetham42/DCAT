import re

def remediate_file(filepath, is_tex):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Fix Image-Spam Claim
    if is_tex:
        content = content.replace(
            "Features extracted from pre-trained CNNs (e.g., VGG, ResNet, MobileNet) can learn to recognize spam-specific patterns in images such as colors, shapes, and visual text~\\cite{ref15}.",
            "CNN-based methods have been successfully applied to the image spam detection task to recognize spam-specific patterns such as colors, shapes, and visual text~\\cite{ref15}. Pre-trained networks (e.g., VGG, ResNet, MobileNet) are commonly used as feature extractors for this purpose."
        )
    else:
        content = content.replace(
            "Features extracted from pre-trained CNNs (e.g., VGG, ResNet, MobileNet) can learn to recognize spam-specific patterns in images such as colors, shapes, and visual text~\\cite{ref15}.",
            "CNN-based methods have been successfully applied to the image spam detection task to recognize spam-specific patterns such as colors, shapes, and visual text~\\cite{ref15}. Pre-trained networks (e.g., VGG, ResNet, MobileNet) are commonly used as feature extractors for this purpose."
        )
    
    # 2. Fix attention-based and gating networks citation
    if is_tex:
        content = content.replace(
            "Prior multimodal studies have explored attention-based and gating-based fusion mechanisms~\\cite{ref13} that that allow the model",
            "Prior multimodal studies have explored attention-based and gating-based fusion mechanisms that allow the model"
        )
        content = content.replace(
            "Prior multimodal studies have explored attention-based and gating-based fusion mechanisms~\\cite{ref13} that allow the model",
            "Prior multimodal studies have explored attention-based and gating-based fusion mechanisms that allow the model"
        )
    else:
        content = content.replace(
            "Prior multimodal studies have explored attention-based and gating-based fusion mechanisms~\\cite{ref13} that that allow the model",
            "Prior multimodal studies have explored attention-based and gating-based fusion mechanisms that allow the model"
        )
        content = content.replace(
            "Prior multimodal studies have explored attention-based and gating-based fusion mechanisms~\\cite{ref13} that allow the model",
            "Prior multimodal studies have explored attention-based and gating-based fusion mechanisms that allow the model"
        )
    
    # 3. Remove unnecessary ref13 citations
    content = content.replace("than text~\\cite{ref13}.", "than text.")
    content = content.replace("accepted communication channel~\\cite{ref13}.", "accepted communication channel.")
    content = content.replace("joint text-image classification~\\cite{ref13}.", "joint text-image classification.")
    
    # 4. Fix MDL-SPAM metadata
    if is_tex:
        content = content.replace(
            "L. J. J et al.,",
            "J. J. Lohith, A. Purushotam, A. Mullangi, and A. Sharma,"
        )
    else:
        content = content.replace(
            "L. J. J et al.,",
            "J. J. Lohith, A. Purushotam, A. Mullangi, and A. Sharma,"
        )

    # 5. Remove unused ref2 and ref14 from bib (tex only)
    if is_tex:
        # ref2
        ref2_pattern = re.compile(r"\\bibitem\{ref2\}.*?(?=\\bibitem\{|\\end\{thebibliography\})", re.DOTALL)
        content = ref2_pattern.sub("", content)
        
        # ref14
        ref14_pattern = re.compile(r"\\bibitem\{ref14\}.*?(?=\\bibitem\{|\\end\{thebibliography\})", re.DOTALL)
        content = ref14_pattern.sub("", content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

remediate_file('paper/PAPER_CONTENT.md', False)
remediate_file('paper/main.tex', True)
print("Remediation complete.")
