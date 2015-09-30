from buildingType import *
from building import *
from gridGenerator import *
import math
import random
from voronoi import *
import os
import sys
from collections import OrderedDict

class cityIO:
    def __init__(self):
        self.buildings = []

    #Pass a list into the storage (mainly used to write to files)
    def loadList(self, buildings):
        self.buildings = buildings

    #Read from a cty file and construct a list of objects (currently just building)
    def read(self, filename):
        self.buildings = []
        with open(filename, 'r') as cityFile:
            tmpList = cityFile.readlines()
            infoDict = OrderedDict()
            #Current List to append to, now always building
            currentList = self.buildings
            for line in tmpList:
                data = line.split()
                #Skip empty line and comments
                if len(data)>0 and data[0][0] != '#':
                    #Type signifies the start of a new object
                    if data[0] == 'Type':
                        #Append old object
                        if len(infoDict) > 0:
                            currentList.append(infoDict)
                        infoDict = OrderedDict()
                        #Set the current list to append, currently only building
                        if data[2] == 'Building':
                            currentList = self.buildings
                        else:
                            sys.exit("Error: unknown object type " + data[2])
                    else:
                        #Append the parameters
                        infoDict[data[0]] = data[2]
        #Append the last object
        if len(infoDict) > 0:
            currentList.append(infoDict)

    #Write to a cty file.
    def write(self, filename):
        with open(filename, 'w') as cityFile:
            cityFile.write("#City " + filename +"\n\n")
            #Write all the buildings
            for building in self.buildings:
                print("Writing data for" + building.get('name'))
                cityFile.write("Type = Building \n")
                for key in building:
                    cityFile.write("    " + key + " = " + building.get(key) + "\n")
                cityFile.write("\n")

    def getBuildingList(self):
        return self.buildings

#Run cityIO.py directly to generate cty files
def main():
    #set the directory to the path of the script to allow running it from any place
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)
    
    #functions that convert int into ints and leaves other unchanged
    def toInt(l):
        for x in l:
            try:
                yield int(x)
            except ValueError:
                yield x

    print(sys.argv)
    with open(sys.argv[1], 'r') as f:
        tmpList = f.read().split()
        config = list(toInt([tmpList[3*i+2] for i in range(len(tmpList)/3)]))
        if config[0] == 'gridGenerator':
            print("Using Grid Generator")
            generator = gridGenerator(config[1], config[2], config[3], config[4], config[5]) #(1, 1, "scene/testScene")
            city = cityIO()
            city.loadList(generator.getBuildingList())
            print("Writing to City File...")
            city.write(config[5]+'.cty')
            print("Done")
        elif config[0] == 'voronoi':
            print("Next Level Troll")
            generator = voronoi(config[1], config[2], config[3], config[4], config[5], config[6], config[7])
            city = cityIO()
            city.loadList(generator.getBuildingList())
            print("Writing to City File...")
            city.write(config[5]+'.cty')
            print("Done")
        else:
            print("Error: generator type " + config[0] + " is not defined")
        f.close()

if __name__ == "__main__": main()
