# Gate 0 Diagnostics Preregistration

This document explicitly pre-registers the rules for the trivial-signal audit before examining any new model evaluation scores, in accordance with the Phase 2 research protocol.

## Gate 0A: Image-Bearing Ham Count
- **Target:** There must be `>= 150` image-bearing ham examples in the group-disjoint test set.
- **Rule:** If the count is `< 150`, we must report this deficit immediately and document the severe limitations of the multimodal inference claim, rather than manufacturing synthetic samples or deleting data.

## Gate 0B: Conditioned Evaluation Population
- **Target Population:** For all multimodal evaluation tiers below, the test population is strictly limited to `has_image = constant` (i.e. emails containing at least one meaningful image).
- **Rationale:** If an email contains no image, a multimodal model collapses to a text model. By restricting the population to image-bearing emails, the simple presence of an image is controlled for, isolating the incremental value of the image's content.

## Gate 0C: The Trivial-Signal Ladder
The evaluation must compute the F1-Score (and report incremental gains + paired significance testing) in the following strict order, comparing each rung to the preceding rung:
1. **Rung 1: Image-presence Baseline (Baseline probability of spam given an image)**
2. **Rung 2: Text-Only Model**
3. **Rung 3: Text + `has_image` Binary Feature**
4. **Rung 4: Image Metadata Model** (Using non-pixel features: image count, dimensions, size, mime-type)
5. **Rung 5: Image-Only Pixel Model**
6. **Rung 6: Late-Fusion Model**
7. **Rung 7: Full DCAT**

## Gate 0D: Incremental Decision Threshold
A model (e.g. Full DCAT) is only scientifically determined to be "meaningfully improving" over a lower rung (e.g. Late-Fusion) if and only if:
1. The numeric Macro-F1 score is higher.
2. The paired bootstrap confidence interval for the difference excludes zero.
3. The McNemar test (or bootstrap test) yields a statistically significant difference at $\alpha = 0.05$.

Absolute metrics alone without confidence bounds will NOT be accepted as proof of mechanism.


## Final Evaluation Split Characteristics
- **Final Seed Used:** 43
- **Gate 0A Result:** The group-disjoint Test split contains exactly **185** image-bearing ham emails. This meets the >= 150 requirement, allowing for statistically powered multimodal evaluation.
