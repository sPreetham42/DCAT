# Multimodal Claim Power Assessment

## 1. Corpus Availability Constraints
- **Total Usable Corpus:** 73,206
- **Total Image-Bearing Ham in Corpus:** 327
- **Image-Bearing Ham in Original Pre-Registered Seed 42 Test:** 3
- **Projected Counts Under Group-Stratified Cross-Validation (K-Fold):** If we perform a 10-Fold Group-Stratified Cross-Validation, we will eventually evaluate all 327 image-bearing hams across the out-of-fold predictions. 
- **Projected Counts Under Group-Stratified Single Split:** If we force a single 10% test split via a constrained optimizer, we could theoretically guarantee $\approx 32$ image-bearing hams in the test split.

## 2. Statistical Implications
The central statistical test planned is McNemar's Test for marginal homogeneity (to detect if DCAT correctly flags image-bearing hams that the Text+ImagePresence baseline incorrectly flags as spam) and Bootstrap 95% Confidence Intervals for the Macro-F1 delta.

- **McNemar's Test Minimum:** The exact McNemar test operates on discordant pairs. With an $N$ of only 3 (under the original Seed 42 split), statistical significance ($p < 0.05$) is mathematically impossible to achieve.
- **Stratified Single Split ($N=32$):** A sample size of 32 provides severely limited statistical power. A massive, perfectly correlated effect size would be required to yield significance.
- **K-Fold Out-of-Fold Aggregate ($N=327$):** Aggregating the out-of-fold test predictions across a 10-Fold CV yields $N=327$. This provides sufficient statistical power to compute legitimate confidence intervals and McNemar statistics, assuming the effect size is moderate to large.

## 3. Recommended Wording of the Claim
Because the global available image-bearing ham population is only 327, we cannot definitively claim that DCAT has robust multimodal capabilities universally. 

**Revised Scientific Claim:** 
> "Within the constrained, leakage-controlled subset of image-bearing emails available in this corpus, does the integration of learned image pixels via cross-attention (DCAT) provide statistically significant discriminative power beyond text representations, binary image-presence indicators, and standard image metadata?"

This wording removes the implicit assumption that the model generalized perfectly to all multimodal data, bounding the claim to the available sample.
