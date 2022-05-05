from collections import namedtuple

class ConfusionMatrix(namedtuple("ConfusionMatrix",
                                 "true_positive false_negative "
                                 "false_positive true_negative")):
    pass

def a_dom_b(a_cfm, b_cfm):
    a_tp, a_fn, a_fp, a_tn = a_cfm
    b_tp, b_fn, b_fp, b_tn = b_cfm

    a_tpr = a_tp / (a_tp + a_fn)
    a_fpr = a_fp / (a_fp + a_tn)

    b_tpr = b_tp / (b_tp + b_fn)
    b_fpr = b_fp / (b_fp + b_tn)

    return a_tpr > b_tpr and a_fpr < b_fpr


def is_domed(classifier, classifers):
    for c2 in classifers:
        if a_dom_b(c2[1], classifier[1]):
            return True
    return False


def roc_non_dominated(classifers):
    non_dom = []
    for c in classifers:
        if not is_domed(c, classifers):
            non_dom.append(c)
    return non_dom

if __name__ == '__main__':
    # Example similar to the lecture notes

    classifiers = [
        ("Red", ConfusionMatrix(60, 40,
                                20, 80)),
        ("Green", ConfusionMatrix(40, 60,
                                  30, 70)),
        ("Blue", ConfusionMatrix(80, 20,
                                 50, 50)),
    ]
    print(sorted(label for (label, _) in roc_non_dominated(classifiers)))