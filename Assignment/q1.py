"""
Input
The list domains will be non-empty.
The length of the list is the dimensionality of the input space.
The i-th element of domains is a set (collection) of values that can be taken by the i-th attribute.
Your program will be tested with small domains.

Output
The function input_space(domains) must return a collection (set, list, …) of tuples.
The order of the tuples in the collection is not important.
The order of values in each tuple is important; the i-th value should correspond to the i-th attribute and its value should be from the i-th domain.

Note
You have the option of using one of Python’s built-in libraries and answer this question in a few lines of code.
The test code sometimes uses capital letters for some variables. This is only to make the notation similar to that used in the lecture notes.
"""

from itertools import product


def input_space(domains):
    """
    :param domains: input
    :return: set of tuples
    """
    return set(product(*domains))


if __name__ == "__main__":
    domains = [
        {0, 1, 2},
        {True, False},
    ]

    for element in sorted(input_space(domains)):
        print(element)
