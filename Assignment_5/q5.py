import hashlib
import numpy as np


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


class weighted_bootstrap:

    def __init__(self, dataset, weights, sample_size):
        self.dataset = dataset
        self.weights = weights  # The class should allow modification of the weights attribute so that the weights can change dynamically.
        self.sample_size = sample_size
        self.random = pseudo_random()

    def __iter__(self):
        return self

    def __next__(self):
        """
        Calculate the running sum of the weights
        Generate a random value up to the sum of the weights
        Find the index i of the first value in the running sum to exceed this random value.
        The row in position i in the dataset gets added to the sample.
        Repeat until a complete sample is drawn.
        """
        running_sum_weights = [sum(self.weights[0:i + 1]) for i in range(len(self.weights))]
        sum_weights = sum(self.weights)
        new_samples = []
        for _ in range(self.sample_size):
            r = next(self.random)
            random_weight = r * sum_weights
            for i in range(len(running_sum_weights)):
                if running_sum_weights[i] > random_weight:
                    new_samples.append(self.dataset[i])
                    break
        return np.array(new_samples)


def voting_ensemble(classifiers):
    def classifier_report(data):
        report = [classifier(data) for classifier in classifiers]
        return max(sorted(report), key=report.count)  # sorts lowest asc 小到大

    return classifier_report


def adaboost(learner, dataset, n_models):
    # https://www.mygreatlearning.com/blog/adaboost-algorithm/
    # was try to set 1 or 0 that is not work, research shows 1/N and N is total number of dataset
    weights = [1/len(dataset) for _ in range(len(dataset))]  # Assign equal weight to each training instance
    wbs = weighted_bootstrap(dataset, weights, len(dataset[0]))
    classifiers = []
    for _ in range(n_models):  # For t iterations:
        model = learner(next(wbs))
        classifiers.append(model)
        error = 0
        for i in range(len(dataset)):
            """
            Apply learning algorithm to weighted dataset,
                store resulting model
             Compute model’s error e on weighted dataset
            """
            feature = dataset[i][:-1]  # input
            target = dataset[i][-1]  # output
            if model(feature) != target:  # if model out put not equal target
                error += weights[i]  # error add weight
        if error == 0 or error >= 0.5:
            """
            If e = 0 or e ≥ 0.5:
                Terminate model generation
            """
            break   # which mean the model is good
        for i in range(len(dataset)):
            """
            For each instance in dataset:
                If classified correctly by model:
                    Multiply instance’s weight by e/(1-e) # instances 是 一个data
            """
            feature = dataset[i][:-1]
            target = dataset[i][-1]
            if model(feature) == target:
                weights[i] *= (error / (1 - error))

        for i in range(len(weights)):
            """
            Normalize weight of all instances
            """
            weights[i] /= sum(weights)

    return voting_ensemble(classifiers)

# def adaboost(learner, dataset, n_models):
#     weights = [1/len(dataset) for _ in dataset]
#     classifiers = []
#     wbs = weighted_bootstrap(dataset, weights, len(dataset))
#
#     for _ in range(n_models):
#         model = learner(next(wbs))
#         classifiers.append(model)
#         error = 0
#         for i in range(len(dataset)):
#             feature = dataset[i][:-1]
#             target = dataset[i][-1]
#             if model(feature) != target:
#                 error += weights[i]
#         if error == 0 or error >= 0.5:
#             break
#         for i in range(len(dataset)):
#             feature = dataset[i][:-1]
#             target = dataset[i][-1]
#             if model(feature) == target:
#                 weights[i] *= error/(1-error)
#
#         sum_weight = sum(weights)
#         for i in range(len(weights)):
#             weights[i] /= sum_weight
#     return voting_ensemble(classifiers)



if __name__ == '__main__':
    import sklearn.datasets
    import sklearn.utils
    import sklearn.linear_model

    digits = sklearn.datasets.load_digits()
    data, target = sklearn.utils.shuffle(digits.data, digits.target, random_state=3)
    train_data, train_target = data[:-5, :], target[:-5]
    test_data, test_target = data[-5:, :], target[-5:]
    dataset = np.hstack((train_data, train_target.reshape((-1, 1))))


    def linear_learner(dataset):
        features, target = dataset[:, :-1], dataset[:, -1]
        model = sklearn.linear_model.SGDClassifier(random_state=1, max_iter=1000, tol=0.001).fit(features, target)
        return lambda v: model.predict(np.array([v]))[0]


    boosted = adaboost(linear_learner, dataset, 10)
    for (v, c) in zip(test_data, test_target):
        print(int(boosted(v)), c)

    print()
    import sklearn.datasets
    import sklearn.utils
    import sklearn.linear_model

    iris = sklearn.datasets.load_iris()
    data, target = sklearn.utils.shuffle(iris.data, iris.target, random_state=0)
    train_data, train_target = data[:-5, :], target[:-5]
    test_data, test_target = data[-5:, :], target[-5:]
    dataset = np.hstack((train_data, train_target.reshape((-1, 1))))


    def linear_learner(dataset):
        features, target = dataset[:, :-1], dataset[:, -1]
        model = sklearn.linear_model.SGDClassifier(random_state=1, max_iter=1000, tol=0.001).fit(features, target)
        return lambda v: model.predict(np.array([v]))[0]


    boosted = adaboost(linear_learner, dataset, 10)
    for (v, c) in zip(test_data, test_target):
        print(int(boosted(v)), c)
