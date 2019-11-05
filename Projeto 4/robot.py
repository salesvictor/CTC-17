import enum
import random
import world



class Robot:
    class Movement(enum.Enum):
        LEFT = enum.auto()
        RIGHT = enum.auto()
        UP = enum.auto()
        DOWN = enum.auto()

        def slide_left(self):
            if self is Robot.Movement.LEFT:
                return Robot.Movement.DOWN
            if self is Robot.Movement.RIGHT:
                return Robot.Movement.UP
            if self is Robot.Movement.UP:
                return Robot.Movement.LEFT
            if self is Robot.Movement.DOWN:
                return Robot.Movement.RIGHT

        def slide_right(self):
            if self is Robot.Movement.LEFT:
                return Robot.Movement.UP
            if self is Robot.Movement.RIGHT:
                return Robot.Movement.DOWN
            if self is Robot.Movement.UP:
                return Robot.Movement.RIGHT
            if self is Robot.Movement.DOWN:
                return Robot.Movement.LEFT

        def change(self):
            if self is Robot.Movement.LEFT:
                return (-1, 0)
            if self is Robot.Movement.RIGHT:
                return (1, 0)
            if self is Robot.Movement.UP:
                return (0, 1)
            if self is Robot.Movement.DOWN:
                return (0, -1)

    reinforcement_for_tile = {
        world.World.Tile.FREE: -0.1,
        world.World.Tile.PIT: -50,
        world.World.Tile.WUMPUS: -100,
        world.World.Tile.GOLD: 100,
        world.World.Tile.OUT_OF_WORLD: -1,
    }

    def __init__(self, world: world.World = world.World(), policy=None, 
                 slide_left_probability=0.2, slide_right_probability=0.1,
                 points=0):
        self.world = world
        self.world.set_agent(self)
        self.x = random.randrange(self.world.max_x())
        self.y = random.randrange(self.world.max_y())
        self.world.set_agent_pos(self.x, self.y)
        self.policy = policy
        self.slide_left_probability = slide_left_probability
        self.slide_right_probability = slide_right_probability
        self.forward_probability = 1 - slide_left_probability - slide_right_probability
        self.points = points
        self.movements = list(Robot.Movement)

    def observe_world(self):
        print(self.world)
        current_tile = self.world.get_tile(self.x, self.y)
        self.points += self.reinforcement_for_tile[current_tile]
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
