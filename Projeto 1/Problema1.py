import csv
import Core.py as Core
from math import *

Cities = []
Graph = [][]

class City:
	def __init__(self, cityid, name, lat, lng):
		self.cityid = cityid
		self.name = name
		self.lat = lat
		self.lng = lng

def readMap():
	with open('australia.csv') as csvfile:
	    readCSV = csv.reader(csvfile, delimiter=',')
	    Cities.append(City(readCSV[1][0], readCSV[1][1], readCSV[1][2], readCSV[1][3]))
	    for row in readCSV[1:]:
	    	Cities.append(City(row[0], row[1], row[2], row[3]))

def getDistance(city1, city2):
	distance = sqrt(pow(city1.lat - city2.lat,2) + pow(city1.lng - city2.lng,2))
	return distance

def createGraph():
	for city in Cities:
		if city.cityid > 1 and city.cityid%2 == 0:
			if city.cityid + 2 <= len(Cities):
				Graph.append([city.cityid, city.cityid + 2, getDistance(city, Cities[city.cityid + 2])])
			Graph.append([city.cityid, city.cityid - 1, getDistance(city, Cities[city.cityid - 1])])

		else if city.cityid%2 == 1 and city.cityid > 2:
			if city.cityid + 1 <= len(Cities):
				Graph.append([city.cityid, city.cityid + 1, getDistance(city, Cities[city.cityid + 1])])
			Graph.append([city.cityid, city.cityid - 2, getDistance(city, Cities[city.cityid - 2])])

def getMinimum(curCity, endCity):


def main():
	readMap()

	startCity = Cities[5]
	endCity = Cities[219]

	createGraph()

	root = Node(None, 0, [startCity.cityid], 0)
	getMinimum(startCity, endCity)

	



if __name__ == "__main__":
    main()