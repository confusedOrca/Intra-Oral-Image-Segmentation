import os
import json
from typing import List
from data_structures.example import ImageData
from utils import seg_data_format

def list_examples(dir_path) -> List[ImageData]:
    datalist = []
    dir_path = os.path.join(os.getcwd(), dir_path)

    for filename in os.listdir(dir_path):
        if filename.endswith('.json'):
            path = os.path.join(dir_path, filename)
            
            with open(path, 'r') as file:
                data = json.load(file)
                h, w, img = data.get("imageHeight"), data.get("imageWidth"), data.get("imagePath")
                shapes = data.get("shapes", [])
                shapes = [seg_data_format(s['points'], w, h, s['label'], s['shape_type']) for s in shapes]
                shapes = [s for s in shapes if s is not None]
                data = ImageData(img, h, w, shapes)
                datalist.append(data)

    return datalist


if __name__ == "__main__":
    image_data_list = list_examples("dataset_v1.2")
    print(image_data_list[10])

