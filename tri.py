import numpy as np
import numpy.linalg as lin

def tri(V0, smer, P):
    V0 = np.asarray(V0)                     #Zažetna točka
    P = np.asarray(P)                       #Parametri trikotnika

    tol = 1e-6

    rgb = P[0]

    Va = P[1]                               #Koordinate oglišč
    Vb = P[2]
    Vc = P[3]

    N = (P[4] + P[5] + P[6]) / 3            #Normala trikotnika iz normal oglišč

    # print("\t", smer)
    smer = smer / lin.norm(smer)
    # print("\t", smer)
    div = np.dot(smer, N)                   #Presečišče vektorja in ravnine
    if div == 0:
        return (False, None, None, None)
    d = np.dot((Va - V0), N) / div
    (x, y, z) = V0 + smer * d               #Točka na ravnini

    Vp = [x, y, z]

    Vba = Vb - Va
    Vca = Vc - Va
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

    hit = False

    if A1 + A2 + A3 <= A + tol and d >= 0:
        # print(f"Inside: {A1} + {A2} + {A3} <= {A}\nV0 = {V0}, smer = {smer}, d = {d}\nVp = {Vp}\n")
        hit = True
    else:
        # print("Outside")
        pass
    # print(hit, Vp, N, rgb)
    return (hit, Vp, N, rgb)
