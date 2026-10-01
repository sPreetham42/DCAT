# -*- coding: utf-8 -*-
import os, re, json, csv, statistics as st

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

def cat(rel): return open(os.path.join(ROOT, rel), encoding="utf-8", errors="ignore").read()

tex = cat("paper/main.tex")

def find(pattern, s):
    return re.findall(pattern, s)

# ---- figures ----
figs = re.findall(r"\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}", tex)
print("=== FIGURES in paper ===")
res_figs = []
for f in sorted(set(figs)):
    p = os.path.normpath(os.path.join("paper", f))
    ok = os.path.isfile(p)
    print(f"  {'OK ' if ok else 'MISS'} {f} -> {p}")
    res_figs.append((ok, f))

# ---- labels ----
labels = re.findall(r"\\label\{([^}]+)\}", tex)
used_labels = set(labels)
print("\n=== REFERENCED LABELS ===")
for l in sorted(used_labels):
    print("  ", l)

# cross-references to labels
refs = re.findall(r"\\ref\{([^}]+)\}", tex)
print("\n=== \\ref TARGETS ===")
for r in sorted(set(refs)):
    print("  ", r)

# ---- primary summary table vs results_summary.json ----
summary = json.loads(cat("artifacts/final_results/results_summary.json"))
by_model = {r["Model"]: r for r in summary["primary_benchmark"]}
print("\n=== PRIMARY TABLE vs results_summary.json ===")
checks = [
    ("Text-Only",    "Macro-F1", 0.9827),
    ("Text-Only",    "Spam-F1",  0.9895),
    ("Text-Only",    "Ham-F1",   0.9760),
    ("Image-Only",   "Macro-F1", 0.3220),
    ("Image-Only",   "Spam-F1",  0.1540),
    ("Image-Only",   "Ham-F1",   0.4901),
    ("Published-Baseline", "Macro-F1", 0.9869),
    ("Published-Baseline", "Spam-F1",  0.9920),
    ("Published-Baseline", "Ham-F1",   0.9818),
    ("Late-Fusion",  "Macro-F1", 0.9871),
    ("Late-Fusion",  "Spam-F1",  0.9921),
    ("Late-Fusion",  "Ham-F1",   0.9820),
    ("DCAT-No-Cross-Attention", "Macro-F1", 0.9867),
    ("DCAT-No-Cross-Attention", "Spam-F1",  0.9919),
    ("DCAT-No-Cross-Attention", "Ham-F1",   0.9815),
    ("Full-DCAT",    "Macro-F1", 0.9862),
    ("Full-DCAT",    "Spam-F1",  0.9916),
    ("Full-DCAT",    "Ham-F1",   0.9809),
    ("Full-DCAT",    "MM-Macro-F1", "0.6253"),
    ("DCAT-Early-Exit", "Macro-F1", 0.9867),
    ("DCAT-Early-Exit", "Spam-F1",  0.9919),
    ("DCAT-Early-Exit", "Ham-F1",   0.9814),
]
allkey_ok = True
for m, k, exp in checks:
    val = by_model.get(m, {}).get(k, "?")
    ok = (str(val) == str(exp))
    if not ok:
        allkey_ok = False
    print(f"  {'OK ' if ok else 'XX '} {m:28s} {k:12s} paper={exp}  artifact='{val}'")

# ---- primary CSV vs paper (Macro-F1 rounding) ----
with open(os.path.join(ROOT, "results/tables/final_results.csv")) as f:
    rows = {r["Model"]: r for r in csv.DictReader(f)}
print("\n=== PRIMARY CSV Macro-F1 vs paper ===")
mp = {
    "Text-Only": "Text-Only",
    "Image-Only": "Image-Only",
    "Published-Baseline": "Published-Baseline",
    "Late-Fusion": "Late-Fusion",
    "DCAT-No-Cross-Attention": "DCAT-No-Cross-Attention",
    "Full-DCAT": "Full-DCAT",
    "DCAT-Early-Exit": "DCAT-Early-Exit",
}
for k, mname in mp.items():
    r = rows.get(mname, {})
    mf1 = float(r.get("Macro-F1", 0))
    print(f"  {mname:28s} csv_raw={mf1:.6f}  round4={round(mf1,4):.4f}  (paper uses {round(mf1,4):.4f})")

# ---- multimodal CV table ----
cv = [r for r in csv.DictReader(open(os.path.join(ROOT, "artifacts/weighted_cv/cv_results.csv")))]
print("\n=== MM 5-FOLD CV: paper vs cv_results.csv ===")
for m in ["Full-DCAT", "Late-Fusion", "DCAT-No-XAttn", "Published-Baseline"]:
    vals = [float(r["macro_f1"]) for r in cv if r["model"] == m]
    if not vals:
        print(f"  {m}: no rows")
        continue
    mu, sd = st.mean(vals), st.pstdev(vals)
    print(f"  {m:20s} mean={mu:.4f} std={sd:.4f}  folds={vals}")

print("\n=== 95% CIs (paper uses LaTeX \pm 1.96*s/sqrt(5)) ===")
ci_paper = {
    "Late-Fusion": (0.4469, 0.6548),
    "Full-DCAT": (0.4936, 0.8947),
    "Weighted-DCAT": (0.5479, 0.8933),
}
for m,(plo, phi) in ci_paper.items():
    vals = [float(r["macro_f1"]) for r in cv if r["model"] == m]
    if not vals:
        print(f"  {m}: no rows")
        continue
    mu, sd = st.mean(vals), st.pstdev(vals)
    lo = mu - 1.96*sd/(5**0.5); hi = mu + 1.96*sd/(5**0.5)
    print(f"  {m:18s} paper=[{plo},{phi}]  recomputed=[{lo:.4f},{hi:.4f}]")

# ---- McNemar ----
print("\n=== McNEMAAR p-values ===")
print("  paper reports: 2.49e-45 (Weighted vs Full); 3.34e-06 (Weighted vs Late)")
print("  source: artifacts/final_results/results_lineage.csv")
ln = list(csv.DictReader(open(os.path.join(ROOT, "artifacts/final_results/results_lineage.csv"))))
for row in ln:
    if row["metric"].lower().startswith("mcnemar"):
        print("   lineage:", row)

# ---- efficiency ----
print("\n=== EFFICIENCY vs efficiency_summary.csv ===")
eff = list(csv.DictReader(open(os.path.join(ROOT, "artifacts/final_results/efficiency_summary.csv"))))
for r in eff:
    print(f"  {r['Model']:16s} lat={r['Avg Latency (s)']} p95={r['P95 Latency (s)']} skip={r['Vision Skip Rate (%)']} flop={r['Avg FLOPs (B)']} flop_red={r['FLOP Reduction (%)']} lat_red={r['Latency Reduction (%)']}")

# ---- efficiency_results.csv backup ----
effraw = list(csv.DictReader(open(os.path.join(ROOT, "results/tables/efficiency_results.csv"))))
print("\n=== efficiency_results.csv backup ===")
for r in effraw:
    print(f"  {r['Model']:18s} lat={r['Latency/sample (ms)']}", end="")
    print()

# ---- seed table ----
seedrows = list(csv.DictReader(open(os.path.join(ROOT, "results/tables/seed_summary.csv"))))
print("\n=== SEED TABLE ===")
for r in seedrows:
    print(f"  {r['Model']:20s} 42={r['Seed 42']} 43={r['Seed 43']} 44={r['Seed 44']} mean={r['Mean']}")

# ---- model_meta ----
with open(os.path.join(ROOT, "results/tables/experiment_metadata.csv")) as f:
    mrows = {r["Model"]: r for r in csv.DictReader(f)}
print("\n=== MODEL META (paper Table 4) vs experiment_metadata.csv ===")
for pname, mname in [("Text-only","Text-only"),("Image-only","Image-only"),("Late Fusion","Late Fusion"),("DCAT (no cross-attention)","DCAT-No-XAttn"),("DCAT (full)","DCAT")]:
    r = mrows.get(mname, {})
    print(f"  {pname:24s} total={r.get('Parameters')} trainable={r.get('Trainable Parameters')}")

# ---- dataset numbers (paper Table 1) ----
print("\n=== DATASET TABLE (paper) source check ===")
manifest = list(csv.DictReader(open(os.path.join(ROOT, "data/manifests/spamassassin_profile.csv"))))
labels_count = {}
mod_count = {}
for row in manifest:
    labels_count[row["label"]] = labels_count.get(row["label"], 0) + 1
    mod_count[row["modality"]] = mod_count.get(row["modality"], 0) + 1
print(f"  spamassassin_profile rows: {len(manifest)}")
print(f"  label dist: {labels_count}")
print(f"  modality dist: {mod_count}")
print("  note: paper dataset table draws from README + pipeline narrative; SpamAssassin profile is the public subset, not the full 75k corpus.")

# ---- leakage audit ----
print("\n=== LEAKAGE AUDIT (paper Table 12) source check ===")
import json as J
la = J.loads(cat("artifacts/leakage_audit/leakage_audit.json"))
for k,v in la.items():
    if isinstance(v, (dict, list)):
        print(f"  {k}: {str(v)[:200]}")
    else:
        print(f"  {k}: {v}")

print("\n=== ATTENTION: potential overclaim words ===")
suspect = ["prove","proves","proven","significantly outperforms","statistically significant improvement",
           "clearly superior","superior to","dominates","universally","always","never fails",
           "fully explains","perfect","flawless"]
for w in suspect:
    for m in re.finditer(re.escape(w), tex):
        print(f"  '{w}' at pos {m.start()}: ...{tex[max(0,m.start()-60):m.end()+60]}...")
print("  (contextual 'statistically significant' is acceptable where paired tests are reported)")
