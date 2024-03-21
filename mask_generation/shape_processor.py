from utils import rect_to_poly
from labels import labels


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