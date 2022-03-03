# If you wish, you can use the following template.
#
# Representation-dependent functions are defined outside of the main CEA
# function. This allows CEA to be representation-independent. In other words
# by defining the following functions appropriately, you can make CEA work with
# any representation.
import copy


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

    h = list(code)
    for i in range(len(code)):
        if not more_general(code[i:i + 1], x[i:i + 1]):
            if code[i] != '0':
                h[i] = '?'
            else:
                h[i] = x[i]
    return [tuple(h)]


def generalize_specific(G, S, x):
    for s in list(S):
        if s not in S:
            continue
        if not more_general(s, x):
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
    return h


def specialize_general(G, S, domains, x):
    for g in list(G):
        if g not in G:
            continue
        if more_general(g, x):
            G.remove(g)
            H = minimal_specialisations(g, domains, x)
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
            G = {g for g in G if more_general(g, x)}
            S = generalize_specific(G, S, x)

        else:  # if negative
            S = {s for s in S if not more_general(s, x)}
            G = specialize_general(G, S, domains, x)

        # Append S and G (or their copy) to corresponding trace list
        S_trace.append(copy.deepcopy(S))
        G_trace.append(copy.deepcopy(G))

    return S_trace, G_trace


if __name__ == "__main__":
    # A case where the target function is not in H

    domains = [
        {'red', 'green', 'blue'}
    ]

    training_examples = [
        (('red',), True),
        (('green',), True),
        (('blue',), False),
    ]

    S_trace, G_trace = cea_trace(domains, training_examples)
    S, G = S_trace[-1], G_trace[-1]
    print(len(S) == len(G) == 0)
