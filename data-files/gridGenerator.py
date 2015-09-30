import math
import os
from random import *
from collections import OrderedDict

class gridGenerator:

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

        self.tallSpot = [uniform(.25*self.rows, .75*self.rows), uniform(.25*self.cols, .75*self.cols)]
        self.smallSpot = [uniform(1, self.rows), uniform(1, self.cols)]

    # Generate a list of information enocding each unique building
    def getBuildingList(self):
        for row in range(0, self.rows):
            for column in range(0, self.cols):

                # get a height given a min max range
                randH = self.getHeight(row, column)

                # should return a string
                name = self.cityName + '/building' + str((row*self.cols) + column) + '.obj'

                #changed to OrderedDict to facilitate file storage
                infoDict = OrderedDict([
                    ('name', name),
                    ('type', str(4)),
                    #('type', str(randint(1, 4))),
                    ('length', str(self.buildingSize)),
                    ('width', str(self.buildingSize)),
                    ('height', str(randH)),
                    ('x', str(row * (self.buildingSize + self.streetSize))),
                    ('y', str(0)),
                    ('z', str(column * (self.buildingSize + self.streetSize))),
                    # TODO: Apply random YPR?
                    ('yaw', str(0.0)),
                    ('pitch', str(0.0)),
                    ('roll', str(0.0)),
                    ('blockSize', self.buildingSize + self.streetSize)
                ])

                self.buildings.append(infoDict)

        return self.buildings


    def getHeight(self, x, y):

        # get distance from hotspots
        tallDist = self.manhattanDist(self.tallSpot, [x,y])
        smallDist = self.manhattanDist(self.smallSpot, [x,y])

        # normalize the distance
        nTall = tallDist / float(self.rows + self.cols)
        nSmall = smallDist / float(self.rows + self.cols)

        tallRange = uniform((1-(nTall)) * self.maxH, self.maxH)
        smallRange = uniform(self.minH, self.minH + (nSmall * self.minH))

        # weight based on which height spot is the building closer to
        # basic weight
        height = 0

        height = (smallDist / (smallDist + tallDist)) * smallRange + (tallDist / 2*(smallDist + tallDist)) + tallRange

        '''
        if (smallDist < tallDist):
            height =  (0.9 * tallRange) + (0.1 * smallRange)
        elif (smallDist > tallDist):
            height = (0.9 * smallRange) + (0.1 * tallRange)
        else:
            height = (smallRange + tallRange) / 2.0
        '''
        
        return int(math.ceil((height)))

    def manhattanDist(self, posA, posB):
        return 1 + abs(posA[0] - posB[0]) + abs(posA[1] - posB[1])

    
