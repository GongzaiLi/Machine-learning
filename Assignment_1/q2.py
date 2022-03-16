"""
Notes

Each member of F must be a function whose domain is the input space and returns True or False.
F的每个成员必须是一个函数，其域是输入空间，并返回真或假。

In Python, functions are hashable and therefore can be added to sets.
在Python中，函数是可散列的，因此可以被添加到集合中。

Do not make any assumption about the type of elements in X other than that they are hashable.  hashable 是可Hash的  dict 就是 hashable
不要对X中元素的类型做任何假设，除了它们是可散列的。     ==  如果一个对象的哈希值在其整个生命周期内都不会改变，那么它就是可哈希的

Your function will be tested only with small input spaces.
你的函数将只用小的输入空间进行测试。

Python’s itertools module may have some useful tools for you.
Python的itertools模块可能有一些对你有用的工具。

There are different ways of implementing your answer. In most cases, you will need to create functions in a loop.
These functions probably need to access some non-local variables (in their closure).
If the non-local variable changes after a function is created, the function is still affected.
There are different techniques to avoid this problem. Do your own research on how to create functions in a loop.
有不同的方法来实现你的答案。在大多数情况下，你将需要在一个循环中创建函数。这些函数可能需要访问一些非局部变量（在它们的闭合中）。
如果非本地变量在函数创建后发生了变化，那么该函数仍然会受到影响。有不同的技术来避免这个问题。请你自己研究一下如何在循环中创建函数。

In some test cases you may see that the elements of the input space (X) are simple objects (e.g. a string)
instead of a tuple (an element of the cartesian product of the domains).
This is to a) have simpler more readable test cases;
and b) emphasise that different representations can be used to describe input objects.
在一些测试用例中，你可能会看到输入空间(X)的元素是简单的对象(例如一个字符串)，而不是一个元组(域的笛卡尔积的一个元素)。
这是为了：a）有更简单的可读性的测试案例；b）强调可以用不同的表示法来描述输入对象。
"""
from itertools import *


# def all_possible_functions(X):
#     supp_h = set()
#     for i in range(2 ** len(X)):  # F = 2^|X|
#         for j in combinations(X, i):
#             print(j)
#             supp_h.add(j)
#
#     F = {f(element) for element in supp_h}
#     return F
#
#
# def f(element):
#     def f_sub(x):
#         return x in element
#
#     return f_sub
#======================================================
# def f_factory(return_statement, items):
#     def f(x):
#         index = items.index(x)
#         return return_statement[index]
#     return f
#
# def all_possible_functions(X):
#     results = []
#     responses = itertools.product(*[[True, False]]*len(X))
#     for return_statement in responses:
#         results.append(f_factory(return_statement, list(X)))
#     return results

from itertools import *

def all_possible_functions(X):
    all_funcs = list(product([False, True], repeat=len(X)))
    ans = []
    for f in all_funcs:
        def F(fun, x_item):
            def h(x):
                print(fun, x_item, 222222222222)
                index = x_item.index(x)
                print(index, 3333333)
                return fun[index]
            return h
        ans.append(F(f, list(X)))
    return ans

"""
对于Calbe 的这个部分告诉我， 就是把所有 green 和 purple 一起的所有情况
___________
| G  |  P |
———————————
| T  |  T |
| T  |  F |
| F  |  T |
| F  |  F |

这样情况就算是 all possible
"""
# def f_factory(return_statement, items):
#
#     def f(x):
#         index = items.index(x)
#         return return_statement[index]
#
#     return f
#
#
# def all_possible_functions(X):
#     results = []
#     responses = product(*[[True, False]] * len(X))
#     for return_statement in responses:
#         print(return_statement, 11111111111111111)
#         results.append(f_factory(return_statement, list(X)))
#     return results


if __name__ == "__main__":

    X = {"green", "purple"}  # an input space with two elements
    F = all_possible_functions(X)

    # Let's store the image of each function in F as a tuple
    images = set()
    for h in F:
        images.add(tuple(h(x) for x in X))

    for image in sorted(images):
        print(image)

    # X = {"green", "purple"}  # an input space with two elements
    # F = all_possible_functions(X)
    #
    # # Let's store the image of each function in F as a tuple
    # images = set()
    # for h in F:
    #     images.add(tuple(h(x) for x in X))
    #
    # for image in sorted(images):
    #     print(image)
    #
    # X = {1, 2, 3}
    # F = all_possible_functions(X)
    # print(len(F))
    #
    # X = {('red', 'large'), ('green', 'large'), ('red', 'small'),
    #      ('green', 'small')}
    # F = all_possible_functions(X)
    # # Let's store the image of each function in F as a tuple
    # images = set()
    # for h in F:
    #     images.add(tuple(h(x) for x in X))
    # for image in sorted(images):
    #     print(image)
