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
        running_sum_weights = [sum(self.weights[0:i+1]) for i in range(len(self.weights))]
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



if __name__ == '__main__':
    # assert len(dataset) == len(weights)
    wbs = weighted_bootstrap([1, 2, 3, 4, 5], [1, 1, 1, 1, 1], 5)  # where dataset and weights must be the same length
    """
            should produce a new bootstrapped sample of sample_size rows,
            where each row has a chance of occurring proportional to its weight.
            """
    sample = next(wbs)

    print(type(sample))
    print(sample)

    print(next(wbs))
    print()
    wbs.weights = [1, 1, 1000, 1, 1]
    print(next(wbs))
    print(next(wbs))
