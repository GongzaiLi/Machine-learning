from collections import namedtuple


class ConfusionMatrix(namedtuple("ConfusionMatrix",
                                 "true_positive false_negative "
                                 "false_positive true_negative")):
    # https://realpython.com/python-namedtuple/

    def __str__(self):
        elements = [self.true_positive, self.false_negative,
                    self.false_positive, self.true_negative]
        return ("{:>{width}} " * 2 + "\n" + "{:>{width}} " * 2).format(
            *elements, width=max(len(str(e)) for e in elements))


def confusion_matrix(classifier, dataset):
    true_positive, false_negative, false_positive, true_negative = 0, 0, 0, 0

    for x, y in dataset:
        classified = classifier(x)  # prediction
        if classified:
            if classified == y:
                true_positive += 1
            else:
                false_positive += 1
        else:
            if classified == y:
                true_negative += 1
            else:
                false_negative += 1

    return ConfusionMatrix(true_positive, false_negative, false_positive, true_negative)


if __name__ == '__main__':
    dataset = [
        ((0.8, 0.2), 1),
        ((0.4, 0.3), 1),
        ((0.1, 0.35), 0),
    ]
    print(confusion_matrix(lambda x: 1, dataset))
    print()
    print(confusion_matrix(lambda x: 1 if x[0] + x[1] > 0.5 else 0, dataset))
