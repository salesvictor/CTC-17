import optimizer
import robot
import world


if __name__ == '__main__':
    world = world.World()
    robot = robot.Robot(world)
    print(world)
    optimizer.optimize_utility(robot, world, True)
