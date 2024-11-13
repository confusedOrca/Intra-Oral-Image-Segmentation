import shutil
from os import listdir, remove, getcwd
from os.path import join, exists
import cv2
import config
from file_reader import read_txt_file
from mask_generator import generate_mask
from concurrent.futures import ThreadPoolExecutor, as_completed

CWD = getcwd()
SRC = join(CWD, config.SRC)
DST = join(CWD, config.DST)
NAME = config.NAME

def process_file(file_name, folder_path):
    file_path = join(folder_path, file_name)
    
    data = read_txt_file(file_path)
    mask = generate_mask(data)
    
    mask_file_name = file_name.replace('.txt', '.png')
    mask_file_path = join(folder_path, mask_file_name)
    cv2.imwrite(mask_file_path, mask)
    
    remove(file_path)


def process_files_parallel(folder_path):
    futures = []
    
    with ThreadPoolExecutor() as executor:
        for file_name in listdir(folder_path):
            if file_name.endswith('.txt'):
                futures.append(executor.submit(process_file, file_name, folder_path))
        
        for future in as_completed(futures):
            future.result()
            
            
def copy_src_to_dst(src, dst, name):
    dst_path = join(dst, name)
    if exists(dst_path):
        shutil.rmtree(dst_path)
    
    shutil.copytree(src, dst_path)
    return dst_path


def main():
    dst_path = copy_src_to_dst(SRC, DST, NAME)
    labels_folder = join(dst_path, config.LABELS)
    process_files_parallel(labels_folder)
    print(f"Generated masks in {labels_folder}")


if __name__ == "__main__":
    main()
