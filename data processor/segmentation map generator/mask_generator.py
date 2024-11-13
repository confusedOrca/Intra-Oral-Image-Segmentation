import numpy as np
import cv2
from concurrent.futures import ThreadPoolExecutor
from config import MAX_DIM

IMAGE_HEIGHT = MAX_DIM
IMAGE_WIDTH = MAX_DIM

def fill_polygon(mask, points, class_id):
    cv2.fillPoly(mask, [np.array(points)], class_id)
    return mask

def generate_mask(data):
    mask_copies = []
    base_mask = np.zeros((IMAGE_HEIGHT, IMAGE_WIDTH), dtype=np.uint8)

    with ThreadPoolExecutor() as executor:
        tasks = []

        for row in data:
            class_id = row[0]
            coordinates = row[1:]
            points = [
                (int(x * IMAGE_WIDTH), int(y * IMAGE_HEIGHT)) 
                for x, y in zip(coordinates[::2], coordinates[1::2])
                ]

            mask_copy = base_mask.copy()
            tasks.append(executor.submit(fill_polygon, mask_copy, points, class_id))

        for task in tasks:
            mask_copies.append(task.result())
    
    combined_mask = np.max(np.array(mask_copies), axis=0)
    return combined_mask
