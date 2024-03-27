import os
import torch
from torch.utils.data import Dataset, ConcatDataset, DataLoader, Subset
from dataset import IntraOralDataset
import numpy as np
from sklearn.model_selection import train_test_split
import albumentations as A
from albumentations.pytorch import ToTensorV2
import cv2


root = os.path.abspath(os.path.join(os.getcwd(), os.pardir))

IMG_DIR = os.path.join(root, "Labelled intraoral smartphone images")
MASK_DIR = os.path.join(root, "masks_v1")

def get_data_loaders(train_transformation=None, test_transformation=None, batch_size=16):
    lower_img_dir = os.path.join(IMG_DIR, "Labels_Lower jaw")
    lower_masks_dir = os.path.join(MASK_DIR, "lower")
    lower_img_files = [dir for dir in os.listdir(lower_img_dir) if not dir.endswith("json")]
    lower_train_files, lower_test_files = train_test_split(lower_img_files, test_size=0.2, random_state=16)

    lower_train_indices = [lower_img_files.index(filename) for filename in lower_train_files]
    lower_test_indices = [lower_img_files.index(filename) for filename in lower_test_files]

    lower_train_dataset = Subset(IntraOralDataset(lower_img_dir, lower_masks_dir, train_transformation), lower_train_indices)
    lower_test_dataset = Subset(IntraOralDataset(lower_img_dir, lower_masks_dir, test_transformation), lower_test_indices)

    upper_img_dir = os.path.join(IMG_DIR, "Labels_Upper jaw")
    upper_masks_dir = os.path.join(MASK_DIR, "upper")
    upper_img_files = [dir for dir in os.listdir(upper_img_dir) if not dir.endswith("json")]
    upper_train_files, upper_test_files = train_test_split(upper_img_files, test_size=0.2, random_state=16)

    upper_train_indices = [upper_img_files.index(filename) for filename in upper_train_files]
    upper_test_indices = [upper_img_files.index(filename) for filename in upper_test_files]

    upper_train_dataset = Subset(IntraOralDataset(upper_img_dir, upper_masks_dir, train_transformation), upper_train_indices)
    upper_test_dataset = Subset(IntraOralDataset(upper_img_dir, upper_masks_dir, test_transformation), upper_test_indices)

    train_dataset = ConcatDataset([lower_train_dataset, upper_train_dataset])
    test_dataset = ConcatDataset([lower_test_dataset, upper_test_dataset])

    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=True)

    return train_loader, test_loader
    
    
if __name__ == "__main__":
    transform = A.Compose(
        [
            A.LongestMaxSize(max_size=1024, always_apply=True),
            A.PadIfNeeded(min_height=1024, min_width=1024, border_mode=cv2.BORDER_CONSTANT, value=[0, 0, 0], always_apply=True),
            A.Normalize(mean=[0.0, 0.0, 0.0], std=[1.0, 1.0, 1.0], max_pixel_value=255.0),
            ToTensorV2(),
        ]
    )
    
    train_loader, test_loader = get_data_loaders(transform, transform, 8)
    
    data_iter = iter(test_loader)
    data, labels = next(data_iter)
    
    print(data.shape)
    print(labels.shape)