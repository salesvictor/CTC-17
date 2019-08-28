import csv
import Core as Core
from math import *

class Cities:
	def __init__(self):
		self.list = []
		self.graph = []

	@classmethod
	def cost(cls, action):
		distance = sqrt(pow(action[0].lat - action[1].lat,2) + pow(action[0].lng - action[1].lng,2))
		return distance

	@classmethod
	def getActions(cls, state):


class City:
	def __init__(self, cityid, name, lat, lng):
		self.cityid = cityid
		self.name = name
		self.lat = lat
		self.lng = lng

def readMap(australia):
	with open('australia.csv') as csvfile:
	    readCSV = csv.reader(csvfile, delimiter=',')
	    australia.list.append(City(readCSV[1][0], readCSV[1][1], readCSV[1][2], readCSV[1][3]))
	    australia.graph.append([])
	    for row in readCSV[1:]:
	    	australia.list.append(City(row[0], row[1], row[2], row[3]))
	    	australia.graph.append([])

def createGraph(australia):
	for city in australia.list:
		if city.cityid > 1 and city.cityid%2 == 0:
			if city.cityid + 2 <= len(australia.list):
				australia.graph[city.cityid].append(city.cityid + 2)
				australia.graph[city.cityid + 2].append(city.cityid)
			australia.graph[city.cityid].append(city.cityid - 1)
			australia.graph[city.cityid - 1].append(city.cityid)

		else if city.cityid%2 == 1 and city.cityid > 2:
			if city.cityid + 1 <= len(australia.list):
				australia.graph[city.cityid].append(city.cityid + 1)
				australia.graph[city.cityid + 1].append(city.cityid)
			australia.graph[city.cityid].append(city.cityid - 2)
			australia.graph[city.cityid - 2].append(city.cityid)

def main():
	australia = Cities()
	readMap(australia)
	createGraph(australia)

	startCity = australia.list[5]
	endCity = australia.list[219]

	root = Core.Node(None, 0, [startCity.cityid], 0)
	

if __name__ == "__main__":
    main()