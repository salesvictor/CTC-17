import secrets

class Game:
    def __init__(self, dimension):
        self.dimension = dimension
        self.blank_position = (dimension-1, dimension-1)
        self.goal_state = [[i+1 for i in range(j*dimension, j*dimension+dimension)] for j in range(dimension)]
        self.goal_state[-1][-1] = None
        self.state = self.goal_state

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
            print(position)
            return True
        return False

    def shuffle(self, moves = 10):
        delta_x = [-1,1, 0, 0]
        delta_y = [ 0,0,-1, 1]
        delta = tuple((dx, dy) for dx, dy in zip(delta_x, delta_y))
        for _ in range(moves):
            while True:
                delta_position = secrets.choice(delta)
                new_position = tuple(self.blank_position[i]+delta_position[i] for i in range(2))
                if self.isValid(new_position):
                    break
            self.move(delta_position)
            print(self)

    def move(self, delta_position):
        new_position = tuple(self.blank_position[i]+delta_position[i] for i in range(2))
        other_num = self.state[new_position[0]][new_position[1]]
        self.state[new_position[0]][new_position[1]] = None
        self.state[self.blank_position[0]][self.blank_position[1]] = other_num
        self.blank_position = new_position

    def cost(cls, action):
        return 1

Cities.cost(action)

game = Game(10)
print(game)

game.shuffle(10)
