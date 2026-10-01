# Independent Split Verification

## Overlap Checks
- Train/Validation Overlap: 0
- Train/Test Overlap: 0
- Validation/Test Overlap: 0
- Cross-split Group Leakage: 0

## Record Counts
- Train: 55744
- Validation: 7303
- Test: 10159
- Total Usable: 73206

## Test Set Composition (Independent Audit)
- Total Test Examples: 10159
- Test Ham: 2488
- Test Spam: 7671

### Modality x Label
- Image-Bearing Ham: **3**
- Image-Bearing Spam: 865
- Text-Only Ham: 2485
- Text-Only Spam: 6806

### Image Nature
- Pure Image-Only: 156
- Multimodal (Text+Image): 712

*Note: Since the image-bearing ham count is likely strictly < 150 (since it was 3 under Seed 42 originally), the multimodal test power is severely limited and the Gate 0 claims MUST be narrowed. The scientific priority remains unbiased construction.*
