from list_examples import list_examples
from utils import move_resized_image, gen_yolov8_label

MAX_DIM = 640

def main():
    src = "aggregated_dataset"
    img_dst = "labelled_dataset\images"
    lbl_dst = "labelled_dataset\labels"
    examples = list_examples(src)
    
    for e in examples:
        move_resized_image(src, img_dst, e.height, e.width, MAX_DIM, e.img)
        gen_yolov8_label(lbl_dst, e.shapes, e.img.replace(".JPEG", ".txt"))

if __name__ == "__main__":
    main()