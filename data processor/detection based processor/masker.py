from PIL import Image, ImageDraw

def draw_bboxes_on_image(image_path, bboxes):
    image = Image.open(image_path)
    width, height = image.size
    mask = Image.new("L", (width, height), 0)
    draw = ImageDraw.Draw(mask)

    for bbox in bboxes:
        coo = bbox["coo"]
        w, h = bbox["w"], bbox["h"]
        
        h *= 1.1
        w *= 1.05 
        
        x_center, y_center = coo
        x1 = x_center - (w / 2)
        y1 = y_center - (h / 2) 
        x2 = x_center + (w / 2)
        y2 = y_center + (h / 2)
        
        draw.rectangle([x1 * width, y1 * height, x2 * width, y2 * height], fill=255)

    return mask

def apply_mask_to_image(image_path, mask):
    image = Image.open(image_path).convert("RGBA")  
    transparent_image = Image.new("RGBA", image.size, (0, 0, 0, 0))
    transparent_image.paste(image, (0, 0), mask)
    
    return transparent_image

def mask(image_path, bbox_data):
    mask = draw_bboxes_on_image(image_path, bbox_data)
    image_with_mask = apply_mask_to_image(image_path, mask)
    return image_with_mask