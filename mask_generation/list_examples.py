import sys
import os
import json
from typing import List

parent_dir = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
sys.path.append(parent_dir)

from data_structures.example import ImageData
from shape_processor import select_and_process_shapes
    

def list_examples(dir_path, jaw) -> List[ImageData]:
    datalist = []

    for filename in os.listdir(dir_path):
        if filename.endswith('.json'):
            path = os.path.join(dir_path, filename)
            
            with open(path, 'r') as file:
                data = json.load(file)
                h, w, img_path = data.get("imageHeight"), data.get("imageWidth"), data.get("imagePath")
                shapes = select_and_process_shapes(data.get("shapes", []))
                data = ImageData(img_path, h, w, jaw, shapes)
                datalist.append(data)

    return datalist


if __name__ == "__main__":
    lower_jaw_dir = os.path.join(parent_dir, "Labelled intraoral smartphone images\Labels_Lower jaw")
    image_data_list = list_examples(lower_jaw_dir, "lower")
    
    print(image_data_list[10])


