import enum

class Tile(enum.Enum):
    free = 0
    pit = 1
    wumpus = 2
    gold = 3

world = [
    [Tile.free,   Tile.pit,  Tile.free, Tile.free, Tile.free,   Tile.free, Tile.pit,  Tile.free],
    [Tile.wumpus, Tile.gold, Tile.pit,  Tile.free, Tile.free,   Tile.free, Tile.pit,  Tile.free],
    [Tile.free,   Tile.free, Tile.free, Tile.free, Tile.wumpus, Tile.gold, Tile.free, Tile.free],
    [Tile.free,   Tile.free, Tile.pit,  Tile.free, Tile.free,   Tile.free, Tile.pit,  Tile.free],
]
