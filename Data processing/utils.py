from PIL import Image
import os
import shutil
import random

labels = [
    "visible changes with microcavitation", 
    "visible changes with cavitation", 
    "calculus", 
    "non-carious lesion"
    ]

def seg_data_format(polygon, img_w, img_h, label, s_type):
    if label not in labels:
        return None
    
    if s_type == "rectangle":
        tl = polygon[0]
        br = polygon[1]
        polygon = [tl, [tl[0], br[1]], br, [br[0], tl[1]]]
    
    poly_data = [labels.index(label)]
    
    for p in polygon:
        poly_data.append(round(p[0] / img_w,5))
        poly_data.append(round(p[1] / img_h,5))
    
    return poly_data

def bbox_of_polygon(polygon, img_h, img_w, label):
    
    if label not in labels:
        return None
    
    min_x = float('inf')
    max_x = float('-inf')
    min_y = float('inf')
    max_y = float('-inf')
    label = labels.index(label)

    for point in polygon:
        x, y = point
        min_x = min(min_x, x)
        max_x = max(max_x, x)
        min_y = min(min_y, y)
        max_y = max(max_y, y)

    center_x = (min_x + max_x) / 2
    center_y = (min_y + max_y) / 2
    height = max_y - min_y
    width = max_x - min_x

    bbox = [label, center_x / img_w, center_y / img_h, width / img_w, height / img_h]
    return [round(num, 5) for num in bbox]


def move_resized_image(src_dir, dst_dir, h, w, max_dim_size, name):
    
        src_image_path = os.path.join(os.getcwd(), src_dir, name)
        image = Image.open(src_image_path)

        if h > w:
            new_height = max_dim_size
            new_width = int((max_dim_size / h) * w)
        else:
            new_width = max_dim_size
            new_height = int((max_dim_size / w) * h)
        
        resized_image = image.resize((new_width, new_height))
        dst_image_path = os.path.join(os.getcwd(), dst_dir, name)
        resized_image.save(dst_image_path)
        
def gen_yolov8_label(text_dir, shapes, name):
    if(len(shapes) == 0):
        text_file_path = os.path.join(os.getcwd(), text_dir, name)
        with open(text_file_path, 'a+') as f:
            f.write(f"")
        return
        
    for i, shape in enumerate(shapes):
        line = ' '.join(map(str, shape))
        text_file_path = os.path.join(os.getcwd(), text_dir, name)
        with open(text_file_path, 'a+') as f:
            f.write(f"{line}\n")

def move_images_and_labels(src_folder, dst_folder, images, set):
    for image_name in images:
        image_name = image_name.replace(".JPEG", "")
        
        src_images_dir = os.path.join(os.getcwd(), src_folder, "images")
        src_labels_dir = os.path.join(os.getcwd(), src_folder, "labels")
        dst_images_dir = os.path.join(os.getcwd(), dst_folder, "images", set)
        dst_labels_dir = os.path.join(os.getcwd(), dst_folder, "labels", set)

        src_image_path = os.path.join(src_images_dir, image_name + ".JPEG")
        dst_image_path = os.path.join(dst_images_dir, image_name + ".JPEG")

        src_label_path = os.path.join(src_labels_dir, image_name + ".txt")
        dst_label_path = os.path.join(dst_labels_dir, image_name + ".txt")

        os.makedirs(os.path.dirname(dst_image_path), exist_ok=True)
        shutil.move(src_image_path, dst_image_path)
        
        os.makedirs(os.path.dirname(dst_label_path), exist_ok=True)
        shutil.move(src_label_path, dst_label_path)


def select_random_images(directory, n, seed=0):
    directory = os.path.join(os.getcwd(), directory, "images")
    random.seed(seed)
    images = [f for f in os.listdir(directory) if f.lower().endswith('.jpeg')]
    return random.sample(images, n)