from collections import namedtuple


class ConfusionMatrix(namedtuple("ConfusionMatrix",
                                 "true_positive false_negative "
                                 "false_positive true_negative")):
    pass


def create_roc_points(classifiers):
    """
    :param classifiers: [(label, confusion_matrix),]
    :return: dict: {label: (TPR, FPR)}
    """
    points = dict()
    for label, confusion_matrix in classifiers:
        TP, FN, FP, TN = confusion_matrix
        TPR = TP / (TP + FN)
        FPR = FP / (FP + TN)
        points[label] = (TPR, FPR)
    return points


def roc_non_dominated(classifiers):
    """
    Classifier A dominates classifier B if and only if
        TPRA > TPRB and FPRA < FPRB.
    :param classifiers:
    :return: list
    """
    non_dominated_list = []
    roc_points_dict = create_roc_points(classifiers)

    labels = roc_points_dict.keys()
    for label_b in labels:
        TPRB, FPRB = roc_points_dict[label_b]
        dominated = False  # 被支配
        for label_a in labels:
            if label_a != label_b:
                TPRA, FPRA = roc_points_dict[label_a]
                if TPRA > TPRB and FPRA < FPRB:  # if is true the label_a dominates label_b 被任意一个支配 any
                    dominated = True
                    break  # 过滤掉被支配的
        if not dominated:
            non_dominated_list.append(label_b)

    return [classifier for classifier in classifiers if classifier[0] in non_dominated_list]


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
