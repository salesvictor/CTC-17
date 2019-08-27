class Node:
	def __init__(self, parent, depth, state, cost):
		self.parent = parent
		self.depth = depth
		self.state = state
		self.cost = cost
		self.children = []

	def createSon(self, state, cost):
		child = Node(self, self.depth + 1, state, cost)
		self.children.append(child)
