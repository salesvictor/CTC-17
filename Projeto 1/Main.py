from Core import Node, greedy
from Problema2 import Game

if __name__ == '__main__':
    game = Game(9)
    game.shuffle()
    print(game)

    root = Node(None, 0, [game.state], Game.cost([game.state]))
    solution = greedy(root, Game)
    print(f'Cost: {solution.cost}\nFinal State:\n{Game.construct_by_state(solution.state[-1])}')
