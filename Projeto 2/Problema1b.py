import random
import copy
import time
import math

class Game:
    def __init__(self, size):
        Game.size = size

    @classmethod
    def new_state(cls):
        new_state = set()
        for i in range(Game.size):
            pos = (random.randint(1, Game.size), random.randint(1, Game.size))
            while pos in new_state:
                pos = (random.randint(1, Game.size), random.randint(1, Game.size))
            new_state.add(pos)

        return new_state

    @classmethod
    def get_neighbor(cls, node):
        next_value = 0
        next_state = False
        for pos in node.state:
            for i in range(4):
                aux = copy.deepcopy(node.state)
                aux.remove(pos)
                new_pos = Game.get_move(i, pos)
                if new_pos:
                    aux.add(new_pos)
                    aux_value = Game.get_value(aux)
                    if len(aux) == Game.size and aux_value > node.value:
                        next_value = aux_value
                        next_state = aux
        return next_state, next_value

    @classmethod
    def get_move(cls, num, pos):
        # if num == 0 and pos[0]>1 and pos[1]>1:
        #     return (pos[0] - 1, pos[1] - 1)
        if num == 0 and pos[0]>1:
            return (pos[0] - 1, pos[1])
        # if num == 2 and pos[0]>1 and pos[1]<Game.size:
        #     return (pos[0] - 1, pos[1] + 1)
        if num == 1 and pos[1]<Game.size:
            return (pos[0], pos[1] + 1)
        # if num == 4 and pos[0]<Game.size and pos[1]<Game.size:
        #     return (pos[0] + 1, pos[1] + 1)
        if num == 2 and pos[0]<Game.size:
            return (pos[0] + 1, pos[1])
        # if num == 6 and pos[0]<Game.size and pos[1]>1:
        #     return (pos[0] + 1, pos[1] - 1)
        if num == 3 and pos[1]>1:
            return (pos[0], pos[1] - 1)
        else:
            return False

    @classmethod
    def get_value(cls, state):
        group = set()
        for pos in state:
            group.add(("r",pos[0]))
            group.add(("c",pos[1]))
            group.add(("d1",pos[0]-pos[1]))
            group.add(("d2",pos[0]+pos[1]))
        return len(group)

    @classmethod
    def is_solution(cls, node):
        if node.value == 4*Game.size:
            return True
        else:
            return False

class Node:
    def __init__(self, state, value):
        self.state = state
        self.value = value

def simullated_annealing(MainClass):
    start_time = time.time()
    temperature = 200
    init_state = MainClass.new_state()
    init_value = MainClass.get_value(init_state)
    node = Node(init_state, init_value)
    solution = node
    while temperature > 0:
        aux = MainClass.get_neighbor(node)
        if aux[0]:
            node = Node(aux[0], aux[1])
        else:
            if node.value > solution.value:
                solution = node
            approved = False
            while not approved:
                init_state = MainClass.new_state()
                init_value = MainClass.get_value(init_state)
                next_node = Node(init_state, init_value)
                if(random.uniform(0, 1) > probability(node, next_node, temperature)):
                    node = next_node
                    approved = True
                    print("Temperatura: ", temperature)
                    elapsed_time = time.time() - start_time
                    temperature -= 1/(1+elapsed_time)
    return solution

def probability(node, next_node, temperature):
    return math.exp((next_node.value - node.value)/temperature)


# def hill_climbing(MainClass):
#     solved = False
#     i = 1
#     while not solved:
#         init_state = MainClass.new_state()
#         init_value = MainClass.get_value(init_state)
#         node = Node(init_state, init_value)
#         if i == 1:
#             solution = node
#         maximum = False
#         while not maximum:
#             aux = MainClass.get_neighbor(node)
#             if aux[0]:
#                 node = Node(aux[0], aux[1])
#             else:
#                 maximum = True
#         if node.value > solution.value:
#             solution = node
#         if MainClass.is_solution(solution):
#             solved = True
#         i += 1

#     return solution
            
def main():

    start_time = time.time()

    nrainhas = Game(9)
    
    solution = simullated_annealing(nrainhas)

    elapsed_time = time.time() - start_time

    print(solution.state, solution.value, elapsed_time)

if __name__ == "__main__":
    main()
