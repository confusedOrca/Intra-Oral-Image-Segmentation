from utils import move_images_and_labels, select_random_images
import shutil
import os

TEST_SIZE = 24
VAL_SIZE = 24
TRAIN_SIZE = 172 - TEST_SIZE - VAL_SIZE
SEED = 404

def main():
    src = "labelled_dataset"
    dst = "processed_dataset"
    temp_src = os.path.join(os.getcwd(), "temp")

    shutil.copytree(os.path.join(os.getcwd(), src), temp_src)
    
    test_images = select_random_images("temp", TEST_SIZE, SEED)
    move_images_and_labels("temp", dst, test_images, "test")
    
    valid_images = select_random_images("temp", VAL_SIZE, SEED)
    move_images_and_labels("temp", dst, valid_images, "val")
    
    train_images = select_random_images("temp", TRAIN_SIZE, SEED)
    move_images_and_labels("temp", dst, train_images, "train")
    
    shutil.rmtree(os.path.join(os.getcwd(), "temp"))
    

if __name__ == "__main__":
    main()