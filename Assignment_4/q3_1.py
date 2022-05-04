import numpy as np


def closest_centroid(points, centroids):
    """returns an array containing the index to the nearest centroid for each point"""
    distances = np.sqrt(((points - centroids[:, np.newaxis]) ** 2).sum(axis=2))
    print(distances, "++++++++++++++++++++++")
    return np.argmin(distances, axis=0)


def move_centroids(points, closest, centroids):
    """returns the new centroids assigned from the points closest to them"""
    new_centroids = np.empty_like(centroids)
    print(new_centroids, 3333333333333333)
    # cluster = [ _ for _ in range(len(centroids))]
    for k in range(len(centroids)):
        if len(points[closest == k]) > 0:
            print(points[closest == k], closest, k, 22222222222222222222222)
            # print("points[closet]",points[closest], "poinst[k]",points[k],"points[closet=k]",points[closest ==k])
            new_centroids[k] = points[closest == k].mean(axis=0)
            print(points[closest == k].mean(axis=0), "------------------------")
            # cluster[k]=points[closest==k]
            # print("cluster[k]",cluster[k])
        # print("cluster",cluster)
        else:
            new_centroids[k] = centroids[k]
    # print("new_centriods",new_centroids)
    return new_centroids


def k_means(dataset, centroids):
    centroidss = np.asarray(centroids)
    while True:
        closest = closest_centroid(dataset, centroidss)
        print(closest, 111111)
        new_centroids = move_centroids(dataset, closest, centroidss)
        if np.all(new_centroids == centroidss):
            break
        centroidss = new_centroids
    return centroidss


if __name__ == '__main__':
    dataset = np.array([
        [0.1, 0.1],
        [0.2, 0.2],
        [0.8, 0.8],
        [0.9, 0.9]
    ])
    centroids = (np.array([0., 0.]), np.array([1., 1.]))
    print(dataset)
    print(centroids)
    for c in k_means(dataset, centroids):
        print(c)
