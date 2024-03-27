import numpy as np
import cv2
import os

from labels import labels

def generate_mask(polygons, image_shape):
    mask = np.zeros(image_shape[:2], dtype=np.uint8)
    for polygon in polygons:
        pts = np.array(polygon, np.int32)
        pts = pts.reshape((-1, 1, 2))
        cv2.fillPoly(mask, [pts], 255)
    return mask


def save_masks(polygons_data, label, height, width, output_dir, name):
        label_polygons = [shape['points'] for shape in polygons_data if shape['label'] == label]
        mask = generate_mask(label_polygons, (height, width))
        os.makedirs(output_dir, exist_ok=True)
        file_path = os.path.join(output_dir, name)
        cv2.imwrite(file_path, mask)


if __name__ == "__main__":
    dummy_poly_data = [
        {'label': 'calculus', 'points': [[900, 1200], [900, 1500], [1000, 1600], [1200, 1600], [100, 1600], [100, 1400]]},
        {'label': 'calculus', 'points': [[100, 300], [100, 700], [200, 800], [400, 800], [0, 800], [0, 700]]},
        {'label': 'non-carious lesion', 'points': [[1000, 1300], [1000, 1500], [1000, 1600], [1200, 1600], [1200, 1600], [1100, 1500]]},
    ]

    output_dir = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
    save_masks(dummy_poly_data, labels[3], 4032, 3024, output_dir, "dummy_example")
