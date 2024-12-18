from color_picker import get_color
from PIL import Image, ImageDraw

def draw_path_with_dots(image, coordinates):
    img_width, img_height = image.size
    draw = ImageDraw.Draw(image)

    steps = len(coordinates)
    
    for i in range(steps):
        color = get_color(i, steps)

        x, y = coordinates[i]
        x = int(x * img_width)
        y = int(y * img_height)
        draw.ellipse([(x - 1, y - 1), (x + 1, y + 1)], fill=color, width=10)

        if i < steps - 1:
            next_x, next_y = coordinates[i + 1]
            next_x = int(next_x * img_width)
            next_y = int(next_y * img_height)
            draw.line([(x, y), (next_x, next_y)], fill=color, width=1)

    return image