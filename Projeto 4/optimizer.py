import copy
import robot
import world


def log(utility_map: list, verbose: bool) -> None:
    if verbose:
        for line in utility_map:
            for value in line:
                print(f'{value:7.2f}', end=' ')
            print()
        print()


def equals(actual_map: list, previous_map: list, tolerance: float = 1e-2) -> bool:
    for y, line in enumerate(actual_map):
        for x, _ in enumerate(line):
            if abs(actual_map[y][x] - previous_map[y][x]) > tolerance:
                return False
    return True


def optimize_utility(robot: robot.Robot, world: world.World,
                     verbose: bool = False) -> None:
    utility_map = [[0 for _ in range(world.max_x() + 2)]
                   for _ in range(world.max_y() + 2)]
    previous_map = copy.deepcopy(utility_map)

    reinforcement_for_tile = robot.reinforcement_for_tile

    while True:
        log(utility_map, verbose)
        for y, line in enumerate(utility_map):
            for x, _ in enumerate(line):
                current_tile = world.get_tile(x-1, y-1)
                utility_map[y][x] = reinforcement_for_tile[current_tile]
                gained_utilities = []
                if current_tile is world.Tile.FREE:
                    for forward_movement in robot.movements:
                        left_slide_movement = forward_movement.slide_left()
                        right_slide_movement = forward_movement.slide_right()

                        possible_movements = [forward_movement, left_slide_movement,
                                              right_slide_movement]
                        probabilities = [robot.forward_probability,
                                         robot.slide_left_probability, 
                                         robot.slide_right_probability]

                        gained_utility = 0
                        for movement, probability in zip(possible_movements, probabilities):
                            dx, dy = movement.change()
                            new_x = x + dx
                            new_y = y + dy

                            if (0 <= new_x < world.max_x() and
                                0 <= new_y < world.max_y()):
                                gained_utility += probability * previous_map[new_y][new_x]
                            else:
                                gained_utility += probability * reinforcement_for_tile[world.Tile.OUT_OF_WORLD]

                        gained_utilities.append(gained_utility)

                    utility_map[y][x] += max(gained_utilities)

        if equals(utility_map, previous_map):
            break

        previous_map = copy.deepcopy(utility_map)
