import os
import pandas as pd
import random
import config

def split_images(folder_path, valid_size, test_size, seed):
    random.seed(seed)
    all_files = [os.path.splitext(f)[0] for f in os.listdir(folder_path)]
    
    random.shuffle(all_files)
    total_images = len(all_files)
    train_size = total_images - valid_size - test_size
    train_images = all_files[:train_size]
    test_images = all_files[train_size:train_size + test_size]
    valid_images = all_files[train_size + test_size:]
    
    data = []
    for img in train_images:
        data.append({'example': img, 'split': 'train'})
    for img in valid_images:
        data.append({'example': img, 'split': 'val'})
    for img in test_images:
        data.append({'example': img, 'split': 'test'})
    
    df = pd.DataFrame(data)
    return df

if __name__ == "__main__":
    SEED = config.SEED
    DATASET_PATH = config.DATASET_IMG_PATH
    SAVE_PATH = config.SAVE_PATH
    VALID_SIZE = config.VALID_SIZE
    TEST_SIZE = config.TEST_SIZE

    df = split_images(DATASET_PATH, VALID_SIZE, TEST_SIZE, SEED)
    df.to_csv(SAVE_PATH, index=False)
    print(f"Dataframe saved to {SAVE_PATH}")
