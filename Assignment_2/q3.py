"""
Write three functions misclassification(dataset), gini(dataset), and entropy(dataset) that take a dataset
(list of (x, y) pairs) and calculate the impurity of the dataset.

misclassification is defined as 1 - maxk pk.
gini is defined as ∑k pk(1 - pk).
entropy is defined as -∑k pk log(pk).
"""
import math


def get_pmk(k, dataset):  # find all k possible values
    Qm = len(dataset)
    pmk = [x for x, y in dataset if y == k]
    return (1 / Qm) * len(pmk)


def find_ks(dataset):
    return {y for _, y in dataset}


def misclassification(dataset):
    pmks = []
    ks = find_ks(dataset)
    for k in ks:
        pmk = get_pmk(k, dataset)
        pmks.append(pmk)
    return 1 - max(pmks)


def gini(dataset):
    ans = []
    ks = find_ks(dataset)
    for k in ks:
        pmk = get_pmk(k, dataset)
        ans.append(pmk * (1 - pmk))
    return sum(ans)


def entropy(dataset):
    ans = []
    ks = find_ks(dataset)
    for k in ks:
        pmk = get_pmk(k, dataset)
        ans.append(pmk * math.log(pmk, 2))  # Base Default is 'e' math.log(x, base)
    return -1 * sum(ans)


if __name__ == "__main__":
    print("Question 3")

    # data = [
    #     ((False, False), False),
    #     ((False, True), True),
    #     ((True, False), True),
    #     ((True, True), False)
    # ]
    # print("{:.4f}".format(misclassification(data)))
    # print("{:.4f}".format(gini(data)))
    # print("{:.4f}".format(entropy(data)))

    data = [
        ((0, 1, 2), 1),
        ((0, 2, 1), 2),
        ((1, 0, 2), 1),
        ((1, 2, 0), 3),
        ((2, 0, 1), 3),
        ((2, 1, 0), 3)
    ]
    print("{:.4f}".format(misclassification(data)))
    print("{:.4f}".format(gini(data)))
    print("{:.4f}".format(entropy(data)))

