# If you wish, you can use the following template.
#
# Representation-dependent functions are defined outside of the main CEA
# function. This allows CEA to be representation-independent. In other words
# by defining the following functions appropriately, you can make CEA work with
# any representation.

def decode(code):
    """Takes a code and returns the corresponding hypothesis."""

    def h(x):
        raise NotImplementedError  # Remove this line
        # Complete this function for the conjunction of constraints

    return h


def match(code, x):
    """Takes a code and returns True if the corresponding hypothesis returns
    True (positive) for the given input."""
    return decode(code)(x)


def lge(code_a, code_b):
    """Takes two codes and returns True if code_a is less general or equal
    to code_b."""

    # Complete this for the conjunction of constraints. You do not need to
    # decode the given codes.


def initial_S(domains):
    """Takes a list of domains and returns a set where each element is a
    code for the initial members of S."""
    print(domains, 11111)
    return set(("0" * len(domains)))


def initial_G(domains):
    """Takes a list of domains and returns a set where each element is a
    code for the initial members of G."""

    # Return an appropriate set


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


def cea_trace(domains, D):
    S_trace, G_trace = [], []
    S = initial_S(domains)
    G = initial_G(domains)
    # Append S and G (or their copy) to corresponding trace list

    # for x, y in D:
    #     if y:  # if positive
    #
    #     # Complete
    #
    #     else:  # if negative

    # Complete

    # Append S and G (or their copy) to corresponding trace list

    return S_trace, G_trace


if __name__ == "__main__":
    domains = [
        {'red', 'blue'}
    ]

    training_examples = [
        (('red',), True)
    ]

    S_trace, G_trace = cea_trace(domains, training_examples)
    print(len(S_trace), len(G_trace))
    print(all(type(x) is set for x in S_trace + G_trace))
    S, G = S_trace[-1], G_trace[-1]
    print(len(S), len(G))
