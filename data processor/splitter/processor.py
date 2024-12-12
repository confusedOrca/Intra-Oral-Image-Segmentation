import os
import shutil
import csv
from concurrent.futures import ThreadPoolExecutor
from config import SRC, DST, SAMPLING_CSV

def clear_and_create_folder(folder_path):
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)
    os.makedirs(folder_path)

def process_example(row, src_images, src_labels, dst_images, dst_labels):
    example = row['example']
    split = row['split']

    jaw, number = example.split(' (')
    number = number.rstrip(')')

    jaw_val = 'u' if jaw == 'intraoral_upper' else 'l'
    new_name = f"{jaw_val}_{number}"

    image_src = os.path.join(src_images, f"{example}.JPEG")
    label_src = os.path.join(src_labels, f"{example}.txt")

    image_dst = os.path.join(dst_images, split, f"{new_name}.JPEG")
    label_dst = os.path.join(dst_labels, split, f"{new_name}.txt")

    if os.path.exists(image_src) and os.path.exists(label_src):
        shutil.copy(image_src, image_dst)
        shutil.copy(label_src, label_dst)
    else:
        print(f"Warning: Missing files for example: {image_src}")

def main():
    src_images = os.path.join(SRC, 'images')
    src_labels = os.path.join(SRC, 'labels')

    clear_and_create_folder(DST)
    dst_images = os.path.join(DST, 'images')
    dst_labels = os.path.join(DST, 'labels')

    for split in ['train', 'val', 'test']:
        os.makedirs(os.path.join(dst_images, split))
        os.makedirs(os.path.join(dst_labels, split))

    with open(SAMPLING_CSV, 'r') as file:
        reader = csv.DictReader(file)
        rows = list(reader)

    with ThreadPoolExecutor() as executor:
        for row in rows:
            executor.submit(process_example, row, src_images, src_labels, dst_images, dst_labels)

if __name__ == "__main__":
    main()
