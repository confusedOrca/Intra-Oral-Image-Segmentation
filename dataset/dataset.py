import os
from PIL import Image
from torch.utils.data import Dataset
import numpy as np
from labels import labels


class IntraOralDataset(Dataset):
    def __init__(self, img_dir, mask_dir, transform=None):
        super().__init__()
        
        self.image_dir = img_dir
        self.mask_dirs = mask_dir
        self.transform = transform
        directories = os.listdir(img_dir)
        self.images = [dir for dir in directories if not dir.endswith("json")]
        
    def __len__(self):
        return len(self.images)
    
    def __getitem__(self, index):
        img_path = os.path.join(self.image_dir, self.images[index])
        mask_paths = [
            os.path.join(self.mask_dirs, label, self.images[index]) for label in labels
        ]
        
        image = np.array(Image.open(img_path).convert("RGB"))
        
        masks = []
        for mask_path in mask_paths:
            mask = np.array(Image.open(mask_path).convert("L"), dtype=np.float32)
            mask[mask == 255.0] = 1.0
            masks.append(mask)
        
        if self.transform is not None:
            augmentations = self.transform(image=image, masks=masks)
            image = augmentations["image"]
            masks = augmentations["masks"]
        
        masks = np.transpose(np.stack(masks, axis=-1), (2,0,1))
        
        return image, masks
        
         
        
