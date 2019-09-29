class Node:
    def __init__(self):
        self.label = None
        self.attribute = None


class Tree:
    def __init__(self):
        self.root = Node()
        self.children = []

    def add_child(self, child: Node):
        self.children.append(child)


def parse_file(filename: str):
    file = open(filename, 'r')
    lines = file.readlines()
    vals = []
    for line in lines:
        vals.append(line.split('::'))

    file.close()
    return vals


def most_common(examples):
    return max(set(examples), key=examples.count)


def decision_tree(examples, target_attribute, attributes):
    tree = Tree()
    if len(set(examples)) == 1:
        tree.root.label = examples
    elif not attributes:
        tree.root.label = most_common(examples)
    else:
        attribute = best_attribute(examples)
        tree.root.attribute = attribute
        for value in attribute.values:
            child_tree = Tree()
            relevant_examples = [ex for ex in examples
                                 if attribute in ex.attributes
                                 and ex[attribute] == value]
            if not relevant_examples:
                child_tree.root.label = most_common(relevant_examples)
            else:
                child_tree = decision_tree(relevant_examples, target_attribute,
                                           attributes.remove(attribute))

            tree.add_child(child_tree)

    return tree
