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
    # print(f'depth: {node.depth}\ncost:{node.cost}\nstate:\n{node.state[-1]}')

    # Check if in the final state
    if MainClass.is_goal(node.state):
        #print(node.state, node.depth)
        return node

    # Get possible actions
    actions = MainClass.getActions(node.state)

    # If not, check children
    for action in actions:
        node.createChild(action, MainClass.h_cost(action))

    while node.children:
        leaf_node = greedy(hp.heappop(node.children), MainClass)
        if leaf_node == None:
            continue
        elif MainClass.is_goal(leaf_node.state):
            return leaf_node
        elif not leaf_node.children:
            return None

    return None

def a_star(node, MainClass):
    # print(f'depth: {node.depth}\ncost:{node.cost}\nstate:\n{node.state[-1]}')

    # Check if in the final state
    if MainClass.is_goal(node.state):
        #print(node.state, node.depth)
        return node

    # Get possible actions
    actions = MainClass.getActions(node.state)

    # If not, check children
    for action in actions:
        node.createChild(action, MainClass.g_cost(action) + MainClass.h_cost(action))

    while node.children:
        leaf_node = a_star(hp.heappop(node.children), MainClass)
        if leaf_node == None:
            continue
        elif MainClass.is_goal(leaf_node.state):
            return leaf_node
        elif not leaf_node.children:
            return None

    return None
