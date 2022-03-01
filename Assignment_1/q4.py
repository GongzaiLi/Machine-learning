"""
Write a function less_general_or_equal(ha, hb, X) that takes two hypotheses ha and hb,
and an input space X and returns True if and only if ha is less general or equal to hb.
编写一个函数less_general_or_equal(ha, hb, X)，该函数接收两个假设ha和hb，以及一个输入空间X，当且仅当ha小于或等于hb时返回True。

Notes
The phrase "or equal" should be interpreted as functional equality; that is, computing the same function.
Python's equality operator is not useful here.
短语 "或相等 "应该被解释为功能相等；也就是说，计算相同的函数。Python 的平等运算符在这里没有用。

Do not make any assumption about the type of elements in X other than that they can be consumed by the two hypotheses.
不要对X中的元素类型做任何假设，除了它们可以被两个假设所消耗。

The relation "less general or equal" forms a partial order. "小于一般或等于 "的关系形成了一个部分秩序。
This means that there could be cases where neither h ≤ hʹ nor hʹ ≤ h.
This is unlike total order (e.g. real numbers and the relation ≤) where for every pair of elements, the relation holds at least in one direction.
这与总秩序（如实数和关系≤）不同，在总秩序中，对于每一对元素，关系至少在一个方向上成立。
"""


# for x in X:
#     if not hb(x) and ha(x):
#         return False
# return True

def less_general_or_equal(ha, hb, X):
    supp_ha = {x for x in X if ha(x) == True}
    supp_hb = {x for x in X if hb(x) == True}
    # return supp_ha <= supp_hb
    return supp_ha.issubset(supp_hb)


if __name__ == "__main__":
    print(4)
    X = list(range(1000))


    def h2(x):
        return x % 2 == 0


    def h3(x):
        return x % 3 == 0


    def h6(x):
        return x % 6 == 0


    H = [h2, h3, h6]

    for ha in H:
        for hb in H:
            print(ha.__name__, "<=", hb.__name__, "?", less_general_or_equal(ha, hb, X))


"""
h2 <= h2 ? True
h2 <= h3 ? False
h2 <= h6 ? False
h3 <= h2 ? False
h3 <= h3 ? True
h3 <= h6 ? False
h6 <= h2 ? True
h6 <= h3 ? True
h6 <= h6 ? True
"""
