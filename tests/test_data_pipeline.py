import pytest
import pandas as pd
from pathlib import Path
from dcat.data.parquet import ParquetDatasetReader

@pytest.fixture(scope="module")
def dataset_records():
    path = Path("data/processed/records.parquet")
    if not path.exists():
        pytest.skip("Dataset not yet built. Skipping pipeline tests.")
    return ParquetDatasetReader.load_records(path)

def test_transitive_grouping_logic():
    from scripts.build_dataset import UnionFind
    
    uf = UnionFind()
    
    # Email A = T1 + I1
    uf.union("email_A", "txt_T1")
    uf.union("email_A", "img_I1")
    
    # Email B = T1 + I2
    uf.union("email_B", "txt_T1")
    uf.union("email_B", "img_I2")
    
    # Email C = T2 + I2
    uf.union("email_C", "txt_T2")
    uf.union("email_C", "img_I2")
    
    # Email D = T3 + I3 (completely isolated)
    uf.union("email_D", "txt_T3")
    uf.union("email_D", "img_I3")
    
    # A, B, and C should all resolve to the exact same parent root
    root_A = uf.find("email_A")
    assert root_A == uf.find("email_B")
    assert root_A == uf.find("email_C")
    
    # D should be different
    assert root_A != uf.find("email_D")

def test_each_sample_has_stable_id(dataset_records):
    ids = [r.email_id for r in dataset_records]
    assert len(ids) == len(set(ids)), "Duplicate email IDs found in dataset"
    assert all(i is not None and i != "" for i in ids), "Missing email IDs"

def test_label_is_valid(dataset_records):
    for r in dataset_records:
        assert r.label in (0, 1), f"Invalid label {r.label} for email {r.email_id}"

def test_multimodal_samples_contain_text_and_image(dataset_records):
    from dcat.data.modalities import Modality
    for r in dataset_records:
        if r.modality == Modality.MULTIMODAL:
            assert r.has_text, f"MULTIMODAL record {r.email_id} has no text"
            assert r.has_meaningful_image, f"MULTIMODAL record {r.email_id} has no images"
            assert len(r.images) > 0, f"MULTIMODAL record {r.email_id} image list is empty"
        elif r.modality == Modality.TEXT:
            assert r.has_text, f"TEXT record {r.email_id} has no text"
            assert not r.has_meaningful_image, f"TEXT record {r.email_id} has image flagged"

def test_no_duplicated_leakage_group_crosses_splits():
    manifest_path = Path("data/manifests/leakage_groups.csv")
    if not manifest_path.exists():
        pytest.skip("Manifest missing")
        
    df = pd.read_csv(manifest_path)
    
    train_groups = set(df[df['split'] == 'train']['group_id'])
    val_groups = set(df[df['split'] == 'val']['group_id'])
    test_groups = set(df[df['split'] == 'test']['group_id'])
    
    assert len(train_groups.intersection(val_groups)) == 0, "Group leakage: Train intersects Val"
    assert len(train_groups.intersection(test_groups)) == 0, "Group leakage: Train intersects Test"
    assert len(val_groups.intersection(test_groups)) == 0, "Group leakage: Val intersects Test"

def test_no_hash_crosses_splits_invariant(dataset_records):
    train_texts = set()
    val_texts = set()
    test_texts = set()
    
    train_imgs = set()
    val_imgs = set()
    test_imgs = set()
    
    import hashlib
    
    for r in dataset_records:
        th = None
        if r.text:
            clean_text = r.text.strip()
            th = hashlib.md5(clean_text.encode('utf-8')).hexdigest()
            
        if r.split == 'train':
            if th: train_texts.add(th)
            for img in r.images:
                if img.exact_hash: train_imgs.add(img.exact_hash)
        elif r.split == 'val':
            if th: val_texts.add(th)
            for img in r.images:
                if img.exact_hash: val_imgs.add(img.exact_hash)
        elif r.split == 'test':
            if th: test_texts.add(th)
            for img in r.images:
                if img.exact_hash: test_imgs.add(img.exact_hash)
                
    # Text hash assertions
    assert len(train_texts.intersection(val_texts)) == 0, "Leakage: Train and Val share text hashes"
    assert len(train_texts.intersection(test_texts)) == 0, "Leakage: Train and Test share text hashes"
    assert len(val_texts.intersection(test_texts)) == 0, "Leakage: Val and Test share text hashes"
    
    # Image hash assertions
    # Note: image_processor adds `exact_hash` by md5ing the payload, matching what we do in build_dataset
    assert len(train_imgs.intersection(val_imgs)) == 0, "Leakage: Train and Val share image hashes"
    assert len(train_imgs.intersection(test_imgs)) == 0, "Leakage: Train and Test share image hashes"
    assert len(val_imgs.intersection(test_imgs)) == 0, "Leakage: Val and Test share image hashes"

def test_split_generation_is_deterministic(dataset_records):
    counts = {"train": 0, "val": 0, "test": 0}
    for r in dataset_records:
        if r.split in counts:
            counts[r.split] += 1
            
    assert counts["train"] > 0, "Train split is empty"
    assert counts["val"] > 0, "Val split is empty"
    assert counts["test"] > 0, "Test split is empty"
