import numpy as np
from scipy.spatial.distance import cdist
import sklearn.datasets
import sklearn.utils


def c_calcution(dataset, centroids):
    long = cdist(dataset, centroids, "euclidean")
    print(long, 11111111111111111111111)
    mindex = np.argmin(long, axis=1)

    cltr = []
    newcentroids = []

    for j in range(len(centroids)):
        n = np.where(mindex == j)
        cltr.append(dataset[n])

    for z in range(len(cltr)):
        if len(cltr[z]) != 0:
            newcentroids.append(np.mean(cltr[z], axis=0))
        else:
            newcentroids.append(np.array(centroids[z]))
    return newcentroids


def c_compare(before, new):
    ans = list(zip(before, new))
    comp = []
    for i, j in ans:
        if np.array_equal(i, j) == True:
            comp.append(True)
        else:
            comp.append(False)
    if all(comp) == True:
        return True
    else:
        return False


def k_means(dataset, centroids):
    newcentroids = c_calcution(dataset, centroids)

    while c_compare(centroids, newcentroids) != True:
        centroids = newcentroids
        newcentroids = c_calcution(dataset, newcentroids)

    return newcentroids

if __name__ == '__main__':
    dataset = np.array([
        [0.1, 0.1],
        [0.2, 0.2],
        [0.8, 0.8],
        [0.9, 0.9]
    ])
    centroids = (np.array([0., 0.]), np.array([1., 1.]))
    for c in k_means(dataset, centroids):
        print(c)