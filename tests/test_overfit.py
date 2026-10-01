import torch
from torch.utils.data import DataLoader, Dataset
from dcat.models.dcat.model import DcatModel
from dcat.data.modalities import Modality

class DummyDataset(Dataset):
    def __len__(self):
        return 4
    
    def __getitem__(self, idx):
        # Even idx is spam (1), odd is ham (0)
        label = 1 if idx % 2 == 0 else 0
        return {
            "email_id": str(idx),
            "modality": Modality.MULTIMODAL.value,
            "label": label,
            "input_ids": torch.randint(0, 1000, (32,)),
            "attention_mask": torch.ones(32,),
            "pixel_values": torch.randn(3, 224, 224)
        }

def test_model_overfits():
    torch.manual_seed(42)
    model = DcatModel(
        text_model_name="distilbert-base-uncased",
        vision_model_name="mobilevit_s",
        freeze_encoders=True,
        shared_dim=64,
        cross_attention_layers=1,
        cross_attention_heads=1
    )
    
    ds = DummyDataset()
    loader = DataLoader(ds, batch_size=4)
    
    optimizer = torch.optim.AdamW(model.parameters(), lr=1e-3)
    criterion = torch.nn.BCEWithLogitsLoss()
    
    batch = next(iter(loader))
    labels = batch["label"].float().unsqueeze(1)
    
    # Overfit to 1 batch
    initial_loss = 0
    final_loss = 0
    for epoch in range(15):
        optimizer.zero_grad()
        logits = model(batch)
        loss = criterion(logits, labels)
        loss.backward()
        optimizer.step()
        
        if epoch == 0:
            initial_loss = loss.item()
        if epoch == 14:
            final_loss = loss.item()
            
    assert final_loss < initial_loss
    assert final_loss < 0.1 # Should confidently overfit to near 0
