from labels import labels

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

def get_num_dimensions(arr):
    if not isinstance(arr, list):
        return 0
    if not arr:
        return 1
    return 1 + get_num_dimensions(arr[0])

def select_and_process_shapes(shapes):
    selections = []
    
    for shape in shapes:
        if shape.get("label") in labels:
            if shape.get("shape_type") == "rectangle":
                x1_y1 = shape['points'][0]
                x2_y2 = shape['points'][1]
                shape['points'] = rect_to_poly(x1_y1, x2_y2)
                
            selections.append(shape)
    
    return [{'label': s['label'], 'points': s['points']} for s in selections if s.get("label") in labels]