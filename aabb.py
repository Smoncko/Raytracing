import numpy as np

def aabb(T0, smer, okvir):
    t1 = (okvir[0] - T0[0]) / smer[0]
    t2 = (okvir[1] - T0[0]) / smer[0]
    t3 = (okvir[2] - T0[1]) / smer[1]
    t4 = (okvir[3] - T0[1]) / smer[1]
    t5 = (okvir[4] - T0[2]) / smer[2]
    t6 = (okvir[5] - T0[2]) / smer[2]

    tmin = max(min(t1, t2), min(t3, t4), min(t5, t6))
    tmax = min(max(t1, t2), max(t3, t4), max(t5, t6))

    if tmax < 0 or tmin > tmax:
        return False
    else:
        return True