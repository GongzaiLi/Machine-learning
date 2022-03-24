def get_proportion(classification, data):
    total = 0
    for _, c in data:
        if c == classification:
            total += 1
    return total / len(data)


def get_classes(data):
    return set([d[-1] for d in data])


def misclassification(data):
    pks = []
    for k in get_classes(data):
        pks.append(get_proportion(k, data))
    return 1 - max(pks)

"""
[0.5, 0.5] 1111111
[0.5, 0.5] 1111111
[0.5, 0.5] 1111111
[0.5, 0.5] 1111111
[1.0] 1111111
[1.0] 1111111
[1.0] 1111111
[1.0] 1111111
"""
# def gini(data):
#     H = 0
#     for k in get_classes(data):
#         pk = get_proportion(k, data)
#         H += pk * (1 - pk)
#     return H
#
#
# def entropy(data):
#     H = 0
#     for k in get_classes(data):
#         pk = get_proportion(k, data)
#         if pk != 0:
#             H += pk * math.log(pk)
#     return -H

def partition_by_feature_value(data, index):
    features = []
    d = {}
    for (v, c) in data:
        if d.get(v[index]) is None:
            d[v[index]] = [(v, c)]
            features.append(v[index])
        else:
            d[v[index]].append((v, c))
    separator = lambda f: features.index(f[index])
    return separator, list(d.values())


class DTNode:
    def __init__(self, decision):
        self.decision = decision
        self.children = None

    def predict(self, feature_vector):
        if callable(self.decision):
            return self.children[self.decision(feature_vector)].predict(feature_vector)
        return self.decision

    # def leaves(self):
    #     if len(self.children) == 0:
    #         return 1
    #     return sum([child.leaves() for child in self.children])

def get_impurity(criterion, k, data):
    separator, partition = partition_by_feature_value(data, k)
    print(k, 1111111111111)
    if len(partition) == 1:
        return float('-inf')
    return sum([(len(p)/len(data)) * criterion(p) for p in partition])

"""

[[((True, True), False), ((True, False), True)], [((False, True), True), ((False, False), False)]] 1111111111111
[[((True, True), False), ((False, True), True)], [((True, False), True), ((False, False), False)]] 1111111111111
[[((True, True), False), ((True, False), True)]] 1111111111111
[[((True, True), False)], [((True, False), True)]] 1111111111111
[[((False, True), True), ((False, False), False)]] 1111111111111
[[((False, True), True)], [((False, False), False)]] 1111111111111
"""

def train_tree(data, criterion):
    classes = list(set([d[-1] for d in data]))
    if len(classes) == 1: # if all examples are in one class
        return DTNode(data[0][1])   # return a leaf node with that class label
    elif len(data[0][0]) == 0:  # if the set of features is empty
        proportions = [get_proportion(k, data) for k in classes]
        most_common_label = classes[proportions.index(max(proportions))]
        return DTNode(most_common_label)  # return a leaf node with the most common class label
    else:
        features = data[0][0]
        impurities = [get_impurity(criterion, k, data) for k in range(len(features))]
        feature_index = impurities.index(max(impurities))
        separator, partition = partition_by_feature_value(data, feature_index)
        #print("partition", partition)
        node = DTNode(separator)
        node.children = [train_tree(p, criterion) for p in partition]
        return node

if __name__ == "__main__":
    print("Question 4")

    # dataset = [
    #     ([], False),
    #     ([], True),
    #     # ((True, True), False),
    #     # ((True, False), True),
    #     # ((False, True), True),
    #     # ((False, False), False)
    # ]
    # t = train_tree(dataset, misclassification)
    # print(t.predict((True, False)))
    # print(t.predict((False, False)))

    dataset = []
    with open('car.data', 'r') as f:
        for line in f.readlines():
            out, *features = line.strip().split(",")
            dataset.append((tuple(features), out))
    t = train_tree(dataset, misclassification)


