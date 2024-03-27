import os
import cv2
import numpy as np
import torch
from SlimSAM import model, processor
from utils import return_bbox_n_center, get_num_dimensions
from labels import labels

root_dir = os.path.abspath(os.path.join(os.getcwd(), os.pardir))

def generate_SAM_mask(shapes, raw_image, dataset, jaw, image_name):
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model.to(device)
    
    for label in labels:
        input_boxes, center = return_bbox_n_center(shapes, label)
        input_boxes = [input_boxes]
        center = [center]
        
        if(get_num_dimensions(input_boxes) < 3):
            width, height = raw_image.size
            combined_mask = np.zeros((height, width), dtype=np.uint8) * 255
        
        else:
            inputs = processor(raw_image, input_boxes=[input_boxes], input_labels=[center],  return_tensors="pt").to(device)

            with torch.no_grad():
                outputs = model(**inputs)
            
            masks = processor.image_processor.post_process_masks(
                outputs.pred_masks.cpu(), inputs["original_sizes"].cpu(), inputs["reshaped_input_sizes"].cpu()
            )
            
            scores = outputs.iou_scores
            best_index = np.argmax(scores.to('cpu').numpy()[0], axis=1)
        
            combined_mask = np.zeros_like(masks[0][0][0], dtype=bool)
            for i in range(len(best_index)):
                mask = masks[0][i][best_index[i]]
                combined_mask = np.logical_or(combined_mask, mask)
            combined_mask = combined_mask.numpy().astype(np.uint8) * 255
        
        target_directory = root_dir + f"\{dataset}\{jaw}\{label}"
        os.makedirs(target_directory, exist_ok=True)
        file_path = os.path.join(target_directory, image_name)
        cv2.imwrite(file_path, combined_mask)