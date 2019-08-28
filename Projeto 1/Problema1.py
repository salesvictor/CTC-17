import csv
import copy
import Core as Core

class Cities:
    def __init__(self, start, finish):
        Cities.list = []
        Cities.graph = []
        Cities.start = start
        Cities.finish = finish

    @classmethod
    def cost(cls, action):
        city = Cities.list[action[-1]]
        goal_city = Cities.list[Cities.finish]
        distance = ((city.lat - goal_city.lat) ** 2 + (city.lng - goal_city.lng) ** 2) ** .5
        return distance

    @classmethod
    def getActions(cls, state):
        actions = []
        for city in Cities.graph[state[-1]]:
            if not city in state:
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
                australia.graph[city.cityid].append(city.cityid + 2)
                australia.graph[city.cityid + 2].append(city.cityid)
                australia.graph[city.cityid].append(city.cityid - 1)
                australia.graph[city.cityid - 1].append(city.cityid)

        elif city.cityid%2 == 1 and city.cityid > 2:
            if city.cityid + 1 < len(australia.list):
                australia.graph[city.cityid].append(city.cityid + 1)
                australia.graph[city.cityid + 1].append(city.cityid)
                australia.graph[city.cityid].append(city.cityid - 2)
                australia.graph[city.cityid - 2].append(city.cityid)

def main():
    australia = Cities(5, 219)
    readMap(australia)
    createGraph(australia)

    root = Core.Node(None, 0, [5], 0)
    Core.greedy(root,Cities)


if __name__ == "__main__":
    main()
