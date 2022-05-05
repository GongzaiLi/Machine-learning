import hashlib
import numpy as np


def pseudo_random(seed=0xdeadbeef):
    """generate an infinite stream of pseudo-random numbers"""
    state = (0xffffffff & seed) / 0xffffffff
    while True:
        h = hashlib.sha256()
        h.update(bytes(str(state), encoding='utf8'))
        bits = int.from_bytes(h.digest()[-8:], 'big')
        state = bits >> 32
        r = (0xffffffff & bits) / 0xffffffff
        yield r


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



def find_closest_centroid(points, centroids):
    """
    For a current set of cluster means, assign each observation as:
    euclidean distance   https://en.wikipedia.org/wiki/Euclidean_distance
    :param points: dataset
    :param centroids: array is a single centroid vector
    :return: a list about index of each point the closest centroid
    """
    closest_centroid = []
    for point in points:
        distances = []
        for centroid in centroids:
            distance = np.sqrt(sum(np.subtract(point, centroid) ** 2))  # euclidean distance
            distances.append(distance)
        closest_centroid.append(np.argmin(distances))  # find min element index
    return np.array(closest_centroid)


def reestimate_cluster_centroids(points, current_centroids, closest_centroid):
    """
    For a given assignment C, compute the cluster means mk:
    :param points: dataset
    :param current_centroids:  current set of centroids
    :param closest_centroid: a list about index of each point the closest centroid
    :return: new_centroids
    """
    new_centroids = np.copy(current_centroids)

    for k in range(len(current_centroids)):
        cluster_k_set = np.array([points[i] for i in range(len(closest_centroid)) if closest_centroid[i] == k])
        if len(cluster_k_set) > 0:
            # numpy mean -> https://numpy.org/doc/stable/reference/generated/numpy.mean.html
            new_centroids[k] = cluster_k_set.mean(axis=0)
        # else:  # does not need
        #     new_centroids[k] = centroids[k]
    return new_centroids


def k_means(dataset, centroids):
    """
    :param dataset: A dataset is a numpy array, where each row is a feature vector.
    :param centroids: array is a single centroid vector
    :return: current_centroids
    """
    current_centroids = np.copy(centroids)
    while True:
        closest_centroid = find_closest_centroid(dataset, current_centroids)
        new_centroids = reestimate_cluster_centroids(dataset, current_centroids, closest_centroid)
        if np.all(current_centroids == new_centroids):  # compare all np all metricx
            break
        current_centroids = new_centroids
    return current_centroids

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
