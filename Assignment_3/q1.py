"""
Define a function linear_regression_1d which takes in a list of pairs, where the first value in each pair is
the feature value and the second is the response value. Return a pair (m, c) where m is the slope of the line of least
squares fit, and c is the intercept of the line of least squares fit.
定义一个函数linear_regression_1d，该函数接收一个配对列表，其中每一对中的第一个值是特征值，第二个是响应值。返回一对（m，c），其中m是最小二乘法拟合线的斜率，c是最小二乘法拟合线的截距。
"""


def dot(x, y):
    return sum([xi * yi for xi, yi in zip(x, y)])


def linear_regression_1d(data):
    """
    :param data:(x, y) feature value, response value
    :return: (m, c)
    m is the least squares fit, c is the intercept of the line of the least squares fit.
    """
    x, y = zip(*(data))
    n = len(data)
    x_times_y = dot(x, y)
    x_times_x = dot(x, x)
    m = (n * x_times_y - sum(x) * sum(y)) / (n * x_times_x - sum(x) ** 2)
    c = (sum(y) - m * sum(x)) / n
    return m, c


if __name__ == "__main__":
    print(1)

    data = [(1, 4), (2, 7), (3, 10)]
    m, c = linear_regression_1d(data)
    print(m, c)
    print(4 * m + c)
