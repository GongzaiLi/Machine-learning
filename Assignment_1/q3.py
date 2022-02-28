"""
Write a function version_space(H, D) that takes a set of hypotheses H, and a training data set D, and returns the version space.
编写一个函数version_space(H, D)，接收一组假设H和一个训练数据集D，并返回版本空间。

Input
The elements of H are hypotheses. Each hypothesis (function) takes an input object and returns True or False (i.e. a binary classifier).
The elements of D are 2-tuples of the form (x, y) where x is an input object and y is either True or False.
输入
H的元素是假说。每个假设（函数）接受一个输入对象并返回真或假（即一个二进制分类器）。
D的元素是形式为(x, y)的2元组，其中x是一个输入对象，y是真或假。

Output
The return value must be a set which will be a subset of (or equal to) H.
返回值必须是一个集合，它将是H的一个子集（或等于）。

Notes
Do not make any assumption about the type of input objects other than that they can be consumed by hypotheses in H.
不要对输入对象的类型做任何假设，除了它们可以被H中的假设所消耗。
"""

from itertools import *


def all_possible_functions(X):
    """
    :param X: an input space with two elements
    :return: all possible functions == functions in a set
    """
    supp_h = set()
    for i in range(2 ** len(X)):  # F = 2^|X|
        for j in combinations(X, i):
            supp_h.add(j)

    F = {f(element) for element in supp_h}
    return F


def f(element):
    def f_sub(x):
        return x in element

    return f_sub


def version_space(H, D):
    VS = set()
    for h in H:
        if all(h(x) == y for x, y in D):  # consistent(h, D) check
            VS.add(h)
    return VS


if __name__ == "__main__":
    print("q3")
    X = {"green", "purple"}  # an input space with two elements
    D = {("green", True)}  # the training data is a subset of X * {True, False}
    F = all_possible_functions(X)
    H = F  # H must be a subset of (or equal to) F

    VS = version_space(H, D)

    print(len(VS))

    for h in VS:
        for x, y in D:
            if h(x) != y:
                print("You have a hypothesis in VS that does not agree with the D!")
                break
        else:
            continue
        break
    else:
        print("OK")

    D = {
        ((False, True), False),
        ((True, True), True),
    }


    def h1(x):
        return True


    def h2(x):
        return False


    def h3(x):
        return x[0] and x[1]


    def h4(x):
        return x[0] or x[1]


    def h5(x):
        return x[0]


    def h6(x):
        return x[1]


    H = {h1, h2, h3, h4, h5, h6}
    VS = version_space(H, D)
    print(sorted(h.__name__ for h in VS))
