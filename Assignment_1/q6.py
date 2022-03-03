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


####----------------
def lge(code_a, code_b):
    """Takes two codes and returns True if code_a is less general or equal
    to code_b."""

    # Complete this for the conjunction of constraints. You do not need to
    # decode the given codes.


def minimal_generalisations(code, x):
    """Takes a code (corresponding to a hypothesis) and returns the set of all
    codes that are the minimal generalisations of the given code with respect
    to the given input x."""

    # Return an appropriate set


def minimal_specialisations(cc, domains, x):
    """Takes a code (corresponding to a hypothesis) and returns the set of all
    codes that are the minimal specialisations of the given code with respect
    to the given input x."""

    # Return an appropriate set


"""
The number of elements in the list domains is equal to the number of features (attributes) in the problem. 
The i-th element is a collection (set or list with no repetition) of values that can be taken by the i-th feature.
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
            G = {g for g in G if match(g, x)}  # {('?',)}

            i = 0
            while i == len(S):
                if not match(S[])





        # Complete

        else:  # if negative
            print(x)

    # Complete

    # Append S and G (or their copy) to corresponding trace list

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
