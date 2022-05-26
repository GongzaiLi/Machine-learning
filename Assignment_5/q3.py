import sklearn.datasets
import sklearn.utils
import sklearn.tree

import hashlib
import numpy as np

def voting_ensemble(classifiers):
    def classifier_report(data):
        report = [classifier(data) for classifier in classifiers]
        return max(sorted(report), key=report.count) # sorts lowest asc 小到大
    return classifier_report



def pseudo_random(seed=0xDEADBEEF):
    """Generate an infinite stream of pseudo-random numbers"""
    state = (0xffffffff & seed) / 0xffffffff
    while True:
        h = hashlib.sha256()
        h.update(bytes(str(state), encoding='utf8'))
        bits = int.from_bytes(h.digest()[-8:], 'big')
        state = bits >> 32
        r = (0xffffffff & bits) / 0xffffffff
        yield r


def bootstrap(dataset, sample_size):
    random = pseudo_random()
    while True:
        new_sample = []
        for _ in range(sample_size): # new dataset size
            r = next(random)  # random everytime r
            random_index = int(r * len(dataset))
            new_sample.append(dataset[random_index])
        yield np.array(new_sample)

def bagging_model(learner, dataset, n_models, sample_size):
    """
    :param dataset: n * (d+1) each row is a new feature vector; the final column is the class.
    """
    classifiers = []
    new_dataset = bootstrap(dataset, sample_size)
    for _ in range(n_models):
        classifiers.append(learner(next(new_dataset)))
    return voting_ensemble(classifiers)



if __name__ == '__main__':
    iris = sklearn.datasets.load_iris()  # The iris dataset is a classic and very easy multi-class classification dataset.

    data, target = sklearn.utils.shuffle(iris.data, iris.target, random_state=1)  # 把数据洗牌
    train_data, train_target = data[:-5, :], target[:-5]  # 选取 train 数据
    test_data, test_target = data[-5:, :], target[-5:]  # 选取 test 数据
    dataset = np.hstack((train_data, train_target.reshape((-1, 1))))  # 把两个list合并 形成dataset


    def tree_learner(dataset):
        features, target = dataset[:, :-1], dataset[:, -1]  # https://www.w3schools.com/python/numpy/numpy_array_slicing.asp
        model = sklearn.tree.DecisionTreeClassifier(random_state=1).fit(features, target) # decision tree classifier
        return lambda v: model.predict(np.array([v]))[0]


    bagged = bagging_model(tree_learner, dataset, 50, len(dataset) // 2)
    # Note that we get the first one wrong!
    for (v, c) in zip(test_data, test_target):
        print(int(bagged(v)), c)
