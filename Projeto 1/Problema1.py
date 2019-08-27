import csv
import Core.py as Core

Cities = []

class City:
	def __init__(self, id, name, lat, lng):
		self.id = id
		self.name = name
		self.lat = lat
		self.lng = lng

def readMap():
	with open('australia.csv') as csvfile:
	    readCSV = csv.reader(csvfile, delimiter=',')
	    for row in readCSV[1:]:
	    	Cities[row[0]] = City(row[0], row[1], row[2], row[3])

def getNextCities(City):
	
def getMinimum(CityA, CityB):


def main():
	readMap()

	AliceSprings = City(5)
	Yulara = City(219)
	getMinimum(CityA, CityB)

	



if __name__ == "__main__":
    main()