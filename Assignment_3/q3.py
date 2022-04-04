import numpy as np


def linear_regression(xs, ys, basis_functions=None):
    x_raw_size, x_col_size = xs.shape
    intercept = np.ones(x_raw_size).reshape(-1, 1)
    if basis_functions is not None:
        X = intercept
        for f in basis_functions:
            basis_vector = np.array([f(x) for x in xs]).reshape(-1, 1)
            X = np.concatenate((X, basis_vector), axis=1)
    else:
        X = np.concatenate((intercept, xs), axis=1)

    theta = np.linalg.inv(X.T @ X) @ X.T @ ys
    return theta


if __name__ == "__main__":
    print(3)

    xs = np.arange(5).reshape((-1, 1))
    print(xs)
    ys = np.array([3, 6, 11, 18, 27])
    print(ys)
    # Can you see y as a function of x? [hint: it's quadratic.]
    functions = [lambda x: x[0], lambda x: x[0] ** 2]  # first elements is offset 其余都是相应函数系数
    print(functions)
    print(linear_regression(xs, ys, functions))

# nate
#     a = np.array([
#         [1, 10],
#         [1, 2]
#     ])
#     print(a)
#     b = [1, 10]
#     print(b)
#     c = a @ b
#     print(c.shape)#(2, ) raw is 2
