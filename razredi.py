import queue
import numpy as np

class Conf:
    T0 = []
    loc = []
    luc = []
    moc = 0
    bvh = None
    viewport = 0
    BG = [] 
    parametri = []
    glad = False
    max_globina = 1
    max_bvh_glob = 5
    sence = False

class Parameter:
    def __init__(self, barve, A, B, C, nA, nB, nC, idx):
        self.barve = barve
        self.A = A
        self.B = B
        self.C = C
        self.nA = nA
        self.nB = nB
        self.nC = nC
        self.idx = idx
    def __repr__(self):
        return f"Parameter\nBarve:{self.barve}\nA:{self.A} B:{self.B} C:{self.C}\nnA:{self.nA} nB:{self.nB} nC:{self.nC}"

class Okvir:
    def __init__(self, otroci, minmax, parametri):
        self.otroci = otroci
        self.minmax = minmax
        self.parametri = parametri
    def __repr__(self):
        return f"Okvir\nOtroci:{self.otroci}\nMinmax:{self.minmax}\nParam:{self.parametri}"

    def level_order_walk(self):
        q = queue.Queue()
        q.put(self)

        while not q.empty():
            front = q.get()
            # print(front)
            for o in front.otroci:
                q.put(o)
            if len(front.otroci) == 0:
                print(len(front.parametri))

class Meje:
    def __init__(self, minX=np.inf, maxX=-np.inf, minY=np.inf, maxY=-np.inf, minZ=np.inf, maxZ=-np.inf):
        self.minX = minX
        self.maxX = maxX
        self.minY = minY
        self.maxY = maxY
        self.minZ = minZ
        self.maxZ = maxZ
    def __repr__(self):
        return f"Meje: (minX={self.minX}, maxX={self.maxX}, minY={self.minY}, maxY={self.maxY}, minZ={self.minZ}, maxZ={self.maxZ})\n"

    def posodobi(self, noveMeje: list):
        self.minX = min(self.minX, noveMeje[0])
        self.maxX = max(self.maxX, noveMeje[0])
        self.minY = min(self.minY, noveMeje[1])
        self.maxY = max(self.maxY, noveMeje[1])
        self.minZ = min(self.minZ, noveMeje[2])
        self.maxZ = max(self.maxZ, noveMeje[2])