# Split Diagnosis (Seed 42)

## 1. Corpus Imbalance
- Total usable corpus records: 73206
- Total image-bearing hams in corpus: 327 (0.45%)
- *Diagnosis:* The raw corpus suffers from extreme natural imbalance. P(image | ham) is very low.

## 2. Group Packing Algorithm
- Number of unique connected-components (groups) containing image-bearing hams: 54
- *Diagnosis:* The 327 examples are distributed across 54 groups. 
- They are reasonably well-distributed. The failure of Seed 42 to balance them across the splits was purely due to the random 80/10/10 allocation lacking explicit stratification for the rare joint `label=0 & has_image=True` strata.

## 3. Seed 42 Allocation
- Train: 317 (96.9%)
- Val: 7 (2.1%)
- Test: 3 (0.9%)

*Diagnosis:* The lack of joint label/modality stratification caused Seed 42 to randomly assign the vast majority (317) to the training set, leaving only 3 for testing. Because of group indivisibility and the rarity of the class, random splitting is mathematically incapable of guaranteeing a 10% balanced test yield.

## 4. Largest Contributing Groups
- **Group 544:** Total Size = 200, Image-Bearing Hams = 180
- **Group 685:** Total Size = 60, Image-Bearing Hams = 60
- **Group 628:** Total Size = 36, Image-Bearing Hams = 36
- **Group 2039:** Total Size = 2, Image-Bearing Hams = 1
- **Group 16482:** Total Size = 1, Image-Bearing Hams = 1
