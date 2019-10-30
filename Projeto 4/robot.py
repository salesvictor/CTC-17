import enum
import random
import world


class Movement(enum.Enum):
    LEFT = enum.auto()
    RIGHT = enum.auto()
    UP = enum.auto()
    DOWN = enum.auto()

    def slide_left(self):
        if self is Movement.LEFT:
            return Movement.DOWN
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
    points_for_tile = {
        world.Tile.FREE: -0.1,
        world.Tile.PIT: -50,
        world.Tile.WUMPUS: -100,
        world.Tile.GOLD: 100,
        world.Tile.OUT_OF_WORLD: -1,
    }

    def __init__(self, world: world.World = world.World(), policy=None, 
                 slide_left=0.2, slide_right=0.1, points=0):
        self.world = world
        self.world.set_agent(self)
        self.x = random.randrange(self.world.max_x())
        self.y = random.randrange(self.world.max_y())
        self.world.set_agent_pos(self.x, self.y)
        self.policy = policy
        self.slide_left = slide_left
        self.slide_right = slide_right
        self.points = points
        self.movements = list(Movement)

    def observe_world(self):
        print(self.world)
        current_tile = self.world.get_tile(self.x, self.y)
        self.points += self.points_for_tile[current_tile]
        if current_tile is world.Tile.OUT_OF_WORLD:
            self._go_back()
            print(self.world)
        elif current_tile is not world.Tile.FREE:
            self._restart()
            self.observe_world()

    def take_action(self):
        # TODO: implement policy
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
        return (self.x >= self.world.max_x() or self.x < 0
                or self.y >= self.world.max_y() or self.y < 0)

    def _restart(self):
        print('Restarting!')
        self.__init__(self.world, self.policy, self.slide_left, 
                      self.slide_right, self.points)

    def _go_back(self):
        if self.x == -1:
            self.x = 0
        elif self.x == self.world.max_x():
            self.x -= 1
        elif self.y == -1:
            self.y = 0
        elif self.y == self.world.max_y():
            self.y -= 1
        self.world.set_agent_pos(self.x, self.y)

    def _move(self, movement: Movement):
        dx, dy = movement.change()
        self.x += dx
        self.y += dy
        self.world.set_agent_pos(self.x, self.y)

    def __str__(self):
        return '☺'
