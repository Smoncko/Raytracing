import sys
from razredi import Meje

#Algoritem za preverjanje presečišča med žarkom in okvirjem

def aabb(T0, smer, okvir: Meje):
    t1 = (okvir.minX - T0[0]) / (smer[0] + sys.float_info.epsilon)
    t2 = (okvir.maxX - T0[0]) / (smer[0] + sys.float_info.epsilon)
    t3 = (okvir.minY - T0[1]) / (smer[1] + sys.float_info.epsilon)
    t4 = (okvir.maxY - T0[1]) / (smer[1] + sys.float_info.epsilon)
    t5 = (okvir.minZ - T0[2]) / (smer[2] + sys.float_info.epsilon)
    t6 = (okvir.maxZ - T0[2]) / (smer[2] + sys.float_info.epsilon)

    tmin = max(min(t1, t2), min(t3, t4), min(t5, t6))
    tmax = min(max(t1, t2), max(t3, t4), max(t5, t6))

    if tmax > 0 and tmin < tmax:
        return True, tmin, tmax
    
    return False, 0, 0