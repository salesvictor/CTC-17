class Node:
	def __init__(self, father, depth, state, cost):
		self.father = father
		self.depth = depth
		self.state = state
		self.cost = cost
		self.sons = []

	def createSon(self, state, cost):
		son = Node(self, self.depth + 1, state, cost)
		self.sons.append(son)
		son.father = self

