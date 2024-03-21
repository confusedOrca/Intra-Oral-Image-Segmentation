def rect_to_poly(upper_left_coo, lower_right_coo):
    x1, y1 = upper_left_coo
    x2, y2 = lower_right_coo
    return [ [x1, y1], [x2, y1], [x2, y2], [x1, y2] ]