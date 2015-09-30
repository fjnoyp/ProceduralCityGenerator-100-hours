from objectManipulator import *

from TestBuilding import * 
from Cube import *
from Kowloon import *
from FrustumBuilding import *
from EliBuilding import *

import random
from sys import argv
import os


# Generate a building. x,y,z: dimensions of bounding box. t:type of building, see buildingType.py. 
# name: name of the output obj file.
def generateBuilding(width, height, length, t, name, seed):
    if not seed:
        seed = random.randint(1000000)
    # Ignore the cool shit. Just list new objects after cube
    building = { 
        0 : Cube,
        1 : Kowloon,
        2 : FrustumBuilding,
        3 : EliBuilding,
        4 : TestBuilding,
#        5 : EliBuildingBridge,
    }[t.metaType](length = length, width = width, max_height = height, seed = seed).to_obj()

    '''
    # inside of to_obj, return tuple containg obj and the lights array
    if typeof(building) == typeof( (1,2) ):
        lights = building[1]
    '''

    result =  building.write(name)
    return result

def main():

    # X IS WIDTH, Z IS LENGTH
#    generateBuilding(20, 40, 20, BuildingType(0), "test0.obj")
#    generateBuilding(30, 50, 30, BuildingType(1), "test1.obj")
#    generateBuilding(20, 70, 20, BuildingType(2), "test2.obj")
 #   generateBuilding(25, 55, 25, BuildingType(3), "test3.obj")
    #generateBuilding(30,120,30,BuildingType(4),"test.obj", random.randint(0,100000))
    #generateBuilding(30,30,30,BuildingType(1),"kow202.obj", random.randint(0,100000))
    generateBuilding(20, 30, 20, BuildingType(4),  "test.obj", random.randint(0,500000))
    #generateBuilding(15, 100, 15, BuildingType(2),  "TONY.obj", random.randint(0, 50000000))
    

if __name__ == "__main__": 
    main()

    """
    for i in xrange(1, y):
        rnd = randint(1, 6)
        if rnd == 1:
            tmpobj.load("models/cube/Cube.obj")
        if rnd == 2:
            tmpobj.load("models/squarePyramid/square_pyramid_full.obj")
        if rnd == 3:
            tmpobj.load("models/squarePyramid/square_pyramid_half.obj")
        if rnd == 4:
            tmpobj.load("models/cylinders/cylinder_full_radius.obj")
        if rnd == 5:
            tmpobj.load("models/trianglarPrisms/Tri45.obj")
        if rnd == 6:
            tmpobj.load("models/cylinders/cylinder_half_radius.obj")
        tmpobj.scale(0.9)
        tmpobj.translate(0,i*2,0)
        mainobj.append(tmpobj)
    """

