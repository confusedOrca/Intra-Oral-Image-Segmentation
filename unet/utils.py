import os
import torch
from dataset.dataset import IntraOralDataset
from torch.utils.data import DataLoader

root = os.path.abspath(os.path.join(os.getcwd(), os.pardir))

def save_checkpoint(state, filename):
    print("Saving checkpoint")
    torch.save(state, filename)
    
def load_checkpoint(checkpoint, model):
    print("loading checkpoint")
    model.load_state_dict(checkpoint["state_dict"])

def get_loaders(img_dir, mask_dir, batch_size, transform, num_workers=4, pin_memory=True):
    ds = IntraOralDataset(img_dir, mask_dir, transform)
    loader = DataLoader(ds, batch_size=batch_size, num_workers=num_workers, pin_memory=pin_memory, shuffle=True)
    return loader
    