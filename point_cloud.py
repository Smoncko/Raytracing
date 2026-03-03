import matplotlib.pyplot as plt
import sys
import json
from sklearn.cluster import KMeans
import time
import numpy as np

def main():
    with open(sys.argv[1]) as f:
        data = json.load(f)

    objekti = data["objekti"]
    Vx = []
    Vy = []
    Vz = []

    with open(objekti) as p:
        for line in p:
            tip = line.rstrip().split(" ")
            if tip[0] == "v":
                Vx.append(float(tip[1]))
                Vy.append(float(tip[2]))
                Vz.append(float(tip[3]))

    points = list(zip(Vx, Vy, Vz))


    ax = plt.axes(projection="3d")
    timer = time.time()
    kmeans = KMeans(n_clusters=11)
    kmeans.fit(points)
    print("KMeans time taken: ", time.time() - timer)
    print(len(kmeans.labels_))

    ax.scatter(Vx, Vy, Vz, c=kmeans.labels_)
    plt.show()

    # sse = {}
    # for k in range(2, 20):
    #     kmeans = KMeans(n_clusters=k).fit(points)
    #     sse[k] = kmeans.inertia_
    # plt.figure()
    # plt.plot(list(sse.keys()), list(sse.values()))
    # plt.xlabel("Number of clusters")
    # plt.ylabel("SSE")
    # plt.show()


if __name__ == "__main__":
    main()