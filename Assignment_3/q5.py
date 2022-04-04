import numpy as np
import math


# def logistic_regression(xs, ys, alpha, num_iterations):
#     intercept = np.ones(xs.shape[0]).reshape(-1, 1)
#     xs = np.concatenate((intercept, xs), axis=1)
#
#     sigmoid = lambda x: 1 / (1 + math.exp(-x))
#
#     num_examples, features = xs.shape
#
#     theta = np.zeros(features)
#     # θj := θj + α(y (i) − hθ(x^(i)) xj^(i)
#     for _ in range(num_iterations):
#         for i in range(num_examples):
#             xi = xs[i, :]
#             yi = ys[i]
#             theta = theta + alpha * (yi - sigmoid(np.matmul(theta.T, xi))) * xi
#
#     return lambda x: sigmoid(np.matmul(theta.T, np.insert(x, 0, [1])))

def logistic_regression(xs, ys, alpha, num_iterations):
    x_raw_size, x_col_size = xs.shape
    intercept = np.ones(x_raw_size).reshape(-1, 1)
    X = np.concatenate((intercept, xs), axis=1)

    sigmoid = lambda z: 1 / (1 + math.exp(-z))  # g(z) Logistic Regression = θ.T 。 x

    count = 0
    X_raw_size, X_col_size = X.shape
    theta = np.zeros(X_col_size)
    # θj = θj + α(y(i) − hθ(x(i))) xi
    while count < num_iterations:
        for i in range(X_raw_size):
            yi = ys[i]
            xi = X[i, :]  # X[:, i] 取所有的raw 的地i个col的element || X[i, :] 去 i raw 的所有 col
            theta = theta + alpha * (yi - sigmoid(theta.T @ xi)) * xi
        count += 1

    return lambda x: sigmoid(theta.T @ np.insert(x, 0, [1]))  # insert the θ0


if __name__ == "__main__":
    print("Question 5")
    xs = np.array([1, 2, 3, 101, 102, 103]).reshape((-1, 1))
    ys = np.array([0, 0, 0, 1, 1, 1])
    model = logistic_regression(xs, ys, 0.05, 10000)
    test_inputs = np.array([1.5, 4, 10, 20, 30, 40, 50, 60, 70, 80, 90, 101.8, 97]).reshape((-1, 1))

    for test_input in test_inputs:
        print("{:.2f}".format(np.array(model(test_input)).item()))
