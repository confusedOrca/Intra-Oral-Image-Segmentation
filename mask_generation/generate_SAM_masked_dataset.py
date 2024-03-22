import os
from list_examples import list_examples
from generate_SAM_mask import generate_SAM_mask
from PIL import Image

root_dir = os.path.abspath(os.path.join(os.getcwd(), os.pardir))

def generate_SAM_masks(dir, jaw, dataset):
    datalist = list_examples(dir, jaw)
    
    for data in datalist:
        name = data.image_dir
        shapes = data.shapes
        raw_image = Image.open(dir + f"\{name}")
        generate_SAM_mask(shapes, raw_image, dataset, jaw, name)
        

if __name__ == "__main__":
    upper_dir = root_dir + "\Labelled intraoral smartphone images\Labels_Upper jaw"
    lower_dir = root_dir + "\Labelled intraoral smartphone images\Labels_Lower jaw"
    generate_SAM_masks(upper_dir, "upper", "masks_v2")
    generate_SAM_masks(lower_dir, "lower", "masks_v2")
        