class Node:
	def __init__(self, father, depth, state):
		self.father = father
		self.depth = depth
		self.state = state
		self.sons = []
		self.cost = None

	def setCost(self, cost):
		self.cost = cost

	def createSon(self, newSon):
		self.sons.append(newSon)

