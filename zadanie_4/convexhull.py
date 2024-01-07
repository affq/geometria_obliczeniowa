# otoczka wypukła - algorytm Grahama

import math
import random
import matplotlib.pyplot as plt
import time

def det(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def graham(points):
    points = sorted(points)
    points = sorted(points, key=lambda x: math.atan2(x[1] - points[0][1], x[0] - points[0][0]))
    stack = [points[0], points[1]]

    for point in points[2:]:
        while det(stack[-2], stack[-1], point) <= 0:
            stack.pop()
        stack.append(point)

    return stack


