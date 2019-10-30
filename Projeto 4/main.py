import robot


if __name__ == '__main__':
    robot = robot.Robot()
    for _ in range(10):
        robot.observe_world()
        print(f'Points: {robot.points}\n')
        robot.take_action()
