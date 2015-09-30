from buildingType import *
import random

# labels for the array indices
TILE = 0
TRI = 1
GARDEN = 2
EMPTY = 3
ROOF = 4
LIT_WINDOW = 5
UNLIT_WINDOW = 6
BLUE_WINDOW = 7
KITKAT = 8


TERMINATE = 0
REPEAT = 1
MAKE_GARDEN = 2


class EliBuilding(Building):

    def __init__(self, length, width, max_height, seed):
        Building.__init__(self, length, width, max_height, seed)
        
        # Primitives needed for the building
        tri_obj = OBJ(TRI) 
        tri_obj.load("models/triangularPrisms/Tri45.obj")        
        tri_obj.objType = TRI


        garden_obj = OBJ(GARDEN)
        garden_obj.load("models/cube/Cube_type3.obj", "models/cube/Cube_type3.mtl")
        garden_obj.objType = GARDEN

        empty_obj = OBJ(EMPTY)
        empty_obj.objType = EMPTY
        
        cube_obj = OBJ(TILE)
        cube_obj.load("models/cube/Cube_type3.obj", "models/cube/Cube_type3.mtl")
        cube_obj.objType = TILE

        litWindow_obj = OBJ(LIT_WINDOW)
        litWindow_obj.load("models/advanced/window_type3_2.obj", "models/advanced/window_type3_2.mtl")
        litWindow_obj.objType = LIT_WINDOW

        unlitWindow_obj = OBJ(UNLIT_WINDOW)
        unlitWindow_obj.load("models/advanced/window_type3.obj","models/advanced/window_type3.mtl")
        unlitWindow_obj.objType = UNLIT_WINDOW

        blueWindow_obj = OBJ(BLUE_WINDOW)
        blueWindow_obj.load("models/advanced/window_type3_3.obj","models/advanced/window_type3_3.mtl")
        blueWindow_obj.objType = BLUE_WINDOW

        #kitkat_obj = OBJ(KITKAT)
        #kitkat_obj.load("models/kitkat/kitkat_type4.obj","models/kitkat/kitkat_type4.mtl")
#        kitkat_obj.load("models/kitkat/kitkat_emissive_type3.obj","models/kitkat/kitkat_emissive_type3.mtl")
        kitkat_obj.objType = KITKAT

 #       kitkat_obj = OBJ(KITKAT)
  #      kitkat_obj.load("models/wallSlices/wall_slices_half_straight_cut.obj")
   #     kitkat_obj.objType = KITKAT


        # A cube has all floorplan things set to true
        self.floorplan = [[True for l in range(length)] for w in range(width)]
        
        # The places where stacks have terminated
        self.terminated = [[False for l in range(length)] for w in range(width)]
        
        # Axioms are a cube and triangular prism
        self.axioms = [cube_obj.copy(), tri_obj.copy(), garden_obj.copy(), empty_obj.copy()]
        
        self.nonterminals = [cube_obj.copy(), tri_obj.copy(), garden_obj.copy(), empty_obj.copy()] # Fix copy part=fix OBJ constr

        self.terminals = [cube_obj.copy(), tri_obj.copy(), garden_obj.copy(), empty_obj.copy(), tri_obj.copy(), litWindow_obj.copy(), unlitWindow_obj.copy(), blueWindow_obj.copy(), kitkat_obj.copy()] 
        
        self.rules = { TILE          : [self.terminate, self.repeatUp, self.makeGarden],
                       TRI           : [self.terminate, self.terminate, self.terminate],
                       GARDEN        : [self.terminate, self.repeatUp, self.makeGarden],
                       EMPTY         : [self.terminate, self.repeatUp, self.makeGarden],
                       ROOF         : [self.terminate, self.repeatUp, self.makeGarden],
                       LIT_WINDOW    : [self.terminate, self.repeatUp, self.makeGarden],
                       UNLIT_WINDOW  : [self.terminate, self.repeatUp, self.makeGarden],
                       BLUE_WINDOW  :  [self.terminate, self.repeatUp, self.makeGarden],
                       KITKAT        : [self.terminate, self.repeatUp, self.makeGarden]
        } 
    
        # creates square grid, TODO reset floorplan
        self.maxSide = min(length, width)-1
        
        self.minSide = 0

        self.expand()
        
    def expand(self):
        # While not everything has been terminated
        startGarden = self.MAX_HEIGHT / 4
        period = self.MAX_HEIGHT / 8

        while not all([done for sublist in self.terminated for done in sublist]):
            

            # Iterate over the stacks of things in grid
            for r in range( len(self.grid) ):
                for c in range( len(self.grid[0]) ):
                    # Only do it if we are allowed to build here
                    if self.floorplan[r][c] and not self.terminated[r][c]:

                        # The current building stack in the grid
                        stack = self.grid[r][c]
                        
                        # Here we have to decide what function to take
                        func_i = None # function index
                        
                        # len(stack) = height of stack
                        # - 1 in order not to have terminals go over max height
                        if not stack:
                            self.repeatUp(stack, r, c)
                            #stack.append( self.axioms[CUBE].translate(r,0,c) )
                            continue
                        elif len(stack) >= self.MAX_HEIGHT: # or self.maxSide <= 0:
                            func_i = TERMINATE
                        elif (len(stack) >= startGarden and (len(stack) % period == 0)):
                            func_i = MAKE_GARDEN
                        else:
                            func_i = REPEAT

                        f = self.rules[ stack[-1].objType ][func_i]
                        f(stack, r, c)

                       
    def repeatUp(self, stack, r, c):
        if not stack: #absolute translations

#            if  (r == self.minSide):
 #               stack.append( self.terminals[EMPTY].translate(r, 0, c) )
  #          elif(r == self.maxSide):
   #             stack.append( self.terminals[EMPTY].translate(r, 0, c) )
    #        elif(c == self.minSide):
     #           stack.append( self.terminals[EMPTY].translate(r, 0, c) )
      #      elif(c == self.maxSide):
       #         stack.append( self.terminals[EMPTY].translate(r, 0, c) )
            # else:

            stack.append( self.terminals[TILE].translate(r, 0, c) )                

        elif (len(stack) < self.MAX_HEIGHT/4): #don't put windows, put kitkats on outside

            if  (r == self.minSide and (not c%(len(self.grid)/4) or not (c%(len(self.grid)/4)-1))):
#            if  (r == self.minSide):
                stack.append( self.terminals[KITKAT].rotate(-0,180,0).translate(r, len(stack), c) )
            elif(r == self.maxSide and (not c%(len(self.grid)/4) or not (c%(len(self.grid)/4)-1))):
                stack.append( self.terminals[KITKAT].rotate(-0,0,0).translate(r, len(stack), c) )
            elif(c == self.minSide and (not r%(len(self.grid)/4) or not (r%(len(self.grid)/4)-1))):
                stack.append( self.terminals[KITKAT].rotate(-0,90,0).translate(r, len(stack), c) )
            elif(c == self.maxSide and (not r%(len(self.grid)/4) or not (r%(len(self.grid)/4)-1))) :
                stack.append( self.terminals[KITKAT].rotate(-0,-90,0).translate(r, len(stack), c) )
            else:
                stack.append( stack[-1].translate(0,1,0))


        else: #put windows.
            # randomly lit or unlit
            rnd   = random.randint(0,20)
            if rnd < 12:
                WINDOW = UNLIT_WINDOW
            else:
                WINDOW = (LIT_WINDOW, BLUE_WINDOW)[rnd < 17]
            
            if  (r == self.minSide):
                stack.append( self.terminals[EMPTY].translate(0, 1, 0) )
            elif(r == self.maxSide):
                stack.append( self.terminals[EMPTY].translate(0, 1, 0) )
            elif(c == self.minSide):
                stack.append( self.terminals[EMPTY].translate(0, 1, 0) )
            elif(c == self.maxSide):
                stack.append( self.terminals[EMPTY].translate(0, 1, 0) )


            elif(r == self.minSide+1): #180 for the third rotation argument?
                stack.append( self.terminals[WINDOW].rotate(0,180,180).translate(r, len(stack), c) )
            elif(r == self.maxSide-1):
                stack.append( self.terminals[WINDOW].rotate(0,0,180).translate(r, len(stack), c) )
            elif(c == self.minSide+1):
                stack.append( self.terminals[WINDOW].rotate(0,90,0).translate(r, len(stack), c -1) )
            elif(c == self.maxSide-1):
                stack.append( self.terminals[WINDOW].rotate(0,-90,0).translate(r, len(stack), c+1) )


            else:
#                stack.append( stack[-1].translate(0, 1, 0) )                
                stack.append( self.terminals[EMPTY].translate(0,1,0))


    def makeGarden(self, stack, r, c):    
        if  (r == self.minSide):
            stack.append( self.terminals[GARDEN].translate(r, len(stack), c) )
        elif(r == self.maxSide):
            stack.append( self.terminals[GARDEN].translate(r, len(stack), c) )
        elif(c == self.minSide):
            stack.append( self.terminals[GARDEN].translate(r, len(stack), c) )
        elif(c == self.maxSide):
            stack.append( self.terminals[GARDEN].translate(r, len(stack), c) )
        else:
            stack.append( self.terminals[TILE].translate(r, len(stack), c) ) # TILE TWO?

    def terminate(self, stack, r, c):
        self.makeGarden(stack, r, c)
        self.terminated[r][c] = True
        if (r==5 and c==5):

            stack.append(self.terminals[ROOF].translate(len(self.grid)/2,len(stack), len(self.grid[0])/2))
        
