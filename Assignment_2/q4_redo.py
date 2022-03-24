class DTNode:
    def __init__(self, decision):
        self.decision = decision
        self.children = []

    def predict(self, feature_vector):
        if not callable(self.decision):
            return self.decision
        next_node_index = self.decision(feature_vector)
        next_node = self.children[next_node_index]
        return next_node.predict(feature_vector)


def partition_by_feature_value(dataset, feature_index):
    partition_dataset = {}
    for data, label in dataset:
        if len(data) != 0:
            feature = data[feature_index]
        else:
            feature = None
        partition_dataset[feature] = partition_dataset.get(feature, []) + [(data, label)]

    def separator(feature_vector):
        feature = feature_vector[feature_index]
        return list(partition_dataset.keys()).index(feature)

    return separator, list(partition_dataset.values())


def get_all_Pmk(dataset):
    ks = {y for _, y in dataset}
    Qm_size = len(dataset)  # the training data available at node m
    all_Pmk = []

    for k in ks:
        Pmk = [x for x, y in dataset if y == k]
        all_Pmk.append((1 / Qm_size) * len(Pmk))
    return all_Pmk


def misclassification(dataset):
    all_Pmk = get_all_Pmk(dataset)
    return 1 - max(all_Pmk)


def gini(dataset):
    all_Pmk = get_all_Pmk(dataset)
    return sum(pmk * (1 - pmk) for pmk in all_Pmk)


import math


def entropy(dataset):
    all_Pmk = get_all_Pmk(dataset)
    return -sum(pmk * math.log(pmk, 2) for pmk in all_Pmk)


def get_classes(dataset):
    classes = []
    for _, label in dataset:
        if label not in classes:
            classes.append(label)
    return classes


def get_most_common_label(dataset):
    all_labels = {}
    for _, y in dataset:
        all_labels[y] = all_labels.get(y, 0) + 1
    return max(all_labels, key=all_labels.get)  # return the key


def get_impurity(dataset, criterion, feature_index):
    _, p = partition_by_feature_value(dataset, feature_index)
    H = [criterion(data) for data in p]
    Qm_size = len(dataset)  # the training data available at node m
    impurity = sum((len(p_data) / Qm_size) * H[index] for index, p_data in enumerate(p))
    return impurity


def train_tree(dataset, criterion):  # criterion 准则
    classes = get_classes(dataset)
    features_number = 0
    if dataset and len(dataset[0]) == 2:
        features_number = len(dataset[0][0])

    def DTree(example, features_number):  # returns a tree
        if len(classes) == 0:
            return DTNode(classes[0])
        elif features_number == 0:
            leaf_node = get_most_common_label(example)
            return DTNode(leaf_node)
        else:
            feature_vector = example[0][0]  # 取第一个 dateset 中 x
            impurities = []
            for index in range(len(feature_vector)):
                impurities.append(get_impurity(example, criterion, index))

            # if impurities == []:
            #     leaf_node = get_most_common_label(example)
            #     return DTNode(leaf_node)

            feature_index = impurities.index(min(impurities))

            separator, partition = partition_by_feature_value(example, feature_index)

            features_number += 1
            node_R = DTNode(separator)  # create a new decision (condition) node R;
            node_R.children = []
            for p in partition:
                node_R.children.append(DTree(p, features_number))
            return node_R

    return DTree(dataset, features_number)


if __name__ == "__main__":
    # dataset = []
    # with open('car.data', 'r') as f:
    #     for line in f.readlines():
    #         out, *features = line.strip().split(",")
    #         dataset.append((tuple(features), out))
    # t = train_tree(dataset, misclassification)
    # print(all(t.predict(d) == out for (d, out) in dataset))

    # dataset = []
    # with open('nursery.data', 'r') as f:
    #     for line in f.readlines():
    #         features = line.strip().split(",")
    #         dataset.append((tuple(features[:-1]), features[-1]))
    # t = train_tree(dataset, misclassification)
    # print(all(t.predict(d) == out for (d, out) in dataset))

    dataset = [
        ((True, True), False),
        ((True, False), True),
        ((False, True), True),
        ((False, False), False)
    ]
    t = train_tree(dataset, misclassification)
    print(t.predict((True, False)))
    print(t.predict((False, False)))