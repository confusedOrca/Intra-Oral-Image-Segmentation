import os
import torch

root = os.path.abspath(os.path.join(os.getcwd(), os.pardir))

def save_checkpoint(state, directory, filename):
    os.makedirs(directory, exist_ok=True)
    filepath = os.path.join(directory, filename)
    print("Saving checkpoint to", filepath)
    torch.save(state, filepath)
    
def load_checkpoint(checkpoint_path, model):
    print("Loading checkpoint from", checkpoint_path)
    checkpoint = torch.load(checkpoint_path)
    model.load_state_dict(checkpoint["state_dict"])
    
def dice_score(prediction, target, smooth=1e-6):
    intersection = torch.sum(prediction * target, dim=(2, 3))
    union = torch.sum(prediction, dim=(2, 3)) + torch.sum(target, dim=(2, 3))
    dice = (2. * intersection + smooth) / (union + smooth)
    return dice.mean()