"""
Suppose X ⊆ ℝ^2; that is, the input space is a subset of a 2D Euclidean plane.
Consider all possible integer-coordinate rectangles in this space.
We define to be the set of hypotheses such that each hypothesis corresponds to a rectangle and h(x) returns true
if and only if x is within or on the boundary of the corresponding rectangle.


"""

# todo ask question
"""
Certain encodings allow certain functions to be computed more efficiently. 
For example, with the rectangle encoding presented here, the function "less general or equal to" 
can be computed without iterating over the elements of the input space.
某些编码允许某些函数更有效地被计算出来。例如，用这里介绍的矩形编码，可以计算 "小于等于 "的函数，而不需要对输入空间的元素进行迭代。
"""

def decode(code):
    def h(x):
        x_x = min(code[0], code[2]) <= x[0] <= max(code[0], code[2])  # 两点的x 之间
        x_y = min(code[0], code[2]) <= x[1] <= max(code[0], code[2])  # 两点的y 之间
        return x_x and x_y
    return h


if __name__ == "__main__":
    import itertools
    #
    # h = decode((-1, -1, 1, 1))
    #
    # for x in itertools.product(range(-2, 3), repeat=2):
    #     # print(x)
    #     print(x, h(x))

    h1 = decode((1, 4, 7, 9))
    h2 = decode((7, 9, 1, 4))
    h3 = decode((1, 9, 7, 4))
    h4 = decode((7, 4, 1, 9))

    for x in itertools.product(range(-2, 11), repeat=2):
        print(x, h1(x))
        if len({h(x) for h in [h1, h2, h3, h4]}) != 1:
            print("Inconsistent prediction for", x)
            break
    else:
        print("OK")
