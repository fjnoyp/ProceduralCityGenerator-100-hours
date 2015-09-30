
from GenericClasses import * 
from objectManipulator import *

import random 
import math


'''
Places FeatureObjects 
'''

#Places a given featureObject in a regular pattern
class FeatureObjectPlacer(): 
        
    def setPlacingBehavior( self, startHeight, lenX, lenZ, repX, repZ, feature ):
        self.startHeight = startHeight
        self.lenX = lenX
        self.lenZ = lenZ
        self.repX = repX
        self.repZ = repZ
        self.feature = feature

    def applyFeature(self, relX, relZ, x, z, chance, grid, occupancyGrid):
        self.feature.setHeight( self.startHeight +1) 
        for xi in range(x, self.lenX, self.repX):
            for zi in range(z, self.lenZ, self.repZ):
                if random.randint(0,chance) == 0: 
                    self.feature.expand(relX,relZ, xi,zi,grid,occupancyGrid)


'''
FeatureObject - set of primitives that make up some feature, also has support to expand out smaller primitives for decoration 

DecorObject - decorations to add to FeatureObjects / other Objects 
'''

#expands out set of large primitives and generates their randomized decorations
class FeatureObject():

    def __init__(self):
        self.primitives = []
        self.relLocs = []
        self.sExpandables = [] 

    # spread constructor method calls to make initialization more clear 
    def setHeight(self, startHeight):
        self.startHeight = startHeight 

    def setExpandables(self, sideExpandables, topExpandables):
        self.sideExpandables = sideExpandables
        self.topExpandables = topExpandables 
    
    def addFeature(self, relX, relY, relZ, isSideExpandable, thePrimitive):
        dir = 0
        if(relX>0): dir = FACE_TOP
        elif(relX<0): dir = FACE_BOT
        elif(relZ>0): dir = FACE_RIGHT
        elif(relZ<0): dir = FACE_LEFT

        thePrimitive = thePrimitive.rotate(0,dir*90,0)
        self.primitives.append( thePrimitive )
        self.relLocs.append( Point3(relX, relY, relZ) )
        self.sExpandables.append(isSideExpandable )

    #must consider relative position to the start
    def expand(self, relX, relZ, x, z, grid, occupancyGrid):

        for i in range(len(self.primitives)) :
            ourX = x + self.relLocs[i].x
            ourY = self.startHeight + self.relLocs[i].y
            ourZ = z + self.relLocs[i].z  

            normX = ourX - relX
            normZ = ourZ - relZ

            if not within2DBounds( normX, normZ, len(occupancyGrid), len(occupancyGrid[0])) :
                return 
                
            if occupancyGrid[ normX ][ normZ ] == False : 
                grid[ ourX ][ ourZ].append( self.primitives[i].translate( ourX, ourY, ourZ ))

                #add random top extra details 
                self.addDecor( ourX, ourZ, self.startHeight+self.relLocs[i].y+1, grid, 0, True)
                
                #add random side extra details - if allowed 
                if self.sExpandables[i] == True : 
                    goX = random.randint(0,1)
                    dir = random.randint(-1,1)

                    direction = 0
                    if goX == 1 : 
                        if dir == 1 : 
                            direction = FACE_LEFT
                        else :
                            direction = FACE_RIGHT
                    else :
                        if dir == 1:
                            direction = FACE_BOT
                        else :
                            direction = FACE_TOP

                    self.addDecor( ourX + (goX*dir), ourZ + ( (1-goX)*dir), self.startHeight, grid, direction, False)

        # Must do at end in case objects stack 
        for i in range(len(self.primitives)):
            ourX = x + self.relLocs[i].x
            ourZ = z + self.relLocs[i].z  
            normX = ourX - relX
            nomrZ = ourZ - relZ
            occupancyGrid[ normX ][ normZ ] = True; 

    def addDecor(self, x, z, startHeight, grid, direction, isTopDecor):
        
        if not within2DBounds(x,z,len(grid),len(grid[0])):
            return 

        if isTopDecor == True :
            grid[x][z].append( self.topExpandables[ random.randint( 0, len(self.topExpandables)-1 ) ].getDecorObject(x,startHeight,z , direction) )
            #translate(x,startHeight,z))F
        else :
            grid[x][z].append( self.sideExpandables[ random.randint( 0, len(self.sideExpandables)-1 ) ].getDecorObject(x,startHeight,z , direction) )
            #translate(x,startHeight,z))



class DecorObject():

    def __init__(self, primitive): 
        self.primitive = primitive
        self.scaleRange = Point(.5, 1.5)
        self.rotRange = Point(0,360)
        self.xzRange = Point(-.5,.5)
        self.yRange = Point(0,0)

    def getDecorObject(self, x, startHeight, z, faceDir):
        s = random.uniform( self.scaleRange.x, self.scaleRange.y)

        xCircPos = random.uniform(0,.5)
        zCircPos = math.sqrt( .25 - xCircPos*xCircPos ) 

        xPos = x - .5 + xCircPos
        zPos = z - .5 + zCircPos 
        yPos = startHeight + .5 

        rot = random.randint( self.rotRange.x, self.rotRange.y )

        #STILL NEEDS SOME WORK (love/hate) 
        '''
        primitiveBuild = self.primitive.scale( 1 )
        primitiveBuild = primitiveBuild.translate( 0, -(1.0/s)-.1, 0)
        primitiveBuild = primitiveBuild.rotate( 0, rot, 0 )
        primitiveBuild = primitiveBuild.translate( xPos, yPos, zPos)#xPos, yPos, zPos
        '''

        primitiveBuild = self.primitive.rotate(0, faceDir*90, 0)        
        primitiveBuild = primitiveBuild.translate( x, startHeight, z )




        return primitiveBuild

    def setScaleRange(self, start, end):
        self.scaleRange = Point(start,end)
        
    def setRotRange(self, start, end):
        self.rotRange = Point(start,end)

    def setPlaceRange(self, xzStart, xzEnd, yStart, yEnd):
        self.xzRange = Point(xzStart, xzEnd)
        self.yRange = Point(yStart, yEnd) 




