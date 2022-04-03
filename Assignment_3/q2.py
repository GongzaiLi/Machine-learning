"""
Define a function linear_regression which takes two numpy arrays as input:
the first is the input part of the training data which is an m×n array (design matrix),
while the second is the output part of the training data which is a one-dimensional array (vector) with m elements.
Return the one-dimensional array (vector) θ, with (n + 1) elements,
which contains the least-squares regression coefficients of the features;
the first ("extra") value is the intercept.
定义一个函数linear_regression，它接收两个numpy数组作为输入：第一个是训练数据的输入部分，
是一个m×n数组（设计矩阵），而第二个是训练数据的输出部分，是一个有m个元素的一维数组（向量）。
返回一维数组（向量）θ，有（n+1）个元素，包含特征的最小二乘回归系数；第一个（"额外"）值是截距。


"""

import numpy as np


def linear_regression(x, y):
    """
    θ = (X.T * X)^−1 * X.T * y
    """
    x_raw_size, x_col_size = x.shape
    intercept = np.ones(x_raw_size).reshape(-1, 1)  # 创建一个新的矩阵 intercept term 每个训练数组的第一个x0 为 1 我们设置的
    X = np.concatenate((intercept, x), axis=1) # 将x 和 intercept 合并在一起

    theta = np.matmul(np.matmul(np.linalg.inv(np.matmul(X.T, X)), X.T), y)
    return theta




# def linear_regression(x, y):
#     intercept = np.ones(x.shape[0]).reshape(-1, 1)
#     x = np.concatenate((intercept, x), axis=1)
#     print(x, 111111)
#     print(x.T, 999999999999)
#     a = np.matmul(x.T, x)
#     print(a, 22222222222222222222)
#     c = np.linalg.inv(a)
#     print(c, 4444444444444444444)
#     b = np.matmul(c, x.T)
#     print(b, 555555555555555555)
#     theta = np.matmul(np.matmul(np.linalg.inv(np.matmul(x.T, x)), x.T), y)
#     return theta

if __name__ == "__main__":
    # print(2)

    xs = np.arange(5).reshape((-1, 1))
    ys = np.arange(1, 11, 2)

    # print(xs.shape, 12321312)
    print(ys, 23232323)
    print(linear_regression(xs, ys))
    """
    np.arange(3) = array([0, 1, 2])
    a = np.arange(6).reshape((3, 2)) = array([[0, 1], [2, 3], [4, 5]])
    numpy.reshape(a, newshape, order='C')
    aarray_like Array to be reshaped.
    """
    # np.ones(x.shape[0]).reshape(-1, 1) 创建一个新的数组 shape 是得出具体array的形状怕（5， 1） 5 为
