import secrets


class Robot:
    def __init__(self, world, policy, slide_left = 0.2, slide_right = 0.1):
        self.x = secrets.randbelow(len(world[0]))
        self.y = secrets.randbelow(len(world))
        self.world = world
        self.policy = policy
        self.slide_left = slide_left
        self.slide_right = slide_right

    def observe_world(self):
        if self._is_out_of_world():
            pass

        if self._get_tile() == Tile.wumpus:
            pass
        elif self._get_tile() == Tile.gold:
            pass
        elif self._get_tile() == Tile.pit:
            pass

    def take_action(self):
        pass

    def _get_tile(self):
        return self.world[self.y][self.x]

    def _is_out_of_world(self):
        return self.x >= len(self.world[0]) or self.x < 0
               or self.y >= len(self.world) or self.y < 0
