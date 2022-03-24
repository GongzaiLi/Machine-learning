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
            feature = ()
        partition_dataset[feature] = partition_dataset.get(feature, []) + [(data, label)]

    def separator(feature_vector):
        if len(feature_vector) == 0:
            return 0
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
    if len(p) == 1:
        return float('inf')
    H = [criterion(data) for data in p]
    Qm_size = len(dataset)  # the training data available at node m
    impurity = sum((len(p_data) / Qm_size) * H[index] for index, p_data in enumerate(p))
    return impurity


def train_tree(dataset, criterion):
    """
    :param dataset:     a list of pairs,
                        where the first element in each pair is a feature vector,
                        and the second is a classification.
    :param criterion:   The criterion function evaluates a dataset for a specific impurity measure
    :return:
    """
    classes = get_classes(dataset)
    if len(classes) == 1:  # if all examples are in one class:
        return DTNode(classes[0])  # return a leaf node with that class label;

    elif len(dataset[0]) == 0:  # issues question  # elif the set of features is empty:

        leaf_node = get_most_common_label(dataset)
        return DTNode(leaf_node)
    else:
        feature_vector = dataset[0][0]  # 取第一个 dateset 中 x
        impurities = []
        for index in range(len(feature_vector)):
            impurities.append(get_impurity(dataset, criterion, index))

        feature_index = impurities.index(min(impurities))
        separator, partition = partition_by_feature_value(dataset, feature_index)

        node_R = DTNode(separator)  # create a new decision (condition) node R;
        node_R.children = []
        for p in partition:
            if len(p[0][0]) == 0:
                leaf_node = get_most_common_label(dataset)
                node_R.children.append(DTNode(leaf_node))
            else:
                node_R.children.append(train_tree(p, criterion))
        return node_R


if __name__ == "__main__":
    dataset = []
    with open('nursery.data', 'r') as f:
        for line in f.readlines():
            features = line.strip().split(",")
            dataset.append((tuple(features[:-1]), features[-1]))
    t = train_tree(dataset, misclassification)
    print(all(t.predict(d) == out for (d, out) in dataset))

    dataset = [
        (("Sunny", "Hot", "High", "Weak"), False),
        (("Sunny", "Hot", "High", "Strong"), False),
        (("Overcast", "Hot", "High", "Weak"), True),
        (("Rain", "Mild", "High", "Weak"), True),
        (("Rain", "Cool", "Normal", "Weak"), True),
        (("Rain", "Cool", "Normal", "Strong"), False),
        (("Overcast", "Cool", "Normal", "Strong"), True),
        (("Sunny", "Mild", "High", "Weak"), False),
        (("Sunny", "Cool", "Normal", "Weak"), True),
        (("Rain", "Mild", "Normal", "Weak"), True),
        (("Sunny", "Mild", "Normal", "Strong"), True),
        (("Overcast", "Mild", "High", "Strong"), True),
        (("Overcast", "Hot", "Normal", "Weak"), True),
        (("Rain", "Mild", "High", "Strong"), False),
    ]
    t = train_tree(dataset, misclassification)
    print(t.predict(("Overcast", "Cool", "Normal", "Strong")))
    print(t.predict(("Sunny", "Cool", "Normal", "Strong")))
