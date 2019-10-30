import enum
import robot


class Tile(enum.Enum):
    FREE = enum.auto()
    PIT = enum.auto()
    WUMPUS = enum.auto()
    GOLD = enum.auto()
    OUT_OF_WORLD = enum.auto()

    def __str__(self):
        if self is Tile.PIT:
            return '○'
        if self is Tile.WUMPUS:
            return '☻'
        if self is Tile.GOLD:
            return '♦'
        return ' '


class World:
    def __init__(self, agent: object = None):
        self._world = [
            ['╔', '═',         '═',       '═',       '═',       '═',         '═',       '═',       '═',       '╗\n'],
            ['║', Tile.FREE,   Tile.PIT,  Tile.FREE, Tile.FREE, Tile.FREE,   Tile.FREE, Tile.PIT,  Tile.FREE, '║\n'],
            ['║', Tile.WUMPUS, Tile.GOLD, Tile.PIT,  Tile.FREE, Tile.FREE,   Tile.FREE, Tile.PIT,  Tile.FREE, '║\n'],
            ['║', Tile.FREE,   Tile.FREE, Tile.FREE, Tile.FREE, Tile.WUMPUS, Tile.GOLD, Tile.FREE, Tile.FREE, '║\n'],
            ['║', Tile.FREE,   Tile.FREE, Tile.PIT,  Tile.FREE, Tile.FREE,   Tile.FREE, Tile.PIT,  Tile.FREE, '║\n'],
            ['╚', '═',         '═',       '═',       '═',       '═',         '═',       '═',       '═',       '╝'],
        ]
        self._agent = agent
        self._agent_pos = (None, None)

    def max_x(self):
        return len(self._world[0]) - 2

    def max_y(self):
        return len(self._world) - 2

    def set_agent(self, agent):
        self._agent = agent

    def set_agent_pos(self, x: int, y: int):
        current_tile = self.get_tile(x, y)
        self._agent_pos = (x+1, y+1)

        return current_tile

    def get_tile(self, x: int, y: int):
        if (x == -1 or y == -1 or x == len(self._world[0]) - 2
            or y == len(self._world) - 2):
            return Tile.OUT_OF_WORLD
        return self._world[y+1][x+1]

    def __str__(self):
        world_str = ''
        for y, line in enumerate(self._world):
            for x, column in enumerate(line):
                if x == self._agent_pos[0] and y == self._agent_pos[1]:
                    world_str += str(self._agent)
                    if x == len(self._world[0]) - 1:
                        world_str += '\n'
                else:
                    world_str += str(column)

        return world_str
