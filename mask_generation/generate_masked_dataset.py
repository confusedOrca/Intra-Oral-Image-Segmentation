import os
from list_examples import list_examples
from generate_mask import save_masks

root_dir = os.path.abspath(os.path.join(os.getcwd(), os.pardir))

from labels import labels

def generate_masks(dir, jaw, mask_dir):
    datalist = list_examples(dir, jaw)
    
    for data in datalist:
        poly_data = data.shapes
        height = data.height
        width = data.width
        name = data.image_dir
        for label in labels:
            path = root_dir + f"{mask_dir}\{jaw}\{label}"
            save_masks(poly_data, label, height, width, path, name)
    

if __name__ == "__main__":
    upper_dir = root_dir + "\Labelled intraoral smartphone images\Labels_Upper jaw"
    lower_dir = root_dir + "\Labelled intraoral smartphone images\Labels_Lower jaw"
    generate_masks(upper_dir, "upper", "\masks_v1")
    generate_masks(lower_dir, "lower", "\masks_v1")