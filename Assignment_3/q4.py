import numpy as np


def linear_regression(xs, ys, basis_functions=None, penalty=0):
    x_raw_size, x_col_size = xs.shape
    intercept = np.ones(x_raw_size).reshape(-1, 1)
    if basis_functions is not None:
        X = intercept
        for f in basis_functions:
            basis_vector = np.array([f(x) for x in xs]).reshape(-1, 1)
            X = np.concatenate((X, basis_vector), axis=1)
    else:
        X = np.concatenate((intercept, xs), axis=1)

    X_raw_size, X_col_size = X.shape
    # identity 就是一个xii = 1 的矩阵 [[1, 0], [0, 1]] https://en.wikipedia.org/wiki/Identity_matrix
    penalty_term = np.identity(X_col_size) * penalty
    theta = np.linalg.inv(X.T @ X + penalty_term) @ X.T @ ys
    return theta


if __name__ == "__main__":
    print("Question 4")

    # xs = np.arange(5).reshape((-1, 1))
    # ys = np.arange(1, 11, 2)
    # print(xs, "xs 111111111111")
    # print(ys, "ys 111111111111")
    #
    # print(linear_regression(xs, ys), end="\n\n")
    #
    # with np.printoptions(precision=5, suppress=True):
    #     print(linear_regression(xs, ys, penalty=0.1))

    # we set the seed to some number so we can replicate the computation
    np.random.seed(0)

    xs = np.arange(-1, 1, 0.1).reshape(-1, 1)
    m, n = xs.shape
    # Some true function plus some noise:
    ys = (xs ** 2 - 3 * xs + 2 + np.random.normal(0, 0.5, (m, 1))).ravel()

    functions = [lambda x: x[0], lambda x: x[0] ** 2, lambda x: x[0] ** 3, lambda x: x[0] ** 4,
                 lambda x: x[0] ** 5, lambda x: x[0] ** 6, lambda x: x[0] ** 7, lambda x: x[0] ** 8]

    for penalty in [0, 0.01, 0.1, 1, 10]:
        with np.printoptions(precision=5, suppress=True):
            print(linear_regression(xs, ys, basis_functions=functions, penalty=penalty)
                  .reshape((-1, 1)), end="\n\n")
