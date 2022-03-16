"""
Write a function partition_by_feature_value(dataset, feature_index) which takes as parameters a dataset and a feature
index and returns a pair, where the first element is a "separator" function, and the second element is the partitioned dataset.
编写一个函数partition_by_feature_value(dataset, feature_index)，该函数将一个数据集和一个特征索引作为参数，并返回一个对，其中第一个元素是一个 "分离器 "函数，第二个元素是分割后的数据集。

A dataset is a list of pairs (x, y), where x is a feature vector, and y is a classification (label). For this quiz,
we assume they are both categorical. A partitioned dataset for feature index i is a list of datasets, where each feature
vector x in each dataset has the same x[i] value.
一个数据集是一个对（x，y）的列表，其中x是一个特征向量，y是一个分类（标签）。在这次测验中，我们假设它们都是分类的。一个针对特征索引i的分区数据集是一个数据集的列表，其中每个数据集中的每个特征向量x都有相同的x[i]值。

A separator function takes a feature vector, and returns the index of the partition of the dataset that feature vector
would belong to.
一个分离器函数接收一个特征向量，并返回该特征向量所属的数据集的分区索引。
"""


# def partition_by_feature_value(data,index):
#     features = []
#     d = {}
#     for (v, c) in data:
#         if d.get(v[index]) is None:
#             d[v[index]] = [(v, c)]
#             features.append(v[index])
#         else:
#             d[v[index]].append((v, c))
#     print(features, 111111111111111)
#     separator = lambda f: features.index(f[index])
#     return separator, list(d.values())


# 按特征值分区 功能是分类dataset中指定的feature
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
        return list(p.keys()).index(v)
    print(p, "here is p")
    return f, list(p.values())


if __name__ == "__main__":
    print("q2")
    # separator
    print('09', '12', '2016', sep='-')

    from pprint import pprint

    dataset = [
        ((True, True), False),
        ((True, False), True),
        ((False, True), True),
        ((False, False), False),
    ]
    f, p = partition_by_feature_value(dataset, 0)
    pprint(sorted(sorted(partition) for partition in p))

    partition_index = f((True, True))
    # Everything in the "True" partition for feature 0 is true
    print(all(x[0] == True for x, c in p[partition_index]))
    partition_index = f((False, True))
    # Everything in the "False" partition for feature 0 is false
    print(all(x[0] == False for x, c in p[partition_index]))

    from pprint import pprint

    dataset = [
        (("a", "x", 2), False),
        (("b", "x", 2), False),
        (("a", "y", 5), True),
    ]
    f, p = partition_by_feature_value(dataset, 1)
    pprint(sorted(sorted(partition) for partition in p))
    partition_index = f(("a", "y", 5))
    print(partition_index, 2222222222)
    # everything in the "y" partition for feature 1 has a y
    print(all(x[1] == "y" for x, c in p[partition_index]))
