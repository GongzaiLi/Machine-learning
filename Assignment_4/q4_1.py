import hashlib
import numpy as np
from scipy.spatial import distance as sdist

def pseudo_random(seed=0xdeadbeef):
    """generate an infinite stream of pseudo-random numbers"""
    state = (0xffffffff & seed)/0xffffffff
    while True:
        h = hashlib.sha256()
        h.update(bytes(str(state), encoding='utf8'))
        bits = int.from_bytes(h.digest()[-8:], 'big')
        state = bits >> 32
        r = (0xffffffff & bits)/0xffffffff
        yield r


def cluster_points(centroids, dataset):
    clusters = [_ for _ in range(len(centroids))]
    closest = closest_centroid(dataset, centroids)
    for k in range(len(centroids)):
        clusters[k] = dataset[closest == k]
    return clusters


def separation(clusters):
    min_intercluster_dists = []
    for i, c1 in enumerate(clusters):
        for j, c2 in enumerate(clusters):
            if i != j:
                print(c1, c2)
                print(sdist.cdist(c1, c2).min(), 11111111111111111111111)
                min_intercluster_dists.append(sdist.cdist(c1, c2).min())


    return sum(min_intercluster_dists) / len(clusters)


def compactness(clusters):
    max_intracluster_dists = []
    for c in clusters:
        intracluster_dists = []
        for p1 in c:
            for p2 in c:
                intracluster_dists.append(np.linalg.norm(p1-p2))
        max_intracluster_dists.append(max(intracluster_dists))
    return sum(max_intracluster_dists) / len(clusters)


def goodness(clusters):
    return separation(clusters) / compactness(clusters)


def generate_random_vector(bounds, r):
    return np.array([(high - low) * next(r) + low for low, high in bounds])


def k_means_random_restart(dataset, k, restarts, seed=None):
    bounds = list(zip(np.min(dataset, axis=0), np.max(dataset, axis=0)))
    r = pseudo_random(seed=seed) if seed else pseudo_random()
    models = []
    for _ in range(restarts):
        random_centroids = tuple(generate_random_vector(bounds, r)
                                 for _ in range(k))
        new_centroids = k_means(dataset, random_centroids)
        clusters = cluster_points(new_centroids, dataset)
        if any(len(c) == 0 for c in clusters):
            continue
        models.append((goodness(clusters), new_centroids))
    return max(models, key=lambda x: x[0])[1]



def closest_centroid(points, centroids):
    """returns an array containing the index to the nearest centroid for each point"""
    distances = np.sqrt(((points - centroids[:, np.newaxis])**2).sum(axis=2))
    return np.argmin(distances, axis=0)


def move_centroids(points, closest, centroids):
    """returns the new centroids assigned from the points closest to them"""
    new_centroids = np.empty_like(centroids)
    #cluster = [ _ for _ in range(len(centroids))]
    for k in range(len(centroids)):
        if len(points[closest==k]) > 0:
            #print("points[closet]",points[closest], "poinst[k]",points[k],"points[closet=k]",points[closest ==k])
            new_centroids[k] = points[closest == k].mean(axis=0)
            #cluster[k]=points[closest==k]
            #print("cluster[k]",cluster[k])
           # print("cluster",cluster)
        else:
            new_centroids[k] = centroids[k]
   # print("new_centriods",new_centroids)
    return new_centroids


def k_means(dataset, centroids):
    centroidss = np.asarray(centroids)
    while True:
        closest = closest_centroid(dataset, centroidss)
        new_centroids = move_centroids(dataset, closest, centroidss)
        if np.all(new_centroids == centroidss):
            break
        centroidss = new_centroids
    return new_centroids

if __name__ == '__main__':
    dataset = np.array([
        [0.1, 0.1],
        [0.2, 0.2],
        [0.8, 0.8],
        [0.9, 0.9]
    ])
    centroids = k_means_random_restart(dataset, k=2, restarts=5)

    for c in sorted([f"{x:8.3}" for x in centroid] for centroid in centroids):
        print(" ".join(c))
