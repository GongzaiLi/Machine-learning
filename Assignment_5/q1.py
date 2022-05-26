def voting_ensemble(classifiers):
    def classifier_report(data):
        report = [classifier(data) for classifier in classifiers]
        return max(sorted(report), key=report.count) # sorts lowest asc 小到大
    return classifier_report

if __name__ == '__main__':
    # Modelling y > x^2
    # classifiers = [
    #     lambda p: 1 if 1.0 * p[0] < p[1] else 0,
    #     lambda p: 1 if 0.9 * p[0] < p[1] else 0,
    #     lambda p: 1 if 0.8 * p[0] < p[1] else 0,
    #     lambda p: 1 if 0.7 * p[0] < p[1] else 0,
    #     lambda p: 1 if 0.5 * p[0] < p[1] else 0,
    # ]
    classifiers = [
        lambda p: 1,
        lambda p: 1,
        lambda p: 0,
        lambda p: 0,
    ]
    data_points = [(0.2, 0.03), (0.1, 0.12),
                   (0.8, 0.63), (0.9, 0.82)]
    c = voting_ensemble(classifiers)
    for v in data_points:
        print(c(v))