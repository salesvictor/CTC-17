import numpy as np
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

def greedy(node, MainClass, actions):
	for action in actions:
		node.createSon(action, MainClass.cost(action))
	if node.state == REF:
		return True
	else:
		finished = False
	while(not finished and len(node.children)):
		finished = greedy(hp.heappop(node.children), MainClass, MainClass.getActions(node.state))


