from utils import MODULE_DIR, BASE_DIR, list_examples
import aggregator
from PIL import Image
import shutil
import config
from os import makedirs
from os.path import join
from concurrent.futures import ThreadPoolExecutor, as_completed

MAX_DIM = config.MAX_DIM
DESTINATION = join(BASE_DIR, config.DESTINATION, config.NAME)

def move_resized_image(dataset_path, dst_dir, name):
        img_src = join(dataset_path, name)
        img_dst = join(dst_dir, name)
        Image.open(img_src).resize((MAX_DIM, MAX_DIM)).save(img_dst)


def gen_yolo_label(text_dir, shapes, img_name):
    label_name = img_name.replace(".JPEG", ".txt")
    
    label_data = []
    for shape in shapes:
        line = ' '.join(map(str, shape))
        label_data.append(f"{line}\n")
        
    text_file_path = join(text_dir, label_name)
    with open(text_file_path, 'w') as f:
            f.writelines(label_data)
    
    
def main():
    temp_dataset_path = aggregator.aggregate()
    img_dst = join(DESTINATION, "images")
    lbl_dst = join(DESTINATION, "labels")
    makedirs(img_dst, exist_ok=True)
    makedirs(lbl_dst, exist_ok=True)

    examples = list_examples(temp_dataset_path)

    with ThreadPoolExecutor() as executor:
        tasks = []

        for e in examples:
            tasks.append(executor.submit(move_resized_image, temp_dataset_path, img_dst, e.img))
            tasks.append(executor.submit(gen_yolo_label, lbl_dst, e.shapes, e.img))

        for task in as_completed(tasks):
            try:
                task.result()
            except Exception as exc:
                print(f"An error occurred: {exc}")

    shutil.rmtree(temp_dataset_path)
    print("Dataset preprocessing finished. Result is stored in: " + DESTINATION)

if __name__ == "__main__":
    main()
    