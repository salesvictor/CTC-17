import heapq as hp

class Node:
    def __init__(self, parent, depth, state, cost):
        self.parent = parent
        self.depth = depth
        self.state = state
        self.cost = cost
        self.children = []

    def __lt__(self, other):
        return self.cost < other.cost

    def createChild(self, state, cost):
        child = Node(self, self.depth + 1, state, cost)
        hp.heappush(self.children, child)

def greedy(node, MainClass):
    print(f'depth: {node.depth}\ncost:{node.cost}\nstate:\n{MainClass.construct_by_state(node.state[-1])}')

    # Check if in the final state
    if MainClass.is_goal(node.state):
        return node

    # If not, check children
    actions = MainClass.getActions(node.state)
    for action in actions:
        node.createChild(action, MainClass.cost(action))

    while node.children:
        leaf_node = greedy(hp.heappop(node.children), MainClass)
        if leaf_node == None:
            continue
        elif MainClass.is_goal(leaf_node.state):
            return leaf_node
        elif not leaf_node.children:
            return None

    return None
