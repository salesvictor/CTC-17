import math
import copy
import pickle
import pandas as pd


class Node:
    def __init__(self):
        self.label = None
        self.attribute = None


class Tree:
    def __init__(self):
        self.root = Node()
        self.children = {}

    def add_child(self, value: str, child: Node):
        self.children[value] = child


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
    if type(examples.iloc[0,0]) == list:
        attribute_values = {item for sublist in examples.iloc[:,0] for item in sublist}

        information_entropy = 0
        total = len(examples.index)
        header = list(examples.columns)
        for attribute_value in attribute_values:
            mask = examples.iloc[:,0].apply(lambda x: attribute_value in x)
            outcomes = examples[mask].iloc[:,-1]
            outcomes = outcomes.reset_index(drop = True)
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
            outcomes = outcomes.reset_index(drop = True)
            value_entropy = entropy(outcomes)
            outcome_count = value_counter(outcomes)
            for count in outcome_count.values():
                information_entropy += count/total * value_entropy

    return entire_entropy - information_entropy


def best_attribute(examples):
    entire_entropy = entropy(examples.iloc[:,-1])

    attributes_entropy = []

    for i in range(len(examples.columns)-1):
        attributes_entropy.append(information_gain(examples.iloc[:,[i,-1]], entire_entropy))

    header = list(examples.columns)

    return header[attributes_entropy.index(max(attributes_entropy))]


def decision_tree(examples):
    tree = Tree()

    if len(set(examples.iloc[:,-1])) == 1:
        tree.root.label = examples.iloc[0,-1]
    elif len(examples.columns) == 1:
        tree.root.label = examples.iloc[:,-1].mode()[0]
    else:
        attribute = best_attribute(examples)
        tree.root.attribute = attribute
        if type(examples.loc[0,attribute]) == list:
            values = {item for sublist in examples[attribute] for item in sublist}
            for value in values:
                child_tree = Tree()
                mask = examples.iloc[:,0].apply(lambda x: value in x)
                relevant_examples = examples[mask]
                relevant_examples = relevant_examples.reset_index(drop = True)
                if relevant_examples.empty:
                    child_tree.root.label = examples.iloc[:,-1].mode()[0]
                else:
                    child_tree = decision_tree(relevant_examples.drop(columns=[attribute]))

                tree.add_child(str(value), child_tree)
        else:
            values = set(examples[attribute])
            for value in values:
                child_tree = Tree()
                relevant_examples = examples[examples[attribute] == value]
                relevant_examples = relevant_examples.reset_index(drop = True)
                if relevant_examples.empty:
                    child_tree.root.label = examples.iloc[:,-1].mode()[0]
                else:
                    child_tree = decision_tree(relevant_examples.drop(columns=[attribute]))

                tree.add_child(str(value), child_tree)
    return tree


def print_tree(value_taken: str, tree):
    print(f"(Value Taken: {value_taken}, Label: {tree.root.label}, Attribute: {tree.root.attribute})")
    for child in tree.children.items():
        print_tree(*child)


def get_rating(tree, user_input):
    #print("(Label: ",tree.root.label, " , Attribute: ", tree.root.attribute, ")")
    #print(tree.children)
    if tree.root.attribute != None:
        rating = get_rating(tree.children[user_input[tree.root.attribute]], user_input)

    else:
        rating = tree.root.label

    return rating

if __name__ == "__main__":

    movies = pd.read_table("ml-1m/movies.dat", sep="::", names=['MovieID', 'Title', 'Genres'], engine='python')
    users = pd.read_table("ml-1m/users.dat", sep="::", names=['UserID', 'Gender', 'Age', 'Occupation', 'Zip-code'], engine='python')
    ratings = pd.read_table("ml-1m/ratings.dat", sep="::", names=['UserID', 'MovieID', 'Rating', 'Timestamp'], engine='python')

    a = pd.merge(ratings, users, on='UserID', how='left')
    b = pd.merge(a, movies, on='MovieID', how='left')

    final = b.loc[:,['Gender', 'Age', 'Occupation', 'Genres', 'Rating']]
    final['Genres'] = final['Genres'].str.split(pat="|")

    #answer = decision_tree(final)
    answer = pickle.load(open('tree.bin', 'rb'))
    print_tree('Root',answer)

    movies = [
        ["Star Wars: Episode V - The Empire Strikes Back (1980)", "Action|Adventure|Fantasy|Sci-Fi", "5"],
        ["Monty Python and the Holy Grail (1974)", "Comedy", "5"],
        ["Toy Story (1995)", "Animation|Children's|Comedy", "5"],
        ["Alien (1979)", "Action|Horror|Sci-Fi|Thriller", "4"],
        ["Monty Python's Life of Brian (1979)", "Comedy", "4"],
        ["Highlander (1986)", "Action|Adventure", "4"],
        ["Jumanji (1995)", "Adventure|Children's|Fantasy", "3"],
        ["Godfather: Part III, The (1990)", "Action|Crime|Drama", "2"],
        ["Robocop 3 (1993)", "Sci-Fi|Thriller", "1"],
        ["Super Mario Bros. (1993)", "Action|Adventure|Children's|Sci-Fi", "1"]
    ]

    for movie in movies:
        user_input = {
            'Gender': "M",
            'Age': "18",
            'Occupation': "17",
            'Genres': movie[1]
        }

        genres = user_input['Genres'].split("|")

        final_rating = 0
        for i in range(len(genres)):
            user_input['Genres'] = genres[i]
            rating = get_rating(answer, user_input)
            print("Rating ", user_input['Genres'],": ", rating)
            final_rating += rating

        print("Film name:", movie[0])
        print("User rating: ", movie[2])
        print("Script Rating: ", final_rating/len(genres))

