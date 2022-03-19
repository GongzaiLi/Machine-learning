# If you wish, you can use the following template.
#
# Representation-dependent functions are defined outside of the main CEA
# function. This allows CEA to be representation-independent. In other words
# by defining the following functions appropriately, you can make CEA work with
# any representation.
import copy


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


def lge(code_a, code_b):
    """Takes two codes and returns True if code_a is less general or equal
        to code_b. Complete this for the conjunction of constraints. You do not need to decode the given codes."""

    # code_a  <=  code_b  that means code_b more general 其中？ 更general  0 更 special

    more_general = []
    for a, b in zip(code_a, code_b):
        # 首先 把两个拿出来 b == ？ 或者
        mg = b == "?" or a == b or a == "0"  # b == "?" or (b != "0" and (a == b or a == "0"))
        more_general.append(mg)
    return all(more_general)


def more_general(code_a, code_b):
    return lge(code_b, code_a)


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


def minimal_generalisations(code, x):
    """Takes a code (corresponding to a hypothesis) and returns the set of all
    codes that are the minimal generalisations of the given code with respect
    to the given input x."""
    print(code, x)
    h = list(code)
    for i in range(len(code)):
        if not match(code[i:i + 1], x[i:i + 1]):
            if code[i] != '0':
                h[i] = '?'
            else:
                h[i] = x[i]
    print([tuple(h)], 888888888888888888)
    return [tuple(h)]


def generalize_specific(G, S, x):
    for s in list(S):
        if s not in S:
            continue
        if not match(s, x):
            S.remove(s)
            H = minimal_generalisations(s, x)
            S.update([h for h in H if any([more_general(g, h) for g in G])])
            S.difference_update([h for h in S if any([more_general(h, s) for s in S if h != s])])
    return S


def minimal_specialisations(cc, domains, x):
    """Takes a code (corresponding to a hypothesis) and returns the set of all
    codes that are the minimal specialisions of the given code with respect
    to the given input x."""

    h = []
    for i in range(len(cc)):
        if cc[i] == '?':
            for ele in domains[i]:
                if x[i] != ele:
                    cc_new = cc[:i] + (ele,) + cc[i + 1:]
                    h.append(cc_new)
        elif cc[i] != '0':
            cc_new = cc[:i] + ("0",) + cc[i + 1:]
            h.append(cc_new)
    print(h, 11111111111111111111)
    return h


def specialize_general(G, S, domains, x):
    for g in list(G):
        if g not in G:
            continue
        if match(g, x):
            G.remove(g)
            H = minimal_specialisations(g, domains, x)
            print(H, len(H), 2222222222222222222)
            G.update([h for h in H if any([more_general(h, s) for s in S])])
            G.difference_update([h for h in G if any([more_general(g, h) for g in G if h != g])])
    return G


def cea_trace(domains, D):
    S_trace, G_trace = [], []
    S = initial_S(domains)
    G = initial_G(domains)

    # Append S and G (or their copy) to corresponding trace list
    S_trace.append(copy.deepcopy(S))
    G_trace.append(copy.deepcopy(G))

    for x, y in D:
        if y:
            G = {g for g in G if match(g, x)}
            S = generalize_specific(G, S, x)

        else:  # if negative
            S = {s for s in S if not match(s, x)}
            G = specialize_general(G, S, domains, x)

        # Append S and G (or their copy) to corresponding trace list
        S_trace.append(copy.deepcopy(S))
        G_trace.append(copy.deepcopy(G))

    return S_trace, G_trace


if __name__ == "__main__":
    # A case where the target function is not in H

    # domains = [
    #     {'red', 'green', 'blue'}
    # ]
    #
    # training_examples = [
    #     (('red',), True),
    #     (('green',), True),
    #     (('blue',), False),
    # ]
    #
    # S_trace, G_trace = cea_trace(domains, training_examples)
    # S, G = S_trace[-1], G_trace[-1]
    # print(len(S) == len(G) == 0)

    domains = [
        {"Sunny", "Cloudy", "Rainy"},
        {"Warm", "Cold"},
        {"Normal", "High"},
        {"Strong", "Weak"},
        {"Warm", "Cool"},
        {"Same", "Change"}
    ]

    training_examples = [
        (('Sunny', 'Warm', 'Normal', 'Strong', 'Warm', 'Same'), True),
        (('Sunny', 'Warm', 'High', 'Strong', 'Warm', 'Same'), True),
        (('Rainy', 'Cold', 'High', 'Strong', 'Warm', 'Change'), False),
        (('Sunny', 'Warm', 'High', 'Strong', 'Cool', 'Change'), True),
    ]

    S_trace, G_trace = cea_trace(domains, training_examples)
    print("S_trace")
    for s in S_trace:
        print(s)
    print("G_trace")
    for g in G_trace:
        print(g)

    print(all(type(x) is set for x in S_trace + G_trace))
    S, G = S_trace[-1], G_trace[-1]
    print(len(S), len(G))

    #
    # domains = [
    #     {'red', 'blue'}
    # ]
    #
    # training_examples = [
    #     (('red',), True)
    # ]
    #
    # S_trace, G_trace = cea_trace(domains, training_examples)
    # print(len(S_trace), len(G_trace))
    # print(all(type(x) is set for x in S_trace + G_trace))
    # S, G = S_trace[-1], G_trace[-1]
    # print(len(S), len(G))

    # A case where the target function is not in H

    # domains = [
    #     ('T', 'F'),
    #     ('T', 'F'),
    # ]
    #
    # training_examples = [
    #     (('F', 'F'), True),
    #     (('T', 'T'), False),
    # ]
    #
    # S_trace, G_trace = cea_trace(domains, training_examples)
    # print(len(S_trace), len(G_trace))
    # S, G = S_trace[-1], G_trace[-1]
    # print(len(S), len(G))
