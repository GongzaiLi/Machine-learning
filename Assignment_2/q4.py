"""
Define a function train_tree(dataset, criterion) that takes a dataset and a criterion,
constructs a decision tree that fits the data, and returns a DTNode object that is the root of the tree.

The dataset is a list of pairs, where the first element in each pair is a feature vector, and the second is a classification.
All the features are categorical. The criterion function evaluates a dataset for a specific impurity measure (e.g. entropy).

Please also include your implementation of the function partition_by_feature_value,
the function misclassification, and the class DTNode. These will be used in the test cases.
"""
"""
DTree(examples, features) # returns a tree
    if all examples are in one class:
        return a leaf node with that class label;
    elif the set of features is empty:
        return a leaf node with the most common class label in examples;
    else:
        create a new decision (condition) node R;
        pick a categorical feature F (or a numeric feature and a threshold);
        for each possible outcome v_i of R:
            add an out-going edge E_v_i to node R;
            let examples_i be the subset of examples that result in outcome v_i;
            if examples_i is empty:
                attach to E_v_i a leaf node (label) that is the most common in examples;
            else:
                attach to E_v_i the result of DTree(examples_i, features \ {F});
        return the subtree rooted at R.
"""


class DTNode:
    def __init__(self, decision):
        self.decision = decision
        self.children = []

    def predict(self, feature_vector):
        if not callable(self.decision):
            return self.decision
        else:
            leaf_index = self.decision(feature_vector)
            next_node = self.children[leaf_index]
            return next_node.predict(feature_vector)


def partition_by_feature_value(dataset, feature_index):
    """
    :param dataset: a list of pairs (x, y) x is a feature vector, and y is a classification (label)
    :param feature_index:
    :return: pair the first element is a "separator" function, and the second element is the partitioned dataset.
    """
    p = {}
    for x, y in dataset:
        vector = x[feature_index]
        p[vector] = p.get(vector, []) + [(x, y)]  # 分类 把这个x里的feature vector 分类出来

    def f(feature_vector):
        # 找到对应的特征 储存位置
        v = feature_vector[feature_index]
        return list(p.keys()).index(v)  # partition_index

    return f, list(p.values())


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


def get_classes(dataset):
    classes = []
    for _, label in dataset:
        if label not in classes:
            classes.append(label)
    return classes


def get_impurity(criterion, feature_index, dataset):  # G(Qm, Theta)
    Qm = len(dataset)
    G_Qm_theta = []

    _, partitions = partition_by_feature_value(dataset, feature_index)
    if len(partitions) == 1:
        return float('-inf')

    for p in partitions:
        H_Qm_theta = criterion(p)
        G_Qm_theta.append((len(p) / Qm) * H_Qm_theta)
    return sum(G_Qm_theta)


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

    elif len(dataset[0]) == 0:  # elif the set of features is empty:
        all_class_label_pmk = [get_pmk(k, dataset) for k in classes]
        max_class_label_index = all_class_label_pmk.index(max(all_class_label_pmk))
        max_class_label = classes[max_class_label_index]

        return DTNode(max_class_label)  # return a leaf node with the most common class label in examples;
    else:
        feature_vector = dataset[0][0]  # 取第一个 dateset 中 x
        impurities = []
        for feature_index in range(len(feature_vector)):
            impurities.append(get_impurity(criterion, feature_index, dataset))

        feature_index = impurities.index(max(impurities))

        separator, partition = partition_by_feature_value(dataset, feature_index)

        next_node = DTNode(separator)
        next_node.children = [train_tree(p, criterion) for p in partition]
        return next_node


if __name__ == "__main__":
    print("Question 4")

    # dataset = [
    #     ((True, True), False),
    #     ((True, False), True),
    #     ((False, True), True),
    #     ((False, False), False)
    # ]
    # t = train_tree(dataset, misclassification)
    # print(t.predict((True, False)))
    # print(t.predict((False, False)))

    dataset = [
        (("Sunny", "Hot", "High", "Weak"), False),
        # (("Sunny", "Hot", "High", "Strong"), False),
        (("Overcast", "Hot", "High", "Weak"), True),
        # (("Rain", "Mild", "High", "Weak"), True),
        # (("Rain", "Cool", "Normal", "Weak"), True),
        # (("Rain", "Cool", "Normal", "Strong"), False),
        # (("Overcast", "Cool", "Normal", "Strong"), True),
        # (("Sunny", "Mild", "High", "Weak"), False),
        (("Sunny", "Cool", "Normal", "Weak"), True),
        # (("Rain", "Mild", "Normal", "Weak"), True),
        # (("Sunny", "Mild", "Normal", "Strong"), True),
        # (("Overcast", "Mild", "High", "Strong"), True),
        # (("Overcast", "Hot", "Normal", "Weak"), True),
        # (("Rain", "Mild", "High", "Strong"), False),
    ]
    t = train_tree(dataset, misclassification)
    a = t.children
    print(a)
    print(a[0].children, "here 0")
    print(a[0].children[0].children, "here 0. 0")
    print(a[0].children[0].decision, "here 0. 0")
    print(a[0].children[1].children, "here 0. 1")
    print(a[0].children[1].decision, "here 0. 1")
    print(a[1].children, "here 1")
    print(a[1].decision, "here 1")
    print(t.predict(("Overcast", "a", "a", "a")))
    print(t.predict(("Sunny", "Cool", "a", "a")))
