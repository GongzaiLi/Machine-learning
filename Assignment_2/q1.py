"""
Define a class DTNode to act as a node for our decision tree. The class will be used as both decision and leaf nodes.
定义一个DTNode类，作为我们决策树的节点。该类将被用作决策节点和叶子节点。

A DTNode object must be initialisable with a decision, which is either
一个DTNode对象必须可以用一个决策来初始化，这个决策可以是

a function that takes an object (typically a feature vector) and indicates which child should be followed
(when the object is node is a decision node); or
一个函数，它接收一个对象（通常是一个特征向量），并指出应该遵循哪个子节点（当对象是决策节点时）；或

a value which represents the classification or regression result (when the object is a leaf node).
一个代表分类或回归结果的值（当对象是一个叶子节点时）

A DTNode object must have an attribute children, which can be set to a data structure that maps the output of
the decision function to a specific child. We assume the output of the decision function is an index into a list.
一个DTNode对象必须有一个属性children，它可以被设置为一个数据结构，将决策函数的输出映射到一个特定的子节点。我们假设决策函数的输出是一个列表的索引。

A DTNode must also have a method predict, which takes an input object (e.g. a feature vector) and returns the result of
the decision tree for that input.
一个DTNode还必须有一个方法predict，它接收一个输入对象（例如一个特征向量）并返回该输入的决策树的结果。

Hint: the predict method is recursive. You can use the built-in function callable to test whether a Python object is
callable (in this case a function).
提示：predict方法是递归的。你可以使用内置的函数callable来测试一个Python对象是否可调用（在这里是一个函数）。
"""

"""
DT node 通过一个decision 这个decision 可以是 一个true false 或者是告诉你通往 children 的节点。一直找到决策树最底层的决策。最后return。
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


if __name__ == "__main__":
    print(1)

    # # The following (leaf) node will always predict True
    # node = DTNode(True)
    #
    # # Prediction for the input (1, 2, 3):
    # x = (1, 2, 3)
    # print(node.predict(x))
    #
    # # Sine it's a leaf node, the input can be anything. It's simply ignored.
    # print(node.predict(None))

    yes_node = DTNode("Yes")
    no_node = DTNode("No")
    tree_root = DTNode(lambda x: 0 if x[2] < 4 else 1)
    tree_root.children = [yes_node, no_node]

    print(tree_root.predict((False, 'Red', 3.5)))
    print(tree_root.predict((False, 'Green', 6.1)))
