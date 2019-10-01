import math
import copy
import pandas as pd

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
        value_count[value] += 1

    return value_count


def entropy(outcomes: list) -> float:
    entropy = 0
    total = len(outcomes)
    outcome_count = value_counter(outcomes)
    for count in outcome_count.values():
        entropy -= count/total * math.log2(count/total)

    return entropy
    

def information_gain(examples, entire_entropy) -> float:
    print("Information gain")

    if type(examples.iloc[0,0]) == list:
        attribute_values = {item for sublist in examples.iloc[:,0] for item in sublist}

        information_entropy = 0
        total = len(examples.index)
        header = list(examples.columns)
        for attribute_value in attribute_values:
            mask = examples.iloc[:,0].apply(lambda x: attribute_value in x)
            outcomes = examples[mask].iloc[:,-1]
            value_entropy = entropy(outcomes)
            outcome_count = value_counter(outcomes)
            for count in outcome_count.values():
                information_entropy += count/total * value_entropy

    else:
        attribute_values = set(examples.iloc[:,0])

        information_entropy = 0
        total = len(examples.index)
        header = list(examples.columns)
        for attribute_value in attribute_values:
            outcomes = (examples[examples[header[0]] == attribute_value]).iloc[:,-1]
            value_entropy = entropy(outcomes)
            outcome_count = value_counter(outcomes)
            for count in outcome_count.values():
                information_entropy += count/total * value_entropy

    return entire_entropy - information_entropy


def most_common(values: list):
    return max(set(values), key=values.count)

def best_attribute(examples):
    entire_entropy = entropy(examples.iloc[:,-1])

    attributes_entropy = []

    for i in range(len(examples.columns)):
        attributes_entropy.append(information_gain(examples.iloc[:,[i,-1]], entire_entropy))

    header = list(examples.columns)

    return header[attributes_entropy.index(max(attributes_entropy))]


def decision_tree(examples):

    print("Decision Tree")

    tree = Tree()

    if len(set(examples.iloc[:,-1])) == 1:
        tree.root.label = examples.iloc[0,-1]
    elif len(examples.columns) == 1:
        tree.root.label = most_common(examples.iloc[:,-1])
    else:
        attribute = best_attribute(examples)
        tree.root.attribute = attribute
        for value in set(examples[attribute]):
            child_tree = Tree()
            relevant_examples = examples[examples[attribute] == value]
            if not relevant_examples:
                child_tree.root.label = most_common(examples.iloc[:,-1])
            else:
                child_tree = decision_tree(relevant_examples.drop(columns=[attribute]))

            tree.add_child(child_tree)

    return tree

    def print_tree(tree):
        print("(Label: ",tree.root.label, " , Attribute: ", tree.root.attribute, ")")
        for child in tree.children:
            print_tree(child)

if __name__ == "__main__":

    movies = pd.read_table("ml-1m/movies.dat", sep="::", names=['MovieID', 'Title', 'Genres'], engine='python')
    users = pd.read_table("ml-1m/users.dat", sep="::", names=['UserID', 'Gender', 'Age', 'Occupation', 'Zip-code'], engine='python')
    ratings = pd.read_table("ml-1m/ratings.dat", sep="::", names=['UserID', 'MovieID', 'Rating', 'Timestamp'], engine='python')

    a = pd.merge(ratings, users, on='UserID', how='left')
    b = pd.merge(a, movies, on='MovieID', how='left')

    final = b.loc[:,['Gender', 'Age', 'Occupation', 'Genres', 'Rating']]
    final['Genres'] = final['Genres'].str.split(pat="|")

    answer = decision_tree(final)
    print_tree(answer)