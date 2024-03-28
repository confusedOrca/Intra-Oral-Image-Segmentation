import os
import sys
from torch.utils.data import ConcatDataset, DataLoader, Subset
from sklearn.model_selection import train_test_split
import albumentations as A
from albumentations.pytorch import ToTensorV2
import cv2

root = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
sys.path.append(root)

from dataset.dataset_class import IntraOralDataset

IMG_DIR = os.path.join(root, "Labelled intraoral smartphone images")
MASK_DIR = os.path.join(root, "masks_v1")

def get_data_loaders(train_transform=None, valid_transform=None, test_transform=None, 
                     batch_size=16, test_size=0.1, valid_size=0.1):
    # Lower jaw dataset
    l_img_dir = os.path.join(IMG_DIR, "Labels_Lower jaw")
    l_masks_dir = os.path.join(MASK_DIR, "lower")
    l_img_files = [dir for dir in os.listdir(l_img_dir) if not dir.endswith("json")]
    l_train_files, l_test_files = train_test_split(l_img_files, test_size=test_size, random_state=8)
    l_train_files, l_valid_files = train_test_split(l_train_files, test_size=valid_size/(1-test_size), random_state=8)

    l_train_indices = [l_img_files.index(filename) for filename in l_train_files]
    l_valid_indices = [l_img_files.index(filename) for filename in l_valid_files]
    l_test_indices = [l_img_files.index(filename) for filename in l_test_files]

    l_train_dataset = Subset(IntraOralDataset(l_img_dir, l_masks_dir, train_transform), l_train_indices)
    l_valid_dataset = Subset(IntraOralDataset(l_img_dir, l_masks_dir, valid_transform), l_valid_indices)
    l_test_dataset = Subset(IntraOralDataset(l_img_dir, l_masks_dir, test_transform), l_test_indices)

    # Upper jaw dataset
    u_img_dir = os.path.join(IMG_DIR, "Labels_Upper jaw")
    u_masks_dir = os.path.join(MASK_DIR, "upper")
    u_img_files = [dir for dir in os.listdir(u_img_dir) if not dir.endswith("json")]
    u_train_files, u_test_files = train_test_split(u_img_files, test_size=test_size, random_state=16)
    u_train_files, u_valid_files = train_test_split(u_train_files, test_size=valid_size, random_state=16)

    u_train_indices = [u_img_files.index(filename) for filename in u_train_files]
    u_valid_indices = [u_img_files.index(filename) for filename in u_valid_files]
    u_test_indices = [u_img_files.index(filename) for filename in u_test_files]

    u_train_dataset = Subset(IntraOralDataset(u_img_dir, u_masks_dir, train_transform), u_train_indices)
    u_valid_dataset = Subset(IntraOralDataset(u_img_dir, u_masks_dir, valid_transform), u_valid_indices)
    u_test_dataset = Subset(IntraOralDataset(u_img_dir, u_masks_dir, test_transform), u_test_indices)

    # Concatenating datasets
    train_dataset = ConcatDataset([l_train_dataset, u_train_dataset])
    valid_dataset = ConcatDataset([l_valid_dataset, u_valid_dataset])
    test_dataset = ConcatDataset([l_test_dataset, u_test_dataset])

    # Creating data loaders
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True, drop_last=False)
    valid_loader = DataLoader(valid_dataset, batch_size=batch_size, shuffle=False, drop_last=False)
    test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False, drop_last=False)

    return train_loader, valid_loader, test_loader
    
    
if __name__ == "__main__":
    transform = A.Compose(
        [
            A.LongestMaxSize(max_size=1024, always_apply=True),
            A.PadIfNeeded(min_height=1024, min_width=1024, border_mode=cv2.BORDER_CONSTANT, value=[0, 0, 0], always_apply=True),
            A.Normalize(mean=[0.0, 0.0, 0.0], std=[1.0, 1.0, 1.0], max_pixel_value=255.0),
            ToTensorV2(),
        ]
    )
    
    train_loader, valid_loader, test_loader = get_data_loaders(transform, transform, transform, 16)
    
    
    
    print(data.shape)
    print(labels.shape)
    
    total_examples = 0
    
    for batch in valid_loader:
        total_examples += batch[0].size(0)
    
    print(total_examples)