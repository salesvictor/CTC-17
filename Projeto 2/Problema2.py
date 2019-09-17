import random
import copy
import time
import math

class Game:
    def __init__(self, size):
        Game.size = size

    @classmethod
    def new_state(cls):
        return (random.uniform(-Game.size,Game.size), random.uniform(-Game.size,Game.size))

    @classmethod
    def get_neighbor(cls, node):
        next_value = 0
        next_state = False
        for i in range(4):
            new_pos = Game.get_move(i, node.state)
            if new_pos:
                aux_value = Game.get_value(new_pos)
                if aux_value > node.value:
                    next_value = aux_value
                    next_state = new_pos
        return next_state, next_value

    @classmethod
    def get_move(cls, num, pos):
        # if num == 0 and pos[0]>1 and pos[1]>1:
        #     return (pos[0] - 1, pos[1] - 1)
        if num == 0:
            return (pos[0] - 0.01, pos[1])
        # if num == 2 and pos[0]>1 and pos[1]<Game.size:
        #     return (pos[0] - 1, pos[1] + 1)
        if num == 1:
            return (pos[0], pos[1] + 0.01)
        # if num == 4 and pos[0]<Game.size and pos[1]<Game.size:
        #     return (pos[0] + 1, pos[1] + 1)
        if num == 2:
            return (pos[0] + 0.01, pos[1])
        # if num == 6 and pos[0]<Game.size and pos[1]>1:
        #     return (pos[0] + 1, pos[1] - 1)
        if num == 3:
            return (pos[0], pos[1] - 0.01)
        else:
            return False

    @classmethod
    def get_value(cls, state):
        x = state[0]
        y = state[1]
        return 4*math.exp(-(x**2+y**2))+math.exp(-((x-5)**2+(y-5)**2))+math.exp(-((x+5)**2+(y-5)**2))+math.exp(-((x-5)**2+(y+5)**2))+math.exp(-((x+5)**2+(y+5)**2))

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
    num_iter = 0
    temperature = 100
    init_state = MainClass.new_state()
    init_value = MainClass.get_value(init_state)
    node = Node(init_state, init_value)
    solution = node
    while temperature > 0:
        #print(node.state, node.value)
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
                #print("Trying: ", next_node.state, next_node.value)
                if(random.uniform(0, 1) > probability(node, next_node, temperature)):
                    node = next_node
                    approved = True
                    print("Temperatura: ", temperature)
                    temperature -= 0.001*(1+num_iter)
                    num_iter += 1
    return solution

def probability(node, next_node, temperature):
    return math.exp((next_node.value - node.value)/temperature)
            
def main():

    start_time = time.time()

    nrainhas = Game(10)
    
    solution = simullated_annealing(nrainhas)

    elapsed_time = time.time() - start_time

    print(solution.state, solution.value, elapsed_time)

if __name__ == "__main__":
    main()
