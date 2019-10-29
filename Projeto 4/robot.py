import enum
import random
from world import Points


class Movement(enum.Enum):
    LEFT = enum.auto()
    RIGHT = enum.auto()
    UP = enum.auto()
    DOWN = enum.auto()

    def slide_left(self):
        if self is Movement.LEFT:
            return Movement.BACK
        if self is Movement.RIGHT:
            return Movement.UP
        if self is Movement.UP:
            return Movement.LEFT
        if self is Movement.DOWN:
            return Movement.RIGHT

    def slide_right(self):
        if self is Movement.LEFT:
            return Movement.UP
        if self is Movement.RIGHT:
            return Movement.DOWN
        if self is Movement.UP:
            return Movement.RIGHT
        if self is Movement.DOWN:
            return Movement.LEFT

    def change(self):
        if self is Movement.LEFT:
            return (-1, 0)
        if self is Movement.RIGHT:
            return (1, 0)
        if self is Movement.UP:
            return (0, 1)
        if self is Movement.DOWN:
            return (0, -1)


class Robot:
    def __init__(self, world, policy, slide_left = 0.2, slide_right = 0.1):
        self.x = random.randrange(len(world[0]))
        self.y = random.randrange(len(world))
        self.world = world
        self.policy = policy
        self.slide_left = slide_left
        self.slide_right = slide_right
        self.points = 0
        self.movements = list(Movement)

    def observe_world(self):
        if self._is_out_of_world():
            self.points += Points.out_of_world
            self._go_back()
        elif self._get_tile() == Tile.wumpus:
            self.points += Points.wumpus
            self._restart();
        elif self._get_tile() == Tile.gold:
            self.points += Points.gold
            self._restart();
        elif self._get_tile() == Tile.pit:
            self.points += Points.pit
            self._restart()
        else:
            self.points += Points.free

    def take_action(self):
        movement = random.choice(self.movements)
        probability = random.random()

        if probability <= self.slide_left:
            movement = movement.slide_left()
        elif probability - self.slide_left <= self.slide_right:
            movement = movement.slide_right()

        self._move(movement)

    def _get_tile(self):
        return self.world[self.y][self.x]

    def _is_out_of_world(self):
        return self.x >= len(self.world[0]) or self.x < 0
               or self.y >= len(self.world) or self.y < 0

    def _restart(self):
        self = Robot(self.world, self.policy, self.slide_left, self.slide_right)

    def _go_back(self):
        if self.x == -1:
            self.x = 0
        elif self.x == len(self.world[0]):
            self.x -= 1
        elif self.y == -1:
            self.y = 0
        elif self.y == len(self.world):
            self.y -= 1

    def _move(self, movement):
        dx, dy = movement.change()
        self.x += dx
        self.y += dy
