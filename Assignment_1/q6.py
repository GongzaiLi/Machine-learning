"""
Write a function cea_trace(domains, training_example)
that takes a list of domains of input features and a list of training examples for
a binary classification problem and returns the traces of the sets S and G.
编写一个函数cea_trace(domains, training_example)，该函数接收一个输入特征域的列表和一个二元分类问题的训练实例列表，并返回集合S和G的轨迹。




"""

# If you wish, you can use the following template.
#
# Representation-dependent functions are defined outside of the main CEA
# function. This allows CEA to be representation-independent. In other words
# by defining the following functions appropriately, you can make CEA work with
# any representation.

"""
('Hi!',) * 4 == ('Hi!', 'Hi!', 'Hi!', 'Hi!') 且所有ip 都不一样

a = [[1]] * 5 == [[1], [1], [1], [1], [1]] ip 都一样
"""

import copy


def initial_S(domains):
    """Takes a list of domains and returns a set where each element is a
    code for the initial members of S."""
    # 返回一个specific hypotheses
    return {len(domains) * ("0",)}


def initial_G(domains):
    """Takes a list of domains and returns a set where each element is a
    code for the initial members of G."""
    # 返回一个general hypotheses
    return {len(domains) * ("?",)}


def decode(code):
    """Takes a code and returns the corresponding hypothesis."""

    def h(x):
        # Complete this function for the conjunction of constraints
        # satisfied
        return all(code[i] != "0" and (code[i] == "?" or code[i] == x[i]) for i in range(len(code)))

    return h


def match(code, x):
    """Takes a code and returns True if the corresponding hypothesis returns
    True (positive) for the given input."""
    return decode(code)(x)


"""
l1 = [1, 2, 3]
l2 = [3, 4, 5]

list(zip(l1, l2))
[(1, 3), (2, 4), (3, 5)]
"""


def lge(code_a, code_b):
    """Takes two codes and returns True if code_a is less general or equal
    to code_b. Complete this for the conjunction of constraints. You do not need to decode the given codes."""

    # code_a  <=  code_b  that means code_b more general 其中？ 更general  0 更 special

    more_general = []
    for a, b in zip(code_a, code_b):
        # 首先 把两个拿出来 b == ？ 或者
        mg = b == "?" or (b != "0" and (a == b or a == "0"))
        more_general.append(mg)
    return all(more_general)


def minimal_generalisations(code, x):
    """Takes a code (corresponding to a hypothesis) and returns the set of all
    codes that are the minimal generalisations of the given code with respect
    to the given input x."""

    h = list(code)
    for i in range(len(code)):
        if not match((code[i],), (x[i],)):
            h[i] = "?" if code[i] != "0" else x[i]

    return {tuple(h)}  # Return an appropriate set


def minimal_specialisations(cc, domains, x):
    """Takes a code (corresponding to a hypothesis) and returns the set of all
    codes that are the minimal specialisations of the given code with respect
    to the given input x."""

    h = []
    for i in range(len(cc)):
        if cc[i] == "?":
            for ele in domains[i]:
                if x[i] != ele:
                    cc_new = cc[:i] + (ele,) + cc[i + 1:]
                    h.append(cc_new)
        elif cc[i] != "0":
            cc_new = cc[:i] + ("0",) + cc[i + 1:]
            h.append(cc_new)
    return h

    # Return an appropriate set


"""
The number of elements in the list domains is equal to the number of features (attributes) in the problem. 
The i-th element is a collection (set or list with no repetition) of values that can be taken by the i-th feature.
"""

"""
该difference_update()方法删除两个集合中都存在的项目。
x = {"apple", "banana", "cherry"}
y = {"google", "microsoft", "apple"}

x.difference_update(y)

print(x)
{'banana', 'cherry'}
"""


def cea_trace(domains, D):
    S_trace, G_trace = [], []
    S = initial_S(domains)
    G = initial_G(domains)

    # Append S and G (or their copy) to corresponding trace list
    S_trace.append(copy.deepcopy(S))
    G_trace.append(copy.deepcopy(G))

    for x, y in D:
        if y:  # if positive # is true
            # Remove from G any hypotheses that do not match d
            G = {g for g in G if match(g, x)}  # {('?',)}

            for s in list(S):
                if s not in S:
                    continue

                if not match(s, x):
                    S.remove(s)
                    H = minimal_generalisations(s, x)
                    # h matches d
                    # some member of G is more general than h
                    S.update(tuple([h for h in H if match(h, x) and any(lge(h, g) for g in G)]))
                    # Remove from S any h that is more general than another hypothesis in S
                    # 找到所有 s more general than h 放入这个set 里面然后yong difference 删除掉
                    S.difference_update({s for s in S if any(lge(h, s) for h in S if s != h)})

        else:  # if negative
            # Remove from S any hypotheses that match d
            S = {s for s in S if not match(s, x)}
            for g in list(G):
                if g not in G:
                    continue
                if match(g, x):
                    G.remove(g)
                    # h does not match d
                    # some member of S is more specific than h
                    H = minimal_specialisations(g, domains, x)
                    G.update(tuple([h for h in H if not match(h, x) and any(lge(s, h) for s in S)]))
                    # Remove from G any h that is more specific than another hypothesis in G
                    G.difference_update({g for g in G if any(lge(h, g) for h in G if g != h)})

        # Append S and G (or their copy) to corresponding trace list
        S_trace.append(copy.deepcopy(S))
        G_trace.append(copy.deepcopy(G))

    return S_trace, G_trace


if __name__ == "__main__":
    domains = [
        {'red', 'blue'},
    ]

    training_examples = [
        (('red',), True)
    ]

    S_trace, G_trace = cea_trace(domains, training_examples)
    print(len(S_trace), len(G_trace))
    print(all(type(x) is set for x in S_trace + G_trace))
    S, G = S_trace[-1], G_trace[-1]
    print(len(S), len(G))

    domains = [
        {'T', 'F'}
    ]

    training_examples = []  # no training examples

    S_trace, G_trace = cea_trace(domains, training_examples)
    print(len(S_trace), len(G_trace))
    S, G = S_trace[-1], G_trace[-1]
    print(len(S), len(G))

    domains = [
        ('T', 'F'),
        ('T', 'F'),
    ]

    training_examples = [
        (('F', 'F'), True),
        (('T', 'T'), False),
    ]

    S_trace, G_trace = cea_trace(domains, training_examples)
    print(len(S_trace), len(G_trace))
    S, G = S_trace[-1], G_trace[-1]
    print(len(S), len(G))
