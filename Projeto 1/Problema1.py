import csv
import Core as Core
import copy
from math import *

class Cities:
	def __init__(self, start, finish):
		Cities.list = []
		Cities.graph = []
		Cities.start = start
		Cities.finish = finish

	@classmethod
	def cost(cls, action):
		distance = sqrt(pow((Cities.list[action[-1]]).lat - (Cities.list[Cities.finish]).lat,2) + pow((Cities.list[action[-1]]).lng - (Cities.list[Cities.finish]).lng,2))
		return distance

	@classmethod
	def getActions(cls, state):
		actions = []
		for city in Cities.graph[state[-1]]:
			aux = copy.deepcopy(state)
			aux.append(city)
			actions.append(aux)
		return actions

	@classmethod
	def is_goal(cls, historic):
		return historic[-1] == Cities.finish

class City:
	def __init__(self, cityid, name, lat, lng):
		self.cityid = cityid
		self.name = name
		self.lat = lat
		self.lng = lng

def readMap(australia):
	with open('australia.csv') as csvfile:
	    readCSV = list(csv.reader(csvfile, delimiter=','))
	    australia.list.append(City(int(readCSV[1][0]), readCSV[1][1], float(readCSV[1][2]), float(readCSV[1][3])))
	    australia.graph.append([])
	    for row in readCSV[1:]:
	    	australia.list.append(City(int(row[0]), row[1], float(row[2]), float(row[3])))
	    	australia.graph.append([])

def createGraph(australia):
	for city in australia.list:
		if city.cityid > 1 and city.cityid%2 == 0:
			if city.cityid + 2 < len(australia.list):
				if (city.cityid + 2) not in australia.graph[city.cityid]:
					australia.graph[city.cityid].append(city.cityid + 2)
				if city.cityid not in australia.graph[city.cityid + 2]:
					australia.graph[city.cityid + 2].append(city.cityid)
			if (city.cityid - 1) not in australia.graph[city.cityid]:
				australia.graph[city.cityid].append(city.cityid - 1)
			if city.cityid not in australia.graph[city.cityid - 1]:
				australia.graph[city.cityid - 1].append(city.cityid)

		elif city.cityid%2 == 1 and city.cityid > 2:
			if city.cityid + 1 < len(australia.list):
				if (city.cityid + 1) not in australia.graph[city.cityid]:
					australia.graph[city.cityid].append(city.cityid + 1)
				if city.cityid not in australia.graph[city.cityid + 1]:
					australia.graph[city.cityid + 1].append(city.cityid)
			if (city.cityid - 2) not in australia.graph[city.cityid]:
				australia.graph[city.cityid].append(city.cityid - 2)
			if city.cityid not in australia.graph[city.cityid - 2]:
				australia.graph[city.cityid - 2].append(city.cityid)

def main():
	australia = Cities(5, 219)
	readMap(australia)
	createGraph(australia)

	print(australia.graph)

	root = Core.Node(None, 0, [5], 0)
	Core.greedy(root,Cities)
	

if __name__ == "__main__":
    main()