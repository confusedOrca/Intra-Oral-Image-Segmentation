import math
import os
from ultralytics import YOLO

class YOLOInference:
    def __init__(self, model_path):
        self.model = YOLO(model_path, task='detect')
        print("Model loaded successfully!")

    def predict(self, image_path):
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image path '{image_path}' does not exist.")

        results = self.model.predict(image_path, conf=0.65)

        xywhn = results[0].boxes.xywhn

        bboxes = [
            {
                "coo": (round(float(bbox[0]), 3), round(float(bbox[1]), 3)),  
                "w": round(float(bbox[2]), 3),
                "h": round(float(bbox[3]), 3),
                "r_coo": (  
                    round(float(bbox[0]) + float(bbox[2]) / 2, 3),
                    round(float(bbox[1]), 3),
                ),
                "flag": False, 
            }
            for bbox in xywhn
        ]

        sorted_bboxes = self.sort_bboxes(bboxes)
        return sorted_bboxes

    def sort_bboxes(self, bboxes):
        initial_bbox = min(bboxes, key=lambda bbox: (bbox["coo"][0], bbox["coo"][1]))
        initial_bbox["flag"] = True
        visited_bboxes = [initial_bbox]
        current_bbox = initial_bbox
        
        while len(visited_bboxes) < len(bboxes):
            closest_bbox = None
            closest_distance = float("inf")

            for bbox in bboxes:
                if not bbox["flag"]:
                    distance = self.calculate_distance(current_bbox["r_coo"], bbox["coo"])
                    if distance < closest_distance:
                        closest_distance = distance
                        closest_bbox = bbox

            if closest_bbox:
                closest_bbox["flag"] = True
                visited_bboxes.append(closest_bbox)
                current_bbox = closest_bbox
        
        return visited_bboxes

    def calculate_distance(self, r_coo_1, coo_2):
        return math.sqrt((r_coo_1[0] - coo_2[0]) ** 2 + (r_coo_1[1] - coo_2[1]) ** 2)