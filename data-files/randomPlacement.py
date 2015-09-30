import math
from random import *
from collections import OrderedDict

class randomPlacement:

    def __init__(self, buildingRows, buildingColumns, buildingSize, streetSize, name, minHeight, maxHeight):
        self.rows = buildingRows
        self.cols = buildingColumns
        self.buildingSize = buildingSize
        self.streetSize = streetSize
        self.cityName = name
        self.buildings = []

        # Instantiate city info, like tall/short building hotspots
        self.minH = minHeight
        self.maxH = maxHeight

    # Generate a list of information enocding each unique building
    def getBuildingList(self):
        for i in range(0,50):

            name = self.cityName + '/building' + str(i) + '.obj'
            x = randint(0,250)
            z = randint(0,250)
            #theta = 30
            #while abs(x%10-5)<2 or abs(z%20-10)<4:
            #    x = randint(0,300)
            #    z = randint(0,300)
            randH = randint(30,60)

            #changed to OrderedDict to facilitate file storage
            infoDict = OrderedDict([
                ('name', name),
                ('type', str(1)),
                ('length', str(self.buildingSize + randint(0,60))),
                ('width', str(self.buildingSize + randint(0,40))),
                ('height', str(randH)),
                ('x', str(x)),
                ('y', str(0)),
                ('z', str(z)),
                # TODO: Apply random YPR?
                ('yaw', str(randint(0,360))),
                ('pitch', str(0)),
                ('roll', str(0))
            ])

            self.buildings.append(infoDict)

        return self.buildings


    
