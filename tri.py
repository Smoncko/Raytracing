import numpy as np
import numpy.linalg as lin
from razredi import Parameter

def tri(V0, smer, par: Parameter):
    tol = 1e-4

    Va = par.A                               #Koordinate oglišč
    Vb = par.B
    Vc = par.C

    N = (par.nA + par.nB + par.nC) / 3            #Normala trikotnika iz normal oglišč

    # print("\t", smer)
    smer = smer / lin.norm(smer)
    # print("\t", smer)
    div = np.dot(smer, N)                   #Presečišče vektorja in ravnine
    if div >= 0:
        return (False, None, None, None)
    
    d = np.dot((Va - V0), N) / div
    if (d < 1e-4):                             #Presečišče je na napačni strani žarka
        return (False, None, None, None)

    Vp = V0 + smer * d               #Točka na ravnini, ki jo določa trikotnik

    Vba = Vb - Va
    Vca = Vc - Va
    Vbc = Vb - Vc
    Vap = Va - Vp
    Vbp = Vb - Vp
    Vcp = Vc - Vp
    n0 = np.cross(Vba, Vca)
    n1 = np.cross(Vap, Vbp)
    n2 = np.cross(Vap, Vcp)
    n3 = np.cross(Vbp, Vcp)
    A  = lin.norm(n0)
    A1 = lin.norm(n1)
    A2 = lin.norm(n2)
    A3 = lin.norm(n3)

    if A1 + A2 + A3 <= A + tol:
        return True, Vp, N, par.barve
    else:
        if (A1 + A2 + A3 - A < 0.1):
            d1 = A1 / lin.norm(Vba)
            d2 = A2 / lin.norm(Vca)
            d3 = A3 / lin.norm(Vbc)
            if d1 < tol or d2 < tol or d3 < tol:
                return True, Vp, N, par.barve
        return False, None, None, None
