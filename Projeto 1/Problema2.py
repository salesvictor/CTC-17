import copy
import secrets
import Core

class Game:
    _delta_x = [-1,1, 0, 0]
    _delta_y = [ 0,0,-1, 1]
    _delta = tuple((dx, dy) for dx, dy in zip(_delta_x, _delta_y))

    def __init__(self, dimension):
        self.dimension = dimension
        self.blank_position = (dimension-1, dimension-1)
        Game.goal_state = [[i+1 for i in range(j*dimension, j*dimension+dimension)] for j in range(dimension)]
        Game.goal_state[-1][-1] = None
        self.state = copy.deepcopy(Game.goal_state)

    def __str__(self):
        string = ''
        for line in self.state:
            for column in line:
                if column != None:
                    string += f'{column}'
                string += '\t'
            string += '\n'

        return string

    def isValid(self, position):
        if 0 <= position[0] <= self.dimension-1 and 0 <= position[1] <= self.dimension-1:
            return True
        return False

    def shuffle(self, moves = 10):
        for _ in range(moves):
            while True:
                delta_position = secrets.choice(Game._delta)
                new_position = tuple(self.blank_position[i]+delta_position[i] for i in range(2))
                if self.isValid(new_position):
                    break
            self.move(delta_position)

    def move(self, delta_position):
        new_position = tuple(self.blank_position[i]+delta_position[i] for i in range(2))
        other_num = self.state[new_position[0]][new_position[1]]
        self.state[new_position[0]][new_position[1]] = None
        self.state[self.blank_position[0]][self.blank_position[1]] = other_num
        self.blank_position = new_position

    @classmethod
    def construct_by_state(cls, state):
        dimension = len(state)
        for x in range(dimension):
            for y in range(dimension):
                if state[x][y] == None:
                    blank_position = (x, y)
        game = Game(dimension)
        game.blank_position = blank_position
        game.state = state

        return game

    @classmethod
    def g_cost(cls, historic):
        initial = Game.construct_by_state(historic[0]).blank_position
        final = Game.construct_by_state(historic[-1]).blank_position
        return abs(final[0]-initial[0]) + abs(final[1]-initial[1])

    @classmethod
    def h_cost(cls, historic):
        cost = 0
        state = historic[-1]
        dimension = len(state)
        for x, line in enumerate(state):
            for y, number in enumerate(line):
                if number == None:
                    target_x = dimension-1
                    target_y = dimension-1
                else:
                    target_x = (number-1) // dimension
                    target_y = (number-1) % dimension
                cost += abs(x-target_x)+abs(y-target_y)
                #print(f'cost({x}, {y}) = {cost}\tshould be: ({target_x}, {target_y})')
        return cost

    @classmethod
    def getActions(cls, historic):
        actions = []
        game = Game.construct_by_state(historic[-1])
        possible_moves = [tuple(game.blank_position[i]+Game._delta[j][i] for i in range(2)) for j in range(4)]
        for i, move in enumerate(possible_moves):
            if game.isValid(move):
                new_game = copy.deepcopy(game)
                new_game.move(new_game._delta[i])
                if not new_game.state in historic:
                    actions.append(historic+[new_game.state])

        return actions

    @classmethod
    def is_goal(cls, historic):
        return historic[-1] == Game.goal_state

if __name__ == '__main__':
    game = Game(9)
    game.shuffle()
    game_original = copy.deepcopy(game)

    print('=============== USING GREEDY ===============')
    root = Core.Node(None, 0, [game.state], 0)
    solution = Core.greedy(root, Game)
    for idx, state in enumerate(solution.state):
        print(f'Step: {idx+1}\nState:\n{Game.construct_by_state(state)}')

    game = game_original
    print('=============== USING A* ===============')
    root = Core.Node(None, 0, [game.state], 0)
    solution = Core.a_star(root, Game)
    for idx, state in enumerate(solution.state):
        print(f'Step: {idx+1}\nState:\n{Game.construct_by_state(state)}')
