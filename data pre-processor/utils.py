from os import getcwd, listdir, cpu_count
from os.path import abspath, dirname, join
import json
from typing import List
from data_structures.example import ImageData
from config import LABELS
from concurrent.futures import ThreadPoolExecutor, as_completed

MODULE_DIR = dirname(abspath(__file__))
BASE_DIR = getcwd()

def format_polygon(polygon, img_w, img_h, label, s_type):
    if label.isdigit():
        label = "tooth"
        
    if label not in LABELS:
        return None
    
    if s_type == "rectangle":
        tl, br = polygon[0], polygon[1]
        polygon = [tl, [tl[0], br[1]], br, [br[0], tl[1]]]
    
    poly_data = [min(LABELS.index(label), 4) + 1]
    for p in polygon:
        poly_data.append(round(p[0] / img_w, 5))
        poly_data.append(round(p[1] / img_h, 5))
    
    return poly_data


def process_file(path: str) -> ImageData:
    with open(path, 'r') as file:
        data = json.load(file)
        img = data.get("imagePath")
        h, w = data.get("imageHeight"), data.get("imageWidth")
        shapes = [
            formatted_shape
            for s in data.get("shapes", [])
            if (formatted_shape := format_polygon(s['points'], w, h, s['label'], s['shape_type'])) is not None
        ]
        return ImageData(img, h, w, shapes)


def list_examples(dir_path: str) -> List[ImageData]:
    datalist = []
    json_files = [
        join(dir_path, filename) 
        for filename in listdir(dir_path) 
        if filename.endswith('.json')
        ]

    with ThreadPoolExecutor(max_workers=cpu_count() * 2) as executor:
        tasks = {
            executor.submit(process_file, path): path for path in json_files
            }
        
        for task in as_completed(tasks):
            try:
                datalist.append(task.result())
            except Exception as exc:
                print(f"Error processing file {tasks[task]}: {exc}")
    
    return datalist
