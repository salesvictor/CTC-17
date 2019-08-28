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

        def createSon(self, state, cost):
            child = Node(self, self.depth + 1, state, cost)
            hp.heappush(self.children, child)

def greedy(node, MainClass):

    # Check if in the final state
    if node.state == MainClass.goal_state:
        return node

    # Get possible actions
	actions = MainClass.getActions(node.state)
    
    # If not, check children
    for action in actions:
        node.createSon(action, MainClass.cost(action))

    while node.children:
        leaf_node = greedy(hp.heappop(node.children), MainClass)
        if leaf_node == None:
            continue
        elif leaf_node.state == MainClass.goal_state:
            return leaf_node
        elif not leaf_node.children:
            return None

    return None
