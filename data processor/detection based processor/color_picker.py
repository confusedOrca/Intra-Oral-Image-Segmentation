def get_color(i, steps):
    if i < steps // 2:
        red = 255 - (255 // (steps // 2)) * i
        green = (255 // (steps // 2)) * i
        blue = 0
    else:
        i = i - (steps // 2)
        red = 0
        green = 255 - (255 // (steps // 2)) * i
        blue = (255 // (steps // 2)) * i

    return (red, green, blue)
