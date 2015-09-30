from buildingType import *
from Features import * 
from GenericClasses import *
#from FeatureObjects import * 

import math # for ceil

import random 
#random.seed(100)

# META CONTROL PORTION 

# ============================================================================================
# CREATE PRIMITIVES ==========================================================================
# ============================================================================================

cube = OBJ()
cube.load("models/cube/Cube_type4.obj","models/cube/Cube_type4.mtl")
cube = cube.translate(.1,.1,.1)

kkOn0 = OBJ()
kkOn0.load("models/kitkat/kitkat_textured_emissive_type4.obj","models/kitkat/kitkat_textured_emissive_type4.mtl")    
kkOn0 = kkOn0.translate(.7,0,0)
kkOn0.append(cube)

kkOff0 = OBJ()
kkOff0.load("models/kitkat/kitkat_off.obj","models/kitkat/kitkat_off.mtl")

kkOff0 = kkOff0.translate(.7,0,0)
kkOff0.append(cube) 

but = OBJ()
but.load("models/advanced/buttress_type4.obj","models/advanced/buttress_type4.mtl")

tetra = OBJ()
tetra.load("models/tetrahedron/corner_edge_type4.obj","models/tetrahedron/corner_edge_type4.mtl")
tetra = tetra.rotate(0,315,0)

triPris = OBJ()
triPris.load("models/triangularPrisms/Tri45_type2.obj","models/triangularPrisms/Tri45_type2.mtl")

triPrisOut = triPris.copy()
triPrisOut = triPrisOut.translate(1,0,0)
triPrisOut.append(cube) 

wind = OBJ()
wind.load("models/advanced/window_type4.obj","models/advanced/window_type4.mtl")

vent = OBJ()
vent.load("models/advanced/vent_type4.obj","models/advanced/vent_type4.mtl")
vent = vent.translate(0,0,0)

halfkk = OBJ()
halfkk.load("models/kitkat/kitkat_onebar_type4.obj","models/kitkat/kitkat_onebar_type4.mtl")
halfkk = halfkk.translate(0,.2,0)

halfCyl = OBJ()
halfCyl.load("models/cylinders/cylinder_half_radius_type1.obj","models/cylinders/cylinder_half_radius_type1.mtl")

cyl = OBJ()
cyl.load("models/cylinders/cylinder_full_radius_type2.obj","models/cylinders/cylinder_full_radius_type2.mtl")

sqrPil = OBJ()
sqrPil = cube.scaleAxis(.35,1,.45)

wSlice = OBJ()
#wSlice.load("models/wallSlices/wall_slices_full.obj")
wSlice.load("models/windows/inset_rect.obj","models/windows/inset_rect.mtl")
wSlice = wSlice.rotate(90,90,0)


wSliceHalf = OBJ()
wSliceHalf.load("models/wallSlices/wall_slices_half.obj")

wSliceHalfCut = OBJ()
wSliceHalfCut.load("models/wallSlices/wall_slices_half_straight_cut.obj")

balconWind1 = OBJ()
balconWind1.load("models/windows/bumped_window_type4_2.obj","models/windows/bumped_window_type4_2.mtl")

balconWind1Off = OBJ()
balconWind1Off.load("models/windows/bumped_window_type4_2_off.obj","models/windows/bumped_window_type4_2_off.mtl")


irSide = OBJ()
irSide.load("models/windows/inset_tri_type4.obj","models/windows/inset_tri_type4.mtl")

blockSide = OBJ()
blockSide.load("models/windows/cut_window_type4.obj","models/windows/cut_window_type4.mtl")

blockSideOut = blockSide.translate(1,0,0)

#============================================================
#MULTI PRIMITIVE PRIMITIVES ================================
#============================================================

irSideCornerOut = cube.copy() 
irSideCornerOut.append( irSide.translate(1,0,0))
irSideCornerOut.append( irSide.translate(0,0,1))


windCube = OBJ()
windCube = wind.translate(1,0,0)
windCube.append(cube)

#cube with half kit kat 
cubeHalfkk = OBJ()
cubeHalfkk = halfkk.translate(1,0,0)
cubeHalfkk.append(cube) 

#cube with two half kit kat 
cornerCubekk = cubeHalfkk.copy()
cornerCubekk.append( cubeHalfkk.rotate(0,-90,0) )

windCornerCubekk = cornerCubekk.copy()
windCornerCubekk.append( kkOn0.rotate(0,-90,0))
windCornerCubekk.append( kkOn0.rotate(0,0,0))

windCornerCubekkOut = cube.copy()
windCornerCubekkOut.append( kkOn0.translate(1,0,0))
windCornerCubekkOut.append( kkOn0.translate(0,0,1))
windCornerCubekkOut.append( windCornerCubekk.translate(1,0,1))

# window on two cube faces with two half kit kat 
windCornerHalfkk = cornerCubekk.copy()
windCornerHalfkk.append( kkOn0.rotate(0,-90,0))
windCornerHalfkk.append( kkOn0.rotate(0,0,0))

# cube with halfkk with half kit kat 
windCubeHalfkk = cubeHalfkk.copy()
windCubeHalfkk.append( kkOn0 )

roofHalfkk = cubeHalfkk.copy()
roofHalfkk.append( kkOn0 ) 

# BUMP WINDOW STUFF 
#outBalconWind0 = balconWind0.translate(1,0,0)
#outBalconWind0.append(cube)

outBalconWind1 = balconWind1.translate(1,0,0)
outBalconWind1.append(cube)

outBalconWind1Off = balconWind1Off.translate(1,0,0)
outBalconWind1Off.append(cube) 

bpCorner = cube.copy()
bpCorner.append( outBalconWind1.rotate(0,-90,0))
bpCorner.append( outBalconWind1.rotate(0,0,0))

bpCornerOut = bpCorner.translate(1,0,1)
bpCornerOut.append( outBalconWind1.translate(1,0,0))
bpCornerOut.append( outBalconWind1.translate(0,0,1))

#KK
kkSide = RAND_OBJ( [kkOn0, kkOff0] )
kkSideOut = kkSide.translate(1,0,0)

#BP 
bpSide = RAND_OBJ( [balconWind1, balconWind1Off ])
bpSideOut = RAND_OBJ( [outBalconWind1, outBalconWind1Off] )

'''
bpCornerOut.append( bpSideOut.translate(1,0,0))
bpCornerOut.append( bpSideOut.translate(0,0,1))

bpCorner.append( bpSideOut.rotate(0,-90,0))
bpCorner.append( bpSideOut.rotate(0,0,0))
'''

# ========================================================
# EXPANDABLES FOR ROOF OR SIDE ===========================
# ========================================================

roofSideExpandables = []

roofSideExpandables.append( DecorObject( vent ))

roofSideExpandables.append( DecorObject( halfkk ) )

roofSideExpandables.append( DecorObject( but.translate(0,-.5,0) )) 

roofSideExpandables.append( DecorObject( wSliceHalf.rotate(90,180,0).translate(-.5,0,0) ))

roofSideExpandables.append( DecorObject( wSliceHalfCut.rotate(90,180,0).translate(-.5,0,0) ))


roofTopExpandables = [] 

roofTopExpandables.append( DecorObject( halfCyl ))


# =========================================================
# ROOF FEATURE OBJECTS =====================================
# =========================================================

# FeatureObject is a basic set of primitives, with smaller primitive 
# "expandables" 

roofFeatures = []

#Feature Object 0 
fo0 = FeatureObject()

fo0.setExpandables( roofSideExpandables, roofTopExpandables ) #decoration expansions 

fo0.addFeature( 0, 0, 0, True, cube)
fo0.addFeature( 0, 1, 0, False, cyl)

roofFeatures.append( fo0 )

#Feature Object 1 
fo1 = FeatureObject()
fo1.setExpandables( roofSideExpandables, roofTopExpandables)

fo1.addFeature(0,0,0,True,cube)
roofFeatures.append(fo1)



    
# Places buildings from Expander, choose next Expander based on previous expansion
# This is the iterative expander for the grammar 
class StackPlacementBehavior():
    def __init__(self, expanders):
        self.expanders = expanders

    def placeExpand(self, x, z, limX, limZ, remainingHeight, totalHeight, grid, heights):
        if remainingHeight < 10 : return 

        # Choose random expander from set of expanders possible 
        desiredExpander = random.randint( 0, len(self.expanders)-1 )

        # SHOULD HAVE INPUTS DETERMINE THE PLACING BEHAVIOR HERE BY SETTING REL BOUNDS (ie the x, z, limX, and limZ bounds) 
        # Get last expansion height to inform how much more space we can expand up 
        ourHeight = self.expanders[ desiredExpander ].expand(x, z, limX, limZ, remainingHeight, grid, heights)

        # SHOULD DECIDE NEXT PLACER BASED ON CURRENT HEIGHT RELATIVE TO DESIRED HEIGHT 
        nextPlacer = StackPlacementBehavior( self.expanders[ desiredExpander ].getNextExpansions() )

        nextPlacer.placeExpand( x, z, limX, limZ, remainingHeight - ourHeight, totalHeight, grid, heights )


# EX:  a columnnade entrance should have different columnade like rectExpanders 
# defines a certain building expansion behavior 
class Expander():
    def __init__(self):
        self.minHeight = 5
        self.maxHeight = 30 

    def setMyPlacers(self, rectPlacers):
        self.rectPlacers = rectPlacers
        
    def setNextExpansions(self, nextExpansions):
        self.nextExpansions = nextExpansions 

    def setHeightRange(self, minHeight, maxHeight):
        self.minHeight = minHeight
        self.maxHeight = maxHeight 

    def getNextExpansions(self):
        #desiredIndex = random.randint( 0, len(self.nextExpansions)-1 )
        return self.nextExpansions#[desiredIndex]
    
    def expand(self, x, z, limX, limZ, desiredHeight, grid, heights):
        desiredRectPlacer = random.randint( 0, len(self.rectPlacers)-1 )
        possibleHeight = random.randint( self.minHeight, self.maxHeight )
        if possibleHeight > desiredHeight:
            possibleHeight = desiredHeight 
        lastHeight = self.rectPlacers[ desiredRectPlacer ].addRectBuilding(x,z,possibleHeight,limX,limZ,grid,heights)
        return lastHeight 


# Stores motif info for a rectangular building structure 
class MotifInfo():
    def __init__(self, botMotif, midMotif, topMotif):
        self.botMotif = botMotif
        self.midMotif = midMotif
        self.topMotif = topMotif
    def rotTopMotif(self, yRot):
        for i in range( len(self.topMotif) ):
            self.topMotif[i] = self.topMotif[i].rotate(0,yRot,0)

# Places a rectangular structure from the side and corner motifs that are given to it 

#First adds the sides, corners, then adds the roof then adds roofFeatures 
class RectPlacer():

    # Place the rectangular structure given the position and dimension behavior 
    def addRectBuilding(self,r,c,h,rowLength,colLength,grid,heights):


        startHeight = self.getMinHeight(r,c,rowLength,colLength,heights)


        self.wallMotif(r, c, h, startHeight, False, FACE_TOP, rowLength, DIR_TOP, self.cMotifInfo1, self.sMotifInfo1, grid,heights)

        self.wallMotif(r, c+colLength-1, h, startHeight, False, FACE_BOT, rowLength, DIR_BOT, self.cMotifInfo2, self.sMotifInfo2, grid,heights)
        
        self.wallMotif(r, c+1, h, startHeight, True, FACE_RIGHT, colLength-2, DIR_RIGHT, self.cMotifInfo2, self.sMotifInfo2, grid,heights)

        self.wallMotif(r+rowLength-1, c+1, h, startHeight, True, FACE_LEFT, colLength-2, DIR_LEFT, self.cMotifInfo2, self.sMotifInfo2, grid,heights) 



        lastHeight = self.roof(r, c, h, startHeight, rowLength, colLength, self.roofMotifInfo, grid, heights) 
        return lastHeight

    # Get the min height where we can start adding this rectangle  
    def getMinHeight(self, r, c, rowLength, colLength, heights):
        minHeight = 100000000
        for ci in range(c,c+colLength,colLength-1):
            for ri in range(r,r+rowLength-1):
                #if( heights[ci][ri] < minHeight):
                #    minHeight = heights[ci][ri]
                if( heights[ri][ci] < minHeight):
                    minHeight = heights[ri][ci]

        for ri in range(r,r+rowLength,rowLength-1):
            for ci in range(c,c+colLength-1):
                if( heights[ri][ci] < minHeight):
                    minHeight = heights[ri][ci]
        return minHeight
        

    # TO DO : ALLOW PATTERNS HERE 
    def setSideMotif1(self,botMotif, midMotif, topMotif):
        self.sMotifInfo1 = MotifInfo( botMotif, midMotif, topMotif )
    def setSideMotif2(self,botMotif, midMotif, topMotif):
        self.sMotifInfo2 = MotifInfo( botMotif, midMotif, topMotif )
    def setCornerMotif1(self,botMotif, midMotif, topMotif):
        self.cMotifInfo1 = MotifInfo( botMotif, midMotif, topMotif )
    def setCornerMotif2(self,botMotif, midMotif, topMotif):
        self.cMotifInfo2 = MotifInfo( botMotif, midMotif, topMotif ) 
    def setRoofMotif(self,sideMotif,cornerMotif,roofMotif):
        self.roofMotifInfo = MotifInfo( sideMotif, cornerMotif, roofMotif)

    # TO DO: should be called at the end to avoid adding roof features that are covered by other
    # buildings placed on the roof
    def addRoofFeatures(self, x, z, startHeight, lenX, lenZ, grid):
        #create occupancy grid 
        #MAKE THIS COMPLETE 
        occupancyGrid = [[False for l in range( lenZ )] for w in range( lenX )]
        
        #main features objects (should be passed in as a parameter)


        featureObjectPlacer = FeatureObjectPlacer()

        # FEATURES 
        ourFeatures = roofFeatures 
        


        for feature in ourFeatures : 

            durX = random.randint(5,30)#lenX+1) #1 + doX * random.randint( 2, 8)
            durZ = random.randint(5,30)#lenZ+1) #1 + (doX-1) * random.randint( 2, 8)

            repX = random.randint( 2, 4 ) 
            repZ = random.randint( 2, 4 ) 

            featureObjectPlacer.setPlacingBehavior(startHeight, durX, durZ, repX, repZ, feature) 

            #featureObjectPlacer.applyFeature( x, z, random.randint(0,int(lenX/2.0)), random.randint(0,int(lenZ/2.0)), grid, occupancyGrid )

            featureObjectPlacer.applyFeature( x, z, 0, 0, 5, grid, occupancyGrid )

                
                

    # Fill xz roof 
    def roof(self, r, c, h, startHeight, rowLength, colLength, motifInfo, grid, heights):
        sideObj = motifInfo.botMotif
        cornerObj = motifInfo.midMotif
        roofObj = motifInfo.topMotif 

        for ri in range( r, r+rowLength):
            for ci in range( c, c+colLength):
                if h+startHeight < heights[ri][ci] : continue 

                val = 0
                if ri == r : val += 2
                elif ri == r + rowLength - 1 : val += 4

                if ci == c : val += 1
                elif ci == c + colLength - 1 : val += 3


                #Corner 
                if val > 4 or val == 3 and ri == r :
                    if val == 5 : 
                        if ri == r : 
                            val = 3
                        else : 
                            val = 1 
                    else : 
                        if val == 3 : 
                            val = 2
                        else :
                            val = 4
                
                        
                    grid[ri][ci].append( cornerObj.rotate(0,90*val,0).translate(ri,h+startHeight,ci))

                #Side
                elif val > 0 :  
                    grid[ri][ci].append( sideObj.rotate(0,90*val,0).translate(ri, h+startHeight, ci))
                    
                else : 
                    grid[ri][ci].append( roofObj.translate(ri,h+startHeight,ci) )

                heights[ri][ci] = h + startHeight
         
        #grid[r][c].append( cube.scaleAxis( 1, 1, 1).translate( r - .2 + (rowLength/2) , h+startHeight, c+.9 ) )
        #grid[r][c].append( cube.scaleAxis( rowLength-2, 1, colLength-1 ).translate( r - 1 + ceil((rowLength-1)/2), h+startHeight, c - 1 + ceil((colLength-1)/2) ))

                

        #self.addRoofFeatures( r + 1, c + 1, heights[ri][ci], rowLength-2, colLength-2, grid)

        return heights[ri][ci]; 
        

    # Fill a up y direction
    def sideMotif(self, stack, r, c, desiredHeight, startHeight, faceDir, motifInfo, heights):


        topMotif = motifInfo.topMotif
        midMotif = motifInfo.midMotif
        botMotif = motifInfo.botMotif

        curHeight = startHeight
        possibleHeight = desiredHeight  #should factor in max height here 

        # avoid having objects within other objects 

        if startHeight+desiredHeight <= heights[r][c] : 
            curHeight = 0
            possibleHeight = desiredHeight * 100 


        #rotate all objects to proper direction 
        faceRotation = faceDir * 90 

        topMotifC = []
        midMotifC = []
        botMotifC = []
        for i in range( len(topMotif) ):
            topMotifC.append(topMotif[i].rotate(0,faceRotation,0))
        for i in range( len(midMotif) ):
            #random.seed( len(stack) * r * c * desiredHeight * startHeight)
            midMotifC.append(midMotif[i].rotate(0,faceRotation,0))
        for i in range( len(botMotif) ):
            botMotifC.append(botMotif[i].rotate(0,faceRotation,0))

        numMiddle = desiredHeight - len(botMotif) - len(topMotif)
        
        if possibleHeight < len(topMotif) + len(botMotif) : 

            index = 0 
            while index < possibleHeight : 
                if index % 2 == 0: 
                    stack.insert(0, botMotifC[ index/2 ].translate(r, curHeight, c) )
                    curHeight += 1 
                else : 
                    stack.append( topMotifC[ int(math.ceil(index/2))].translate(r, curHeight, c) )
                    curHeight += 1
                index += 1
        else:
            # expand out motif from submotifs 

            for i in range( len(botMotif ) ):
                stack.append( botMotifC[i].translate(r, curHeight, c) )
                curHeight += 1
            for i in range( numMiddle ):

                #random.seed( r * c * desiredHeight * startHeight )
                stack.append( midMotifC[ i % len(midMotif)  ].translate(r,curHeight,c))
                curHeight += 1
            for i in range( len(topMotif) ):
                stack.append( topMotifC[i].translate(r, curHeight, c) )
                curHeight += 1

        heights[r][c] = curHeight;

        #TO DO : THIS SHOULD SET THE APPROPRIATE HEIGHT IN HEIGHT ARRAY 

    #goRowDir is boolean to place motifs in column direction
    #motifDir is a integer that determines rotation of wall motifs     

    # (r,c) = position (h) = height, motifDir since goRowDir not enough info for direction
    def wallMotif(self, r, c, h, startHeight, goRowDir, motifDir, wallLength, moveDir, cMotifInfo, sMotifInfo, grid, heights):
        #Set expansion direction 
        rowDir = 0; 
        colDir = 0; 
        if goRowDir : colDir = moveDir.x
        else : rowDir = moveDir.y 

        

        # Add in start block motif 

        self.sideMotif( grid[r][c], r, c, h, startHeight, motifDir, cMotifInfo, heights)

        # TO DO NEED DIFFERENT CONDITIONAL HERE BASED ON HEIGHT ARRAY , SHOULD PLACE ALONG THE ENTIRE LENGTH WHERE POSSIBLE, IE SHOULD PLACE THE ENTIRE RECTANGLE OUTLINE REGARDLESS OF OBSTRUCTIONS


        rowPos = 0
        colPos = 0 
        for i in range( 1, wallLength - 1):
            rowPos = r + i*rowDir
            colPos = c + i*colDir
            self.sideMotif( grid[rowPos][colPos], rowPos, colPos, h, startHeight, motifDir, sMotifInfo, heights)
        
        # Add in final block motif
        ''' messes up on c == 0 if this code is active 
        if rowPos == 0 or colPos == 0:
            rowPos = r 
            colPos = c

        '''
        if wallLength == 1 : return 
        
        if rowPos == 0 and colPos == 0:
            rowPos = r
            colPos = c


        #cMotifInfo.rotTopMotif(180)

        self.sideMotif( grid[rowPos + rowDir][colPos + colDir], rowPos+rowDir,colPos+colDir, h, startHeight,  motifDir, cMotifInfo, heights)
        #self.sideMotif( grid[1][0], 1, 0, h, startHeight, motifDir, cMotifInfo, heights) 

        #cMotifInfo.rotTopMotif(-180) 

#============================================================================================================
# ACTUAL BUILDING CLASS : 
#============================================================================================================
class TestBuilding(Building):


    def __init__(self, length, width, max_height, seed):
        Building.__init__(self, length, width, max_height, seed)
        
        # A cube has all floorplan things set to true
        self.floorplan = [[True for l in range(length)] for w in range(width)]

        '''
        # The places where stacks have terminatedf
        self.terminated = [[False for l in range(length)] for w in range(width)]
        
        # Axioms for a cube are just a cube
        self.axioms = [cube.copy()]
        
        self.nonterminals = [cube.copy()] # Fix copy part=fix OBJ constr

        self.terminals = [cube.copy()] 
        
        self.rules = { type(cube_obj) : [self.terminate, self.repeatUp ] }
        '''


        # START OF THE RECT PLACERS TYPES 
        # JUMP POINT @ !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

        ''' Short description: 
        We set the primitives that a rectPlacer will use to create its corners and wall sides.  These 
        rect placers are used by expanders.  
        '''

        # BP = BUMPED : cube with rectangular window popping out of its side 

        #Basic middle and bottom of BP Window 
        bpMidBot0 = RectPlacer()
        
        middleMotif0 = [ bpSide, blockSide ]
        middleMotif1 = [ bpSide ] 
        bpMidBot0.setSideMotif1( [ bpSide ] , middleMotif0, [bpSideOut ] )
        bpMidBot0.setSideMotif2( [ bpSide], middleMotif1, [bpSideOut ] )

        bpMidBot0.setCornerMotif1( [ bpCorner ] , [ bpCorner ], [ bpCornerOut ] ) 
        bpMidBot0.setCornerMotif2( [ bpCorner ] , [ bpCorner ], [ bpCornerOut ] ) 
        
        bpMidBot0.setRoofMotif( triPris, bpCorner, cube ) 


        #Basic middle and bottom of BP Window, corner OUT  
        bpMidBot1 = RectPlacer()
        
        middleMotif0 = [ bpSide, cubeHalfkk.translate(-1,0,0)  ]
        middleMotif1 = [ bpSide, cubeHalfkk.translate(-1,0,0) ] 
        bpMidBot1.setSideMotif1( [ bpSide ] , middleMotif0, [bpSideOut ] )
        bpMidBot1.setSideMotif2( [ bpSide], middleMotif1, [bpSideOut ] )

        bpMidBot1.setCornerMotif1( [ bpCorner ] , [ bpCornerOut ], [ bpCornerOut ] ) 
        bpMidBot1.setCornerMotif2( [ bpCorner ] , [ bpCornerOut ], [ bpCornerOut ] ) 
        
        bpMidBot1.setRoofMotif( triPris, tetra, cube ) 

        #Basic bottom w/ BP Window
        bpBot0 = RectPlacer()
        
        middleMotif0 = [ blockSide, bpSide ]
        middleMotif1 = [ blockSide, bpSide ] 
        bpBot0.setSideMotif1( [ sqrPil, sqrPil ] , middleMotif0, [bpSideOut ] )
        bpBot0.setSideMotif2( [ sqrPil, sqrPil ], middleMotif1, [bpSideOut ] )

        bpBot0.setCornerMotif1( [ bpCorner ] , [ bpCorner ], [ bpCornerOut ] ) 
        bpBot0.setCornerMotif2( [ bpCorner ] , [ bpCorner ], [ bpCornerOut ] ) 
        
        bpBot0.setRoofMotif( triPris, bpCorner, cube ) 


        #BP Window middle with Triangular roofing 
        bpTop0 = RectPlacer()
        
        middleMotif0 = [ blockSide, bpSideOut, triPrisOut ]
        middleMotif1 = [ blockSide, bpSideOut, triPrisOut ] 
        bpTop0.setSideMotif1( [bpSide] , middleMotif0, [bpSideOut ] )
        bpTop0.setSideMotif2( [bpSide] , middleMotif0, [bpSideOut ] )


        bpTop0.setCornerMotif1( [ bpCorner ] , middleMotif0, [ triPrisOut ] ) 
        bpTop0.setCornerMotif2( [ bpCorner ] , middleMotif0, [ triPrisOut ] ) 
        
        bpTop0.setRoofMotif( triPris, bpCorner, cube ) 


        # BASIC Bottom Type 

        botGeneric = RectPlacer()
        
        middleMotif0 = [ irSide, blockSide, vent,irSide ]#, bpSideOut, triPrisOut ]
        middleMotif1 = [ irSide, blockSide, irSide ]#, bpSideOut, triPrisOut ] 
        botGeneric.setSideMotif1( [ sqrPil, sqrPil, sqrPil, blockSideOut] , middleMotif0, [ irSideCornerOut, irSideCornerOut ] )
        botGeneric.setSideMotif2( [ sqrPil, sqrPil, sqrPil, blockSideOut] , middleMotif0, [ irSideCornerOut, irSideCornerOut ] )


        botGeneric.setCornerMotif1( [ cube  ] , [irSide], [ irSide ] ) 
        botGeneric.setCornerMotif2( [ cube  ] , [irSide], [ irSide ] ) 
        
        botGeneric.setRoofMotif( bpCornerOut, blockSide, cube ) 


        # FLAT TYPE = cube with rectangular cut into it symbolizing a window 

        # FLAT TYPE BLOCK SIDE MIDDLE 
        flatMidGeneric0 = RectPlacer()
        
        middleMotif0 = [ bpSide, blockSide ]#, bpSideOut, triPrisOut ]
        middleMotif1 = [ bpSide, blockSide ]#, bpSideOut, triPrisOut ] 
        flatMidGeneric0.setSideMotif1( [ cube] , middleMotif0, [ bpSideOut ])
        flatMidGeneric0.setSideMotif2( [ cube] , middleMotif0, [ bpSideOut  ] )


        flatMidGeneric0.setCornerMotif1( [ cube, cube, cube ] , middleMotif0, [ cube ] ) 
        flatMidGeneric0.setCornerMotif2( [ cube, cube, cube ] , middleMotif0, [ cube ] ) 
        
        flatMidGeneric0.setRoofMotif( bpSideOut, bpCorner, cube ) 


        # FLAT TYPE BLOCK SIDE MIDDLE 
        flatMidGeneric1 = RectPlacer()
        
        middleMotif0 = [ bpSide, blockSide  ]#, bpSideOut, triPrisOut ]
        middleMotif1 = [ bpSide, blockSide ]#, bpSideOut, triPrisOut ] 
        flatMidGeneric1.setSideMotif1( [ blockSideOut] , middleMotif0, [ cube ])
        flatMidGeneric1.setSideMotif2( [ blockSideOut] , middleMotif0, [ cube  ] )


        flatMidGeneric1.setCornerMotif1( [ cube, cube, cube ] ,[cube], [ cube ] ) 
        flatMidGeneric1.setCornerMotif2( [ cube, cube, cube ] ,[cube], [cube])
        
        flatMidGeneric1.setRoofMotif( bpSideOut, bpCorner, cube ) 


        # FLAT TYPE TOP AREA 

        flatTopGeneric0 = RectPlacer()
        
        middleMotif0 = [ cube, blockSide.translate(1,0,0) ]#, bpSideOut, triPrisOut ]
        middleMotif1 = [ cube, blockSide.translate(1,0,0) ]#, bpSideOut, triPrisOut ] 
        flatTopGeneric0.setSideMotif1( [ cube] , middleMotif0, [ blockSide.translate(1,0,0), blockSide.translate(1,0,0) ])
        flatTopGeneric0.setSideMotif2( [ cube] , middleMotif0, [ blockSideOut, triPris.translate(1,0,0), blockSide  ] )


        flatTopGeneric0.setCornerMotif1( [ cube, cube, cube ] ,[cube], [ cube ] ) 
        flatTopGeneric0.setCornerMotif2( [ cube, cube, cube ] ,[cube], [cube])
        
        flatTopGeneric0.setRoofMotif( triPris, bpCorner, cube ) 


        # Industrial Bottom Generic 
        # NICE LOOKS INDUSTRIAL LIKE 
        grateWindTop = RectPlacer()

        #in this case we would actually want different motifs for sideMotifs, 
        #usually this is not the case however 
        wSliceIn = wSlice.translate(-.2,0,0)
        middleMotif0 = [ wSliceIn, windCube, wSliceIn ] 
        middleMotif1 = [ wSliceIn ] 
                

        grateWindTop.setSideMotif1( [ wSliceIn ], middleMotif0 ,[ wSliceIn, wSliceIn, windCube ] )
        grateWindTop.setSideMotif2( [ wSliceIn ], middleMotif1 ,[ wSliceIn, wSliceIn, windCube] )

        grateWindTop.setCornerMotif1( [cube], [cube], [cube] )
        grateWindTop.setCornerMotif2(  [cube], [cube], [cube] )

        grateWindTop.setRoofMotif( triPris, tetra, cube ) 

        # KK = kit kat window types 

        # BUTTRESS KK FLAT SIDE 
        kkFlatBut = RectPlacer()

        #in this case we would actually want different motifs for sideMotifs, 
        #usually this is not the case however 
        middleMotif0 = [ cube.translate(1,0,0),cube.scaleAxis(.35,1,.45).translate(1.3,0,0),cube.scaleAxis(.37,1,.4).translate(1.3,0,0),but.translate(1,0,0), kkSide]
        middleMotif1 = [ kkSide ] 
                

        kkFlatBut.setSideMotif1( [ kkSide ], middleMotif0 ,[kkSide ] )
        kkFlatBut.setSideMotif2( [ kkSide, kkSide], middleMotif1 ,[kkSide, kkSide] )

        kkFlatBut.setCornerMotif1( [kkSide], [kkSide], [kkSide] )
        kkFlatBut.setCornerMotif2( [kkSide], [kkSide], [kkSide] )

        kkFlatBut.setRoofMotif( triPris, tetra, cube ) 
        #'''

        # COLUMNS KK OUT ROOF KK 
        kkFlatCol = RectPlacer()

        kkFlatCol.setSideMotif1( [ halfCyl, halfCyl, halfCyl, kkSideOut, kkSideOut, triPrisOut ],[ kkSide, cubeHalfkk],[ triPrisOut.rotate(0,0,180), kkSideOut, kkSideOut ] )
        kkFlatCol.setSideMotif2( [ halfCyl, halfCyl, halfCyl, kkSideOut, kkSideOut,triPrisOut ],[ kkSide, cubeHalfkk],[ triPrisOut.rotate(0,0,180),kkSideOut, kkSideOut ] )

        kkFlatCol.setCornerMotif1( [cube, cube, cube], [kkSide, cubeHalfkk], [windCornerCubekkOut, windCornerCubekkOut] )
        kkFlatCol.setCornerMotif2( [cube, cube, cube], [kkSide, cubeHalfkk], [windCornerCubekkOut, windCornerCubekkOut] )
        kkFlatCol.setRoofMotif( triPrisOut, tetra, cube ) 



        #'''
        # KK OUT ON ROOF ( TRI PRIS OUT ) 
        kkOutRoof = RectPlacer()

        kkOutRoof.setSideMotif1( [ kkSide ],[ kkSide, cubeHalfkk],[ triPrisOut.rotate(0,0,180), kkSideOut, kkSideOut ] )
        kkOutRoof.setSideMotif2( [ kkSide ],[ kkSide, cubeHalfkk],[ triPrisOut.rotate(0,0,180),kkSideOut, kkSideOut ] )

        kkOutRoof.setCornerMotif1( [kkSide], [kkSide, cubeHalfkk], [windCornerCubekkOut, windCornerCubekkOut] )
        kkOutRoof.setCornerMotif2( [kkSide], [kkSide, cubeHalfkk], [windCornerCubekkOut, windCornerCubekkOut] )

        kkOutRoof.setRoofMotif( triPrisOut, tetra, cube ) 
        #'''
        
        #'''
        # HALF KK WITH FULL KK (FLAT) 
        kkFlatHalf = RectPlacer()

        kkFlatHalf.setSideMotif1( [ kkSide ],[ kkSide, cubeHalfkk],[kkSide ] )
        kkFlatHalf.setSideMotif2( [ kkSide ],[ kkSide, cubeHalfkk],[kkSide ] )

        kkFlatHalf.setCornerMotif1( [kkSide], [kkSide, cubeHalfkk], [kkSide] )
        kkFlatHalf.setCornerMotif2( [kkSide], [kkSide, cubeHalfkk], [kkSide] )


        kkFlatHalf.setRoofMotif( cubeHalfkk, cornerCubekk, cube)
        #'''


        #Generic and flat kk 
        kkFlatGeneric = RectPlacer()

        kkFlatGeneric.setSideMotif1( [ kkSide, kkSide],[windCube, kkSide],[kkSide, kkSide] )
        kkFlatGeneric.setSideMotif2( [ kkSide, kkSide],[windCube, kkSide],[kkSide, kkSide] )

        kkFlatGeneric.setCornerMotif1( [kkSide], [kkSide], [kkSide] )
        kkFlatGeneric.setCornerMotif2( [kkSide], [kkSide], [kkSide] )

        kkFlatGeneric.setRoofMotif( triPris, tetra, cube ) 

        # END RECT PLACER DECLARATIONS ===================================================

        # JUMP TO POINT  @ !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

        '''Short Description: 
        Expanders take in several rect placers that they randomly choose between.  They also specify
        other expanders that will take their place after it has expanded.  Expaners are in essence 
        the grammar portion, some expaners are "axioms" as they grow out bottom-like rectangular
        buildings, while others are more mid/top level of building 
        '''


        # EXPANDER DECLARATIONS ==========================================================
        #topkkExpader = Expander()
        #midHalfFlatkkExpander = Expander()
        midkkExpander = Expander()
        groundColumnkkExpander = Expander()

        groundFlatExpander = Expander()
        midFlatExpander = Expander()
        topFlatExpander = Expander() 

        groundBPExpander = Expander()
        midBPExpander = Expander()
        topBPExpander = Expander()


        # Mid KK Expander 
        midkkExpander.setMyPlacers( [ kkFlatGeneric, kkFlatHalf, kkFlatBut, kkOutRoof ] )
        midkkExpander.setNextExpansions( [midkkExpander] )
        midkkExpander.setHeightRange( 10, 15 ) 

        # Ground Column KK Expander
        groundColumnkkExpander.setMyPlacers( [ kkFlatCol, grateWindTop, botGeneric ] )
        groundColumnkkExpander.setNextExpansions( [ groundColumnkkExpander, midkkExpander, midkkExpander ] )
        groundColumnkkExpander.setHeightRange( 4, 5 )

        # Ground Flat Expanders 
        groundFlatExpander.setMyPlacers( [ botGeneric, grateWindTop ] )
        groundFlatExpander.setNextExpansions( [ midFlatExpander, groundFlatExpander] )
        groundFlatExpander.setHeightRange( 4, 9)

        #Mid Flat Expanders 
        midFlatExpander.setMyPlacers( [ flatMidGeneric0, flatMidGeneric1  ])
        midFlatExpander.setNextExpansions( [ midFlatExpander, midFlatExpander, topFlatExpander ])
        midFlatExpander.setHeightRange( 8, 13 )

        #Top Flat Expanders 
        topFlatExpander.setMyPlacers( [ flatMidGeneric0, flatTopGeneric0 ])
        topFlatExpander.setNextExpansions( [ midFlatExpander, topFlatExpander] )
        topFlatExpander.setHeightRange( 15, 23 ) 
        
        # Ground BP Expanders 
        groundBPExpander.setMyPlacers( [ bpBot0, bpMidBot0 ] )
        groundBPExpander.setNextExpansions( [ groundBPExpander, midBPExpander ] )
        groundBPExpander.setHeightRange( 4, 10 )

        # Mid BP Expanders
        midBPExpander.setMyPlacers( [ bpMidBot0, bpMidBot1 ] )
        midBPExpander.setNextExpansions( [ midBPExpander, topBPExpander ] )
        midBPExpander.setHeightRange( 12, 23 )

        # Top BP Expanders
        topBPExpander.setMyPlacers( [ bpTop0, bpMidBot1 ] )
        topBPExpander.setNextExpansions( [ topBPExpander, midBPExpander, topBPExpander ] )
        topBPExpander.setHeightRange( 15, 23 ) 

        # END EXPANDER DECLARATIONS 
        

        #Create placers =======================================
        '''
        A placer takes in axiom expanders and iteratively expaners out a building based on the expanders
        that each expander expands to 
        In the future hope to have different placers that place the buildings in different ways (rather 
        than being completly random) 
        '''

        #CONSOLIDATE 
        self.kkBuildingPlacer = StackPlacementBehavior( [ groundColumnkkExpander, groundBPExpander, groundFlatExpander ] )
        # FOR INDIVIDUAL BUILDING TYPE TESTING 
        #self.kkBuildingPlacer = StackPlacementBehavior( [ groundBPExpander ] )
        #self.kkBuildingPlacer = StackPlacementBehavior( [ groundFlatExpander ] )
        #self.kkBuildingPlacer = StackPlacementBehavior( [groundColumnkkExpander ] )


        
        #EXPAND: begin expansion process 
        self.expand()
        

    def expand(self):

        #ROW == X
        numIterations = 3 # magic number, seems to work for sizes (10x10x10 to 40xNx40)
        #numIterations = 1

        minWidth =  ceil ( max( len(self.grid), len(self.grid[0]) ) / 2.0 )

        '''
        for r in range( len(self.grid) ):
            for c in range( len(self.grid[0])):
                self.grid[r][c].append(cube.translate(r,0,c))
        '''

        #At least on iteration should largely cover the bottom
        self.kkBuildingPlacer.placeExpand( 1, 1, len(self.grid)-3, len(self.grid[0])-3, self.MAX_HEIGHT, 0, self.grid, self.heights)
        

        for run in range( 0, numIterations-1 ): 
            randR = random.randint(0, len(self.grid)-minWidth)
            randC = random.randint(0, len(self.grid[0])-minWidth)
            
            randRL = random.randint(minWidth, len(self.grid)-randR)
            randCL = random.randint(minWidth, len(self.grid[0])-randC)

            self.kkBuildingPlacer.placeExpand( randR, randC, randRL, randCL, self.MAX_HEIGHT, 0, self.grid, self.heights)

            print( "Finished Iteration: " + str( run ) + " out of: " + str(numIterations) )
            #self.rectExpansions.addRectBuilding(randR, randC, randH, randRL, randCL, self.grid, self.heights)        

        #self.grid[0][0].append( cube.scaleAxis(100,1,1000))

    '''
    def repeatUp(self, stack, r=None, c=None):
        stack.append( stack[-1].translate(0, 1, 0) )

    def terminate(self, stack, r, c):
        self.terminated[r][c] = True
        #stack.append( self.terminals[0].translate(r, len(stack), c) )

    # class specific helper method 
    def isBuildSpot(self,r,c):
        return self.floorplan[r][c] and not self.terminated[r][c] 

    def isOccupied(self, r, c, curHeight, grid):
        #Bounds check 
        if r < 0 or r >= len(grid) or c < 0 or c >= len(grid[0]) :
            return True
        #IsOccupied check 
        #print ( "r: " + str(r) + " c: " + str(c) )
        return self.terminated[r][c] and self.floorplan[r][c] # and self.heights[r][c] >= curHeight
   '''
