import sys
import json
import numpy as np
import numpy.linalg as lin
from matplotlib.pyplot import imshow, show, axis
from tri import tri
from aabb import aabb
import time
# import winsound
from razredi import *
from sklearn.cluster import KMeans
from collections import OrderedDict

countAABB = 0
countTris = 0

def bvh_kmeans(VM):
    #Algoritem za razbijanje objekta s k-voditelji

    Vx = []
    Vy = []
    Vz = []
    
    for _, v in VM.items():
        Vx.append(v[0])
        Vy.append(v[1])
        Vz.append(v[2])

    points = list(zip(Vx, Vy, Vz))

    #Voditeljev je 7, ta parameter je spremenljiv
    k = 7
    kmeans = KMeans(n_clusters=k)
    kmeans.fit(points)

    minmax = []
    for _ in range(k):
        minmax.append(Meje())
    for l in range(len(kmeans.labels_)):
        minmax[kmeans.labels_[l]].posodobi([Vx[l], Vy[l], Vz[l]])        

    return minmax


def naredi_bvh(parametri, minmax, meje: Meje, max_globina=1, tr_globina=0):
    #Algoritem za ustvarjanje hierarhije očrtanih okvirjev

    ploskve = []
    newMM = []
    
    for i in range(len(parametri)):
        if  not (minmax[i].maxX < meje.minX or minmax[i].minX > meje.maxX) and\
            not (minmax[i].maxY < meje.minY or minmax[i].minY > meje.maxY) and\
            not (minmax[i].maxZ < meje.minZ or minmax[i].minZ > meje.maxZ):
                ploskve.append(parametri[i])
                newMM.append(minmax[i])

    okvir = Okvir([], meje, ploskve)
    if tr_globina == max_globina or len(ploskve) <= 10 or (len(ploskve) == len(parametri) and tr_globina != 0):
        return okvir

    avgX = (meje.minX + meje.maxX) / 2
    avgY = (meje.minY + meje.maxY) / 2
    avgZ = (meje.minZ + meje.maxZ) / 2
    for a in range(0, 2):
        for b in range(0, 2):
            for c in range(0, 2):
                novMinX = meje.minX*a + avgX*(1-a)
                novMaxX = meje.maxX*(1-a) + avgX*a
                novMinY = meje.minY*b + avgY*(1-b)
                novMaxY = meje.maxY*(1-b) + avgY*b
                novMinZ = meje.minZ*c + avgZ*(1-c)
                novMaxZ = meje.maxZ*(1-c) + avgZ*c
                okvir.otroci.append(naredi_bvh(ploskve, newMM, Meje(novMinX, novMaxX, novMinY, novMaxY, novMinZ, novMaxZ), max_globina, tr_globina + 1))

    return okvir

def presek_z_bvh(T0, smer, okvir):
    #Algoritem za iskanje preseka s hierarhijo očrtanih okvirjev
    parametri = {}

    hit, tmin, tmax = aabb(T0, smer, okvir.minmax)
    global countAABB
    countAABB += 1

    if hit:
        if len(okvir.otroci) == 0:
            parametri |= {(tmin, tmax): okvir.parametri}
        for o in okvir.otroci:
            parametri |= presek_z_bvh(T0, smer, o)
    return parametri

def preveri_senco(par: Conf, X, luc_pr):
    #Algoritem za preverjanje, ali smo v senci
    global countTris
    preverjeni = set()
    novi_parametri = {(0, 0): par.parametri}
    if (par.bvh is not None):
        novi_parametri = OrderedDict(sorted(presek_z_bvh(X, luc_pr, par.bvh).items()))
    for _, parametri in novi_parametri.items():
        for p in parametri:
            if not p.idx in preverjeni:
                hit2, tr_X2, _, _ = tri(par.luc, -luc_pr, p)
                preverjeni.add(p.idx)
                countTris += 1
                if hit2 and (lin.norm(np.subtract(par.luc, tr_X2)) + 1e-8 < lin.norm(luc_pr)):
                    return 1
    return 0

def odboj(smer, T0, par: Conf, tr_globina=0):
    #Algoritem za sledenje žarkom
    X = None
    gradF = None
    CLR = None
    najblizji = np.inf
    senca = 0

    if tr_globina == par.max_globina:
        return X, gradF, CLR, najblizji, senca

    novi_parametri = {(0, 0): par.parametri}
    if (par.bvh is not None):
        novi_parametri = OrderedDict(sorted(presek_z_bvh(T0, smer, par.bvh).items()))

    #Če odkomentiramo ta del, nam program vrne prileganje hierarhije očrtanih okvirjev na motiv
    # if sum(map(len, novi_parametri.values())) > 0:
    #     return X, gradF, [100, 100, 100], najblizji, senca
    # else:
    #     return X, gradF, CLR, najblizji, senca

    global countTris
    preverjeni = set()
    oldMM = (np.inf, np.inf)
    for mm, parametri in novi_parametri.items():
        if najblizji == np.inf or oldMM[1] >= mm[0]:
            for p in parametri:
                if not p.idx in preverjeni:
                    hit, tr_X, tr_gradF, tr_CLR = tri(T0, smer, p)
                    preverjeni.add(p.idx)
                    countTris += 1
                    if hit:
                        oldMM = mm
                        oddaljenost = lin.norm(np.subtract(tr_X, T0))
                        if oddaljenost < najblizji:
                            najblizji = oddaljenost
                            X = tr_X
                            gradF = tr_gradF
                            CLR = tr_CLR
    
    if najblizji != np.inf:
        n = gradF / lin.norm(gradF)
        nova_smer = smer - 2 * (np.dot(smer, n))*n
        luc_pr = np.subtract(par.luc, X)

        if (par.sence):
            senca = preveri_senco(par, X, luc_pr)

        if senca == 0:
            cos = np.dot(luc_pr, nova_smer) / (lin.norm(luc_pr) * lin.norm(nova_smer))
            cos = max(cos, 0)
            CLR = CLR * 0.4 + (np.array([255, 255, 255]) * cos**5) / (lin.norm(luc_pr) / 2) * par.moc
        else:
            CLR = np.subtract(CLR, (np.array([50, 50, 50]))) / (lin.norm(luc_pr) / 2)

        CLR = np.minimum(CLR, [255, 255, 255])
        CLR = np.maximum(CLR, [0, 0, 0])

        _, _, rekCLR, rekNorm, _ = odboj(nova_smer, X, par, tr_globina + 1)

        if rekNorm != np.inf:
            utez1 = 1 / najblizji**2
            utez2 = 1 / (rekNorm + najblizji)**2
            s = utez1 + utez2
            utez1 = utez1 / s
            utez2 = utez2 / s
            CLR = CLR * utez1 + rekCLR * utez2

    return X, gradF, CLR, najblizji, senca


def raytracing(par: Conf):
    t = time.time()

    visina, sirina = par.loc

    zaslon = np.zeros((visina, sirina, 3))
    shadows = np.zeros((visina, sirina))
    dist = 0

    #za vsako točko na zaslonu
    for y in range(0, visina):
        for x in range(0, sirina):
            #platno je ravnina y = 0
            pix = [-par.viewport + 2*par.viewport/sirina * x, 0, par.viewport - 2*par.viewport/visina * y]
            
            #žarek kot parametrična premica
            smer = np.subtract(pix, par.T0)

            #rekurzivno preverjanje odbojev
            X, _, CLR, _, senca = odboj(smer, par.T0, par)                   
            if senca == 1:
                shadows[y, x] = 1

            if CLR is None:
                zaslon[y, x, :] = par.BG
            else:
                zaslon[y, x, :] = CLR
                dist += lin.norm(X - par.T0)

        print(f"Completed row {y + 1} of {visina}")
    elapsed = time.time() - t
    print("Raytracing time taken:", elapsed)

    ozadje = 0
    for y in range(visina):
        for x in range(sirina):
            if (zaslon[y, x, :] == par.BG).all():
                ozadje += 1
    print("Točke v barvi ozadja:", ozadje)
    print("Preverjenih trikotnikov:", countTris)
    print("Preverjenih okvirjev:", countAABB)
    print("Povprečna oddaljenost:", dist / (visina * sirina))

    #Laplacevo glajenje slik
    #Blaž Erzar
    if par.glad:
        zaslon2 = np.copy(zaslon)
        for y in range(1, visina - 1):
            for x in range(1, sirina - 1):
                if (zaslon[y, x, :] == par.BG).all():
                    #Vsaka točka z barvo ozadja postane povprečje svojih štirih sosedov
                    zaslon[y, x, :] = (zaslon2[y - 1, x, :] + zaslon2[y + 1, x, :] + zaslon2[y, x - 1, :] + zaslon2[y, x + 1, :]) / 4
    
    # duration = 500  # milliseconds
    # freq = 440  # Hz
    # winsound.Beep(freq, duration)

    zaslon /= 256
    imshow(zaslon)
    # imshow(shadows, cmap="gray")
    axis("off")
    show()


def main():
    par = Conf()

    #Naložimo podatke
    with open(sys.argv[1]) as f:
        data = json.load(f)

    objekti = data["objekti"]

    par.loc = data["loc"]
    par.luc = data["luc"]
    par.moc = data["luc_moc"]
    par.T0 = data["T0"]
    par.BG = data["BG"]
    par.glad = data["glad"]
    par.viewport = data["viewport"]
    zgradiBvh = data["bvh"]
    zgradiBvh2 = data["bvh2"]
    zgradiBvh3 = data["bvh3"]
    barve = data["barve"]
    par.sence = data["sence"]
    par.max_globina = data["max_odbojev"]

    minmax = []

    vec = [0, -1, 0]
    tmp = np.copy(par.T0)
    tmp[2] = 0
    cosAlpha = np.dot(vec, tmp) / (lin.norm(vec) * lin.norm(tmp))
    alpha = np.arccos(cosAlpha)
    sinAlpha = np.sin(alpha)

    Rz = np.array([ [cosAlpha, -sinAlpha, 0],
                    [sinAlpha, cosAlpha, 0],
                    [0, 0, 1]])

    tmp = (Rz @ np.copy(par.T0)[:, np.newaxis]).flatten()
    tmp[0] = 0
    cosBeta = np.dot(vec, tmp) / (lin.norm(vec) * lin.norm(tmp))
    beta = np.arccos(cosBeta)
    sinBeta = np.sin(beta)

    Rx = np.array([ [1, 0, 0],
                    [0, cosBeta, -sinBeta],
                    [0, sinBeta, cosBeta]])
    Rot = Rx @ Rz
    par.T0 = (Rot @ np.copy(par.T0)[:, np.newaxis]).flatten()
    par.luc = (Rot @ np.copy(par.luc)[:, np.newaxis]).flatten()

    parseTimer = time.time()
    VM = {}
    NM = {}
    idxV = 1
    idxN = 1

    idxF = 0
    idx = 0
    flagC = False

    meje = Meje()
    oMeje = Meje()
    oPar = []
    oMinmax = []
    oVM = {}

    first = True
    if zgradiBvh2 or zgradiBvh3:
        par.bvh = Okvir([], Meje(), [])

    with open(objekti) as p:
        for line in p:
            vrstica = line.rstrip().split(" ")

            #Tip vrstice je ime novega objekta
            if vrstica[0] == "o":
                if zgradiBvh2 and not first:
                    par.bvh.otroci.append(naredi_bvh(oPar, oMinmax, oMeje, par.max_bvh_glob))

                if zgradiBvh3 and not first:
                    if (len(oVM) >= 100):
                        oOkvir = Okvir([], oMeje, oPar)
                        mm_kmeans = bvh_kmeans(oVM)
                        for mm in mm_kmeans:
                            oOkvir.otroci.append(naredi_bvh(oPar, oMinmax, mm, par.max_bvh_glob))
                        par.bvh.otroci.append(oOkvir)
                    else:
                        par.bvh.otroci.append(naredi_bvh(oPar, oMinmax, oMeje, par.max_bvh_glob))

                oMeje = Meje()
                oPar = []
                oMinmax = []
                oVM = {}
                first = False

            #Tip vrstice je oglišče
            if vrstica[0] == "v":
                #Rotacija oglišč okrog z osi glede na začetno točko
                pos = (Rot @ [[float(vrstica[1])], [float(vrstica[2])], [float(vrstica[3])]]).flatten()
                VM[idxV] = pos
                oVM[idxV] = pos

                #Zapomnimo si meje objekta
                meje.posodobi(pos)
                idxV += 1

                oMeje.posodobi(pos)

                #Zagotovimo, da ima vsak objekt na sliki svojo barvo
                if flagC:
                    idxF += 1
                    flagC = False
            #Tip vrstice je normala
            if vrstica[0] == "vn":
                NM[idxN] = (Rot @ [[float(vrstica[1])], [float(vrstica[2])], [float(vrstica[3])]]).flatten()
                idxN += 1
            #Tip vrstice je ploskev
            if vrstica[0] == "f":
                flagC = True
                a = list(map(int, [vrstica[1].split("/")[i] for i in [0, 2]]))
                b = list(map(int, [vrstica[2].split("/")[i] for i in [0, 2]]))
                c = list(map(int, [vrstica[3].split("/")[i] for i in [0, 2]]))
                Va = VM[a[0]]
                Vb = VM[b[0]]
                Vc = VM[c[0]]
                
                novParameter = Parameter(np.array(barve[idxF % len(barve)]), Va, Vb, Vc, NM[a[1]], NM[b[1]], NM[c[1]], idx)
                par.parametri.append(novParameter)
                oPar.append(novParameter)

                novMinmax = Meje(min(Va[0], Vb[0], Vc[0]), max(Va[0], Vb[0], Vc[0]),\
                                min(Va[1], Vb[1], Vc[1]), max(Va[1], Vb[1], Vc[1]),\
                                min(Va[2], Vb[2], Vc[2]), max(Va[2], Vb[2], Vc[2]))
                minmax.append(novMinmax)
                oMinmax.append(novMinmax)
                
                idx += 1

    parseElapsed = time.time() - parseTimer
    print("Parse time taken:", parseElapsed)

    bvhTimer = time.time()
    if zgradiBvh:
        par.bvh = naredi_bvh(par.parametri, minmax, meje, par.max_bvh_glob)
        # par.bvh.level_order_walk()

    if zgradiBvh2:
        par.bvh.otroci.append(naredi_bvh(oPar, oMinmax, oMeje, par.max_bvh_glob))
        par.bvh.minmax = meje
        # par.bvh.level_order_walk()

    if zgradiBvh3:
        if (len(oVM) >= 100):
            oOkvir = Okvir([], oMeje, oPar)
            mm_kmeans = bvh_kmeans(oVM)
            for mm in mm_kmeans:
                oOkvir.otroci.append(naredi_bvh(oPar, oMinmax, mm, par.max_bvh_glob))
            par.bvh.otroci.append(oOkvir)
        else:
            par.bvh.otroci.append(naredi_bvh(oPar, oMinmax, oMeje, par.max_bvh_glob))
        par.bvh.minmax = meje

    bvhElapsed = time.time() - bvhTimer
    print("BVH time taken:", bvhElapsed)

    raytracing(par)


if __name__ == "__main__":
    main()