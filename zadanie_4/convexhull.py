import math
from collections import deque

def turn(p1, p2, p3):
    return (p2[0]-p1[0])*(p3[1]-p1[1])-(p2[1]-p1[1])*(p3[0]-p1[0])

def graham(Q):
    P0 = min(Q, key=lambda p: (p[1], -p[0]))
    
    Q = sorted(Q, key=lambda p: (math.atan2(p[1]-P0[1], p[0]-P0[0]), (p[0]-P0[0])**2+(p[1]-P0[1])**2))

    i = 1
    while i < len(Q):
        if math.atan2(Q[i][1]-P0[1], Q[i][0]-P0[0]) == math.atan2(Q[i-1][1]-P0[1], Q[i-1][0]-P0[0]):
            Q.pop(i)
        else:
            i += 1

    m = len(Q)

    S = deque([P0, Q[0], Q[1]])

    for j in range(2, m):
        while turn(S[-2], S[-1], Q[j]) <= 0:
            S.pop()
        S.append(Q[j])
    
    return list(S)
    




