import zadanie_3

def bbox_check(x, y):
    x_coords = [point[0] for point in polygon]
    y_coords = [point[1] for point in polygon]
    return min(x_coords) <= x <= max(x_coords) and min(y_coords) <= y <= max(y_coords)

def check_point_location(x, y):
    return bbox_check(x, y) and polygon_check(x, y)

def intersection_check(x1, y1, x2, y2, x3, y3):
    cross_product = (x2 - x1) * (y3 - y1) - (y2 - y1) * (x3 - x1)
    return cross_product < 0

def edge_check(x1, y1, x2, y2, x3, y3):
    return (x1 - x2) * (y3 - y2) == (y1 - y2) * (x3 - x2)

def polygon_check(x, y):
    counter = 0
    for i in range(len(polygon)):
        if i == len(polygon) - 1:
            if edge_check(polygon[i][0], polygon[i][1], polygon[0][0], polygon[0][1], x, y):
                return True
            if intersection_check(polygon[i][0], polygon[i][1], polygon[0][0], polygon[0][1], x, y):
                counter += 1
        else:
            if edge_check(polygon[i][0], polygon[i][1], polygon[i+1][0], polygon[i+1][1], x, y):
                return True
            if intersection_check(polygon[i][0], polygon[i][1], polygon[i+1][0], polygon[i+1][1], x, y):
                counter += 1
    return counter % 2 == 1