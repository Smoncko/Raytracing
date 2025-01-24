import sys
import json
import numpy as np
import numpy.linalg as lin
from matplotlib.pyplot import imshow, show
from tri import tri
#from aabb import aabb
import pprint
import time
import winsound


def odboj(smer, parametri, T0, luc, tr_globina=0, korak=0.1, max_globina=1):
    X = None
    gradF = None
    CLR = None
    najblizji = None
    oddaljenost = None
    senca = None

    if tr_globina == max_globina:
        return (X, gradF, CLR, oddaljenost, senca)

    for i in range(0, len(parametri)):
        P = parametri[i]

        hit, tr_X, tr_gradF, tr_CLR = tri(T0, smer, P)
        # print(hit, tr_X, tr_gradF, tr_CLR)

        if hit:
            odd = lin.norm(np.subtract(tr_X, T0))

            if (najblizji is None) or (odd < najblizji):
                najblizji = odd
                X = tr_X
                gradF = tr_gradF
                CLR = tr_CLR
                senca = None
            else:
                continue

            n = gradF / lin.norm(gradF)
            nova_smer = smer - 2 * (np.dot(smer, n))*n
            luc_pr = np.subtract(luc, X)

            for k in range(0, len(parametri)):
                P2 = parametri[k]
                if k == 1:
                    continue
                else:
                    hit2, tr_X2, _, _ = tri(luc, -luc_pr, P2)
                    if hit2 and (lin.norm(np.subtract(luc, tr_X2)) < lin.norm(luc_pr)):
                        senca == 1
            
            if senca is None:
                cos = np.dot(luc_pr, nova_smer) / (lin.norm(luc_pr) * lin.norm(nova_smer))
                CLR = (CLR + np.array([255, 255, 255]) * cos ) / (lin.norm(luc_pr) / 2)
            else:
                CLR = (CLR - [50, 50, 50]) / (lin.norm(luc_pr) / 2)
            
            CLR = np.minimum(CLR, [255, 255, 255])
            CLR = np.maximum(CLR, [0, 0, 0])

            (_, _, rekCLR, rekNorm, _) = odboj(nova_smer, parametri, X, luc, tr_globina + 1, korak, max_globina)

            if rekNorm is not None:
                utez1 = 1 / oddaljenost**2
                utez2 = 1 / (rekNorm + oddaljenost)**2
                s = utez1 + utez2
                utez1 = utez1 / s
                utez2 = utez2 / s
                CLR = CLR * utez1 + rekCLR * utez2

    return (X, gradF, CLR, oddaljenost, senca)


def raytracing(T0, loc, luc, parametri, viewport, BG, glad=False):
    t = time.time()

    visina = loc[0]
    sirina = loc[1]

    zaslon = np.zeros((visina, sirina, 3))
    shadows = np.zeros((visina, sirina))

    for y in range(0, visina):                                                  #za vsako točko na zaslonu
        for x in range(0, sirina):
            CLR = None
            senca = None
            pix = [-viewport + 2*viewport/sirina * x, 0, viewport - 2*viewport/visina * y]                      #platno je ravnina y = 0
            smer = np.subtract(pix, T0)                                         #žarek kot parametrična premica
            #if aabb(T0, smer, okvir):
            (_, _, CLR, _, senca) = odboj(smer, parametri, T0, luc)             #rekurzivno preverjanje odbojev
                # CLR = [0, 0, 255]
                # exit = True
            if senca is not None:
                shadows[y, x] = 1
            if CLR is None:
                zaslon[y, x, :] = BG
            else:
                zaslon[y, x, :] = CLR
            
        print(f"Completed row {y} of {visina}")
    elapsed = time.time() - t
    print("Raytracing time taken:", elapsed)

    # duration = 500  # milliseconds
    # freq = 440  # Hz
    # winsound.Beep(freq, duration)

    zaslon /= 256
    imshow(zaslon)
    show()


def main():                                         #nalozimo podatke
    with open(sys.argv[1]) as f:
        data = json.load(f)

    objekti = data["objekti"]
    nObj = len(objekti)

    loc = data["loc"]
    luc = data["luc"]
    T0 = data["T0"]
    BG = data["BG"]
    glad = data["glad"]
    viewport = data["viewport"]

    parametri = []

    vec = [0, -1, 0]
    tmp = np.copy(T0)
    tmp[2] = 0
    cosAlpha = np.dot(vec, tmp) / (lin.norm(vec) * lin.norm(tmp))
    alpha = np.arccos(cosAlpha)
    sinAlpha = np.sin(alpha)
    
    Rz = np.array([ [cosAlpha, -sinAlpha, 0],
                    [sinAlpha, cosAlpha, 0],
                    [0, 0, 1]])
    
    tmp = (Rz @ np.copy(T0)[:, np.newaxis]).flatten()
    tmp[0] = 0
    cosBeta = np.dot(vec, tmp) / (lin.norm(vec) * lin.norm(tmp))
    beta = np.arccos(cosBeta)
    sinBeta = np.sin(beta)
    # print(alpha * 180 / np.pi, beta * 180 / np.pi)

    Rx = np.array([ [1, 0, 0],
                    [0, cosBeta, -sinBeta],
                    [0, sinBeta, cosBeta]])
    Rot = Rx @ Rz
    # print(Rot)
    T0 = (Rot @ np.copy(T0)[:, np.newaxis]).flatten()
    luc = (Rot @ np.copy(luc)[:, np.newaxis]).flatten()
    # print()

    parseTimer = time.time()
    for i in range(0, nObj):
        VM = {}
        NM = {}
        idxV = 1
        idxN = 1
        with open(objekti[i]["parametri"]) as p:
            for line in p:
                tmp = line.rstrip().split(" ")
                if tmp[0] == "v":
                    #Rotacija oglišč okrog z osi glede na začetno točko
                    VM[idxV] = (Rot @ [[float(tmp[1])], [float(tmp[2])], [float(tmp[3])]]).flatten()
                    idxV += 1
                if tmp[0] == "vn":
                    NM[idxN] = (Rot @ [[float(tmp[1])], [float(tmp[2])], [float(tmp[3])]]).flatten()
                    idxN += 1
                if tmp[0] == "f":
                    a = tmp[1].split("/")
                    b = tmp[2].split("/")
                    c = tmp[3].split("/")
                    parametri.append(([255, 0, 0,], VM[int(a[0])], VM[int(b[0])], VM[int(c[0])], NM[int(a[2])], NM[int(b[2])], NM[int(c[2])]))
        # pp = pprint.PrettyPrinter(indent=4)
        # pp.pprint(parametri)
        # pp.pprint(VM)
    # print()
    parseElapsed = time.time() - parseTimer
    print("Parse time taken:", parseElapsed)


    # minX = np.inf
    # maxX = -np.inf
    # minY = np.inf
    # maxY = -np.inf
    # minZ = np.inf
    # maxZ = -np.inf
    # for key in VM:
    #     X, Y, Z = VM[key]
    #     minX = min(minX, X)
    #     maxX = max(maxX, X)
    #     minY = min(minY, Y)
    #     maxY = max(maxY, Y)
    #     minZ = min(minZ, Z)
    #     maxZ = max(maxZ, Z)
    # okvir = [minX, maxX, minY, maxY, minZ, maxZ]

    raytracing(T0, loc, luc, parametri, viewport, BG)


if __name__ == "__main__":
    main()