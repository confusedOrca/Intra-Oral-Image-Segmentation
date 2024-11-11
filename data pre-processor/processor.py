from utils import MODULE_DIR, BASE_DIR, list_examples
import aggregator
import os
from PIL import Image
import shutil
import config
from os.path import join
from concurrent.futures import ThreadPoolExecutor, as_completed

MAX_DIM = config.MAX_DIM
DESTINATION = join(BASE_DIR, config.DESTINATION, config.NAME)

def move_resized_image(dataset_path, dst_dir, name):
        img_src = os.path.join(dataset_path, name)
        img_dst = os.path.join(dst_dir, name)
        Image.open(img_src).resize((MAX_DIM, MAX_DIM)).save(img_dst)


def gen_yolo_label(text_dir, shapes, img_name):
    label_name = img_name.replace(".JPEG", ".txt")
    if(len(shapes) == 0):
        text_file_path = join(text_dir, label_name)
        with open(text_file_path, 'a+') as f:
            f.write(f"")
        return
        
    for i, shape in enumerate(shapes):
        line = ' '.join(map(str, shape))
        text_file_path = join(text_dir, label_name)
        with open(text_file_path, 'a+') as f:
            f.write(f"{line}\n")


def main():
    temp_dataset_path = aggregator.aggregate()
    img_dst = join(DESTINATION, "images")
    lbl_dst = join(DESTINATION, "labels")
    os.makedirs(img_dst, exist_ok=True)
    os.makedirs(lbl_dst, exist_ok=True)

    examples = list_examples(temp_dataset_path)

    with ThreadPoolExecutor() as executor:
        tasks = []

        for e in examples:
            tasks.append(executor.submit(move_resized_image, temp_dataset_path, img_dst, e.img))
            tasks.append(executor.submit(gen_yolo_label, lbl_dst, e.shapes, e.img))

        for future in as_completed(tasks):
            try:
                future.result()
            except Exception as exc:
                print(f"An error occurred: {exc}")

    shutil.rmtree(temp_dataset_path)
    print("Dataset preprocessing finished. Result is stored in: " + DESTINATION)

if __name__ == "__main__":
    main()
    