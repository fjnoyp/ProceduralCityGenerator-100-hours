#from FeatureObjects import * 
from objectManipulator import *
#from DecorObject import * 

'''
Constants and generic classes for use by all classes related to TestBuilding 
'''

# SIDE AND TOP EXPANDABLES 

FACE_RIGHT = 2
FACE_BOT = 3
FACE_LEFT = 4
FACE_TOP = 1

def within2DBounds(x, z, boundX, boundZ):
    return not( z >= boundZ or x >= boundX or x < 0 or z < 0)

class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def equals(self, otherPoint):
        return otherPoint.x == self.x and otherPoint.y == self.y

DIR_TOP = Point(0,1)
DIR_RIGHT = Point(1,0)
DIR_BOT = Point(0,1)
DIR_LEFT = Point(1,1)


class Point3(object):
    def __init__(self,x,y,z):
        self.x = x
        self.y = y
        self.z = z
    def equals(self, otherPoint):
        return otherPoint.x == self.x and otherPoint.y == self.y and otherPoint.z == self.z 


