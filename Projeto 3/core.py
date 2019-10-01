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
    #print(f"(Value Taken: {value_taken}, Label: {tree.root.label}, Attribute: {tree.root.attribute})")
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
    #print_tree('Root',answer)

    movies = [
        ["1", "Toy Story (1995)", "Animation|Children's|Comedy", "5"],
        ["2", "Jumanji (1995)", "Adventure|Children's|Fantasy", "2"],
        ["5", "Father of the Bride Part II (1995)", "Comedy", "1"],
        ["32", "Twelve Monkeys (1995)", "Drama|Sci-Fi", "5"],
        ["34", "Babe (1995)", "Children's|Comedy|Drama", "1"],
        ["39", "Clueless (1995)", "Comedy|Romance", "5"],
        ["48", "Pocahontas (1995)", "Animation|Children's|Musical|Romance", "5"],
        ["73", "Misérables, Les (1995)", "Drama|Musical", "3"],
        ["150", "Apollo 13 (1995)", "Drama", "3"],
        ["158", "Casper (1995)", "Adventure|Children's", "4"],
        ["194", "Smoke (1995)", "Drama", "2"],
        ["235", "Ed Wood (1994)", "Comedy|Drama", "4"],
        ["260", "Star Wars: Episode IV - A New Hope (1977)", "Action|Adventure|Fantasy|Sci-Fi", "2"],
        ["261", "Little Women (1994)", "Drama", "4"],
        ["296", "Pulp Fiction (1994)", "Crime|Drama", "5"],
        ["306", "Three Colors: Red (1994)", "Drama", "4"],
        ["307", "Three Colors: Blue (1993)", "Drama", "4"],
        ["308", "Three Colors: White (1994)", "Drama", "4"],
        ["356", "Forrest Gump (1994)", "Comedy|Romance|War", "4"],
        ["362", "Jungle Book, The (1994)", "Adventure|Children's|Romance", "3"],
        ["364", "Lion King, The (1994)", "Animation|Children's|Musical", "5"],
        ["441", "Dazed and Confused (1993)", "Comedy", "5"],
        ["480", "Jurassic Park (1993)", "Action|Adventure|Sci-Fi", "4"],
        ["484", "Lassie (1994)", "Adventure|Children's", "3"],
        ["541", "Blade Runner (1982)", "Film-Noir|Sci-Fi", "4"],
        ["575", "Little Rascals, The (1994)", "Children's|Comedy", "5"],
        ["582", "Metisse (Café au Lait) (1993)", "Comedy", "3"],
        ["586", "Home Alone (1990)", "Children's|Comedy", "5"],
        ["587", "Ghost (1990)", "Comedy|Romance|Thriller", "3"],
        ["589", "Terminator 2: Judgment Day (1991)", "Action|Sci-Fi|Thriller", "1"],
        ["590", "Dances with Wolves (1990)", "Adventure|Drama|Western", "4"],
        ["592", "Batman (1989)", "Action|Adventure|Crime|Drama", "5"],
        ["594", "Snow White and the Seven Dwarfs (1937)", "Animation|Children's|Musical", "4"],
        ["595", "Beauty and the Beast (1991)", "Animation|Children's|Musical", "5"],
        ["597", "Pretty Woman (1990)", "Comedy|Romance", "4"]
    ]

    for movie in movies:
        user_input = {
            'Gender': "F",
            'Age': "25",
            'Occupation': "14",
            'Genres': movie[2]
        }

        genres = user_input['Genres'].split("|")

        final_rating = 0
        for i in range(len(genres)):
            user_input['Genres'] = genres[i]
            rating = get_rating(answer, user_input)
            #print("Rating ", user_input['Genres'],": ", rating)
            final_rating += rating

        movie_ratings = ratings[ratings.MovieID == int(movie[0])].iloc[:,2]

        print(movie[1], " & ", movie[3], " & ", final_rating/len(genres), " & ", int(movie_ratings.mean()), " & ", movie_ratings.mode()[0], " \\\\")
