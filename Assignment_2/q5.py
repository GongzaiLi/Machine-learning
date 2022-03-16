"""

Update your DTNode to have a new method leaves that
returns the number of leaves in the decision tree (assuming the method is called from the root).
"""


class DTNode:
    def __init__(self, decision):
        self.decision = decision
        self.children = []

    def predict(self, feature_vector):
        if not callable(self.decision):
            return self.decision
        else:
            leaf_index = self.decision(feature_vector)
            next_node = self.children[leaf_index]
            return next_node.predict(feature_vector)

    def leaves(self):
        if not self.children:
            return 1
        leaves_count = 0
        for child in self.children:
            leaves_count += child.leaves()
        return leaves_count



if __name__ == "__main__":
    print(5)

    n = DTNode(True)
    print(n.leaves())

    tt = DTNode(False)
    tf = DTNode(True)
    ft = DTNode(True)
    ff = DTNode(False)
    t = DTNode(lambda v: 0 if v[1] else 1)
    f = DTNode(lambda v: 0 if v[1] else 1)
    t.children = [tt, tf]
    f.children = [ft, ff]
    n = DTNode(lambda v: 0 if v[0] else 1)
    n.children = [t, f]
    print(n.leaves())

