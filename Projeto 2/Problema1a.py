import random
import copy
import time
import sys

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

def hill_climbing_max_tries(MainClass):
    for i in range(100):
        init_state = MainClass.new_state()
        init_value = MainClass.get_value(init_state)
        node = Node(init_state, init_value)
        if i == 0:
            solution = node
        maximum = False
        while not maximum:
            aux = MainClass.get_neighbor(node)
            if aux[0]:
                node = Node(aux[0], aux[1])
            else:
                maximum = True
        if node.value > solution.value:
            solution = node

    return solution

def hill_climbing_until_solved(MainClass):
    solved = False
    i = 1
    while not solved:
        init_state = MainClass.new_state()
        init_value = MainClass.get_value(init_state)
        node = Node(init_state, init_value)
        if i == 1:
            solution = node
        maximum = False
        while not maximum:
            aux = MainClass.get_neighbor(node)
            if aux[0]:
                node = Node(aux[0], aux[1])
            else:
                maximum = True
        if node.value > solution.value:
            solution = node
        if MainClass.is_solution(solution):
            solved = True
        i += 1

    return solution
            
def main():
    nrainhas = Game(int(sys.argv[1]))

    funcs = [hill_climbing_until_solved, hill_climbing_max_tries]
    func = int(sys.argv[2])
    
    start_time = time.time()
    solution = funcs[func](nrainhas)
    elapsed_time = time.time() - start_time

    print(f'{solution.state};{solution.value};{elapsed_time}')

if __name__ == "__main__":
    main()
