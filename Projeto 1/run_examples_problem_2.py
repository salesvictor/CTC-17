import copy
import Core
from Problema2 import Game

ex1 = [1 , 2 , 3 , 4 , 5 , 6 , 7 , 8 , 9 , 10 , 11 , 12 , 13 , 14 , 15 , 16 , 17 , 18 , 19 , 20 , 21 , 22 , 23 , 24 , 25 , 26 , 27 , 28 , 29 , 30 , 31 , 32 , 33 , 34 , 35 , 36 , 37 , 38 , 39 , 40 , 41 , 42 , 43 , 44 , 45 , 46 , 47 , 48 , 49 , 50 , 51 , 52 , 53 , 54 , 55 , 56 , 57 , 58 , 59 , None , 61 , 62 , 63 , 64 , 65 , 66 , 67 , 68 , 60 , 71 , 79 , 72 , 73 , 74 , 75 , 76 , 77 , 69 , 78 , 70 , 80]

state = list(zip(*[iter(ex1)] * 9))
for idx, s in enumerate(state):
    state[idx] = list(s)

game = Game.construct_by_state(state)
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

ex2 = [10 , 44 , 27 , 28 , 61 , 8 , 14 , 17 , None , 22 , 6 , 16 , 43 , 48 , 51 , 36 , 2 , 68 , 24 , 38 , 37 , 45 , 18 , 41 , 70 , 34 , 46 , 55 , 4 , 1 , 30 , 50 , 58 , 32 , 12 , 9 , 3 , 23 , 60 , 56 , 40 , 15 , 72 , 54 , 20 , 7 , 25 , 11 , 47 , 5 , 74 , 29 , 35 , 26 , 52 , 57 , 73 , 65 , 49 , 42 , 77 , 78 , 21 , 31 , 67 , 13 , 53 , 62 , 66 , 80 , 33 , 69 , 39 , 75 , 64 , 19 , 59 , 76 , 63 , 79 , 71]

state = list(zip(*[iter(ex2)] * 9))
for idx, s in enumerate(state):
    state[idx] = list(s)

game = Game.construct_by_state(state)
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
