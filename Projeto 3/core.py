import math


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
    file = open(filename, 'r', encoding='latin-1')
    lines = file.readlines()
    vals = []
    for line in lines:
        vals.append(line.split('::'))

    file.close()
    return vals


def value_counter(values: list) -> dict:
    value_count = {x: 0 for x in values}
    for value in values:
        value_counter[value] += 1

    return value_count


def entropy(outcomes: list) -> float:
    entropy = 0
    total = len(outcomes)
    outcome_count = value_counter(outcomes)
    for count in outcome_count.values():
        entropy -= count/total * math.log2(count/total)

    return entropy
    

def information_gain(examples, target_attribute, attribute) -> float:
    attribute_values = set()
    for value in examples[attribute]:
        attribute_values.add(value)

    information_entropy = 0
    example_outcomes = examples[target_attribute]
    total = len(example_outcomes)
    for attribute_value in attribute_values:
        outcomes = examples[attribute == attribute_value][target_attribute]
        value_entropy = entropy(outcomes)
        outcome_count = value_counter(outcomes)
        for count in outcome_count.values():
            information_entropy += count/total * value_entropy

    return entropy(example_outcomes) - information_entropy


def most_common(values: list):
    return max(set(values), key=values.count)


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
