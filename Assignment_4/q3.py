"""
Assign each point in the training data to a class based on the "centroid" it is closest to.
Update the centroids to be the mean of the training data assigned to it.
arg  min 的意思是当这个function() 达到最小值时
"""

import numpy as np


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
    centroids = (np.array([0., 0.]), np.array([1., 1.]))
    for c in k_means(dataset, centroids):
        print(c)

    dataset = np.array([
        [0.125, 0.125],
        [0.25, 0.25],
        [0.75, 0.75],
        [0.875, 0.875]
    ])
    centroids = (np.array([0., 1.]), np.array([1., 0.]))
    for c in k_means(dataset, centroids):
        print(c)

    dataset = np.array([
        [0.1, 0.3],
        [0.4, 0.6],
        [0.1, 0.2],
        [0.2, 0.1]
    ])
    centroids = (np.array([2., 5.]),)
    for c in k_means(dataset, centroids):
        print(c)
