from predictor import YOLOInference
from masker import mask
from sequencer import draw_path_with_dots
import os

model = YOLOInference(model_path="model/yolo11m_det/best.pt")

def list_jpeg_files(directory):
    jpeg_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(('.jpg', '.jpeg')):
                jpeg_files.append(os.path.join(root, file))
    return jpeg_files

def process_img(img_path):
    result = model.predict(img_path)
    image_with_mask = mask(img_path, result)
    coo_values = [item['coo'] for item in result]
    img = draw_path_with_dots(image_with_mask, coo_values)
    os.remove(img_path)
    img.convert('RGB').save(img_path)

if __name__ == "__main__":
    directory = "dataset/seg_dataset_after_split_yolo_p"
    paths = list_jpeg_files(directory)
    for p in paths:
        process_img(p)
    
    
