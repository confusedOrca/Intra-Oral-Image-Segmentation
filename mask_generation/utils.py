def rect_to_poly(upper_left_coo, lower_right_coo):
    x1, y1 = upper_left_coo
    x2, y2 = lower_right_coo
    return [ [x1, y1], [x2, y1], [x2, y2], [x1, y2] ]

def bounding_box(coordinates):
    if not coordinates:
        return []
    
    min_x = min(coordinates, key=lambda x: x[0])[0]
    max_x = max(coordinates, key=lambda x: x[0])[0]
    min_y = min(coordinates, key=lambda x: x[1])[1]
    max_y = max(coordinates, key=lambda x: x[1])[1]

    return [min_x, min_y, max_x, max_y]

def average_coordinates(coordinates):
    if not coordinates:
        return []
    
    sum_x = sum(y[0] for y in coordinates)
    sum_y = sum(y[1] for y in coordinates)
    avg_x = sum_x / len(coordinates)
    avg_y = sum_y / len(coordinates)
    
    return [avg_x, avg_y]

def return_bbox_n_center(shapes, label):
        label_polygons = [shape['points'] for shape in shapes if shape['label'] == label]
        bboxes = [bounding_box(label_polygon) for label_polygon in label_polygons]
        avg_coordinates = [average_coordinates(label_polygon) for label_polygon in label_polygons]
        return bboxes, avg_coordinates