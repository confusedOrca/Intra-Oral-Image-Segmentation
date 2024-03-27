import torch
import albumentations as A
from albumentations.pytorch import ToTensorV2
from tqdm import tqdm
import torch.nn as nn
import torch.optim as optim
from model import Unet
import cv2
from utils import save_checkpoint, load_checkpoint, get_loaders

LEARNING_RATE = 1e-4
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
BATCH_SIZE = 16
NUM_EPOCHS = 10
NUM_WORKERS = 2
IMAGE_HEIGHT = 256
IMAGE_WIDTH = 256
PIN_MEMORY = True
LOAD_MODEL = False
IMG_DIR = "C:\\Users\\Siam\Desktop\\CSE499A\\Intra-Oral-Image-Segmentation\\Labelled intraoral smartphone images\\Labels_Lower jaw"
MASK_DIR = "C:\\Users\\Siam\\Desktop\\CSE499A\\Intra-Oral-Image-Segmentation\\masks_v1\lower"

def train_fn(loader, model, optimizer, loss_fn, scaler):
    loop = tqdm(loader)
    
    for batch_idx, (data, targets) in enumerate(loop):
        data = data.to(device=DEVICE)
        targets = targets.to(device=DEVICE)
        
        with torch.cuda.amp.autocast():
            predictions = model(data)
            print(predictions.shape)
            print(targets.shape)
            loss = loss_fn(predictions, targets)
        
        optimizer.zero_grad()
        scaler.scale(loss).backward()
        scaler.step(optimizer)
        scaler.update()
        
        loop.set_postfix(loss=loss.item())
        

if __name__ == "__main__":
    transform = A.Compose(
        [
            A.LongestMaxSize(max_size=256),
            A.PadIfNeeded(min_height=256, min_width=256, border_mode=cv2.BORDER_CONSTANT, value=[0, 0, 0]),
            A.Resize(width=256, height=256, always_apply=True),
            A.Normalize(mean=[0.0, 0.0, 0.0], std=[1.0, 1.0, 1.0], max_pixel_value=255.0),
            ToTensorV2(),
        ]
    )
    
    model = Unet().to(DEVICE)
    loss_fn = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=LEARNING_RATE)
    
    train_loader = get_loaders(
        IMG_DIR,
        MASK_DIR,
        BATCH_SIZE,
        transform,
        NUM_WORKERS,
        PIN_MEMORY
    )
    
    scaler = torch.cuda.amp.GradScaler()
    for epoch in range(NUM_EPOCHS):
        train_fn(train_loader, model, optimizer, loss_fn, scaler)
        checkpoint = {
            "state_dict": model.state_dict(),
            "optimizer": optimizer.state_dict(),
        }
        save_checkpoint(checkpoint)