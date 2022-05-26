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


def bootstrap(dataset, sample_size):
    random = pseudo_random()
    while True:
        new_sample = []
        for _ in range(sample_size): # new dataset size
            r = next(random)  # random everytime r
            random_index = int(r * len(dataset))
            new_sample.append(dataset[random_index])
        yield np.array(new_sample)


# def take(n, iterator):
#     while n > 0:
#         yield next(iterator)
#         n -= 1
#
# for i in take(5, pseudo_random()):
#     print(i)

if __name__ == '__main__':
    dataset = np.array([[1, 0, 2, 3],
                        [2, 3, 0, 0],
                        [4, 1, 2, 0],
                        [3, 2, 1, 0]])
    ds_gen = bootstrap(dataset, 3)
    # https://zhuanlan.zhihu.com/p/24851814
    print(next(ds_gen))
    print(next(ds_gen))
