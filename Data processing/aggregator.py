import os
import shutil

def move_contents(src, dst):
    for item in os.listdir(src):
        src_item = os.path.join(os.getcwd(), src, item)
        dst_item = os.path.join(os.getcwd(), dst, item)
        shutil.copy(src_item, dst_item)

if __name__ == "__main__":
    src1 = "dataset/Labels_Lower jaw"
    dst = "aggregated_dataset"
    move_contents(src1, dst)
    
    src2 = "dataset_v1.1/Labels_Upper jaw"
    move_contents(src2, dst)