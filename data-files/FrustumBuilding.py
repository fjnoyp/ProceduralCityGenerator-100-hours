from buildingType import *
from random import *
# labels for primitives
CUBE = 0
TRI = 1
EMPTY = 2
CYL = 3
# labels for function application
TERMINATE = 0
RING = 1
BODY = 2

class FrustumBuilding(Building):

    def __init__(self, length, width, max_height, seed):
        Building.__init__(self, length, width, max_height, seed)
        
        # Primitives needed for the building
        tri_obj = OBJ("models/triangularPrisms/Tri45_type2_2.obj") 
        tri_obj.load("models/triangularPrisms/Tri45_type2_2.obj",
                     "models/triangularPrisms/Tri45_type2_2.mtl")        
        
        cube_obj = OBJ("models/cube/cube_type2.obj")
        cube_obj.load("models/cube/cube_type2.obj",
                     "models/cube/cube_type2.mtl")
        
        cyl_obj = OBJ("models/cylinders/cylinder_full_radius_type2.obj")
        cyl_obj.load("models/cylinders/cylinder_full_radius_type2.obj",
                     "models/cylinders/cylinder_full_radius_type2.mtl")

        # A cube has all floorplan things set to true
        self.floorplan = [[False for l in range(length)] for w in range(width)]
        
        # The places where stacks have terminatedf
        self.terminated = [[True for l in range(length)] for w in range(width)]
        
        # Axioms are a cube and triangular prism
        self.axioms = [cube_obj.copy(), tri_obj.copy()]
        
        self.nonterminals = [cube_obj.copy(), tri_obj.copy(), empty_obj.copy(), cyl_obj.copy()] 

        self.terminals = [cube_obj.copy(), tri_obj.copy()] 
        
        self.rules = { cube_obj : [self.terminate, self.repeatUp, self.body],
                       tri_obj : [self.terminate, self.mirror, self.empty],
                       empty_obj : [self.terminate, self.repeatUp, self.empty]} 
  
        self.length = length
        self.width = width

        self.maxLength = min(length, width)
  
        # creates square grid
        self.maxSide = min(length, width)-1



        self.minSide = 0

        for l in range(self.maxLength):
            for w in range(self.maxLength):
                self.floorplan[w][l] = True
                self.terminated[w][l] = False


        # While not everything has been terminated
        while not all([done for sublist in self.terminated for done in sublist]):
            rand = uniform(0, 1.0)
            if(rand > 0.2):
                func_i = RING
            else:
                func_i = BODY
            self.expand(func_i)
    
        self.postProcess()


    def expand(self, func_i):
            # Iterate over the stacks of things in grid
            for r in range( len(self.grid) ):
                for c in range( len(self.grid[0]) ):
                    
                    # Only do it if we are allowed to build here
                    if self.floorplan[r][c] and not self.terminated[r][c]:
                        
                        # The current building stack in the grid
                        stack = self.grid[r][c]
                        
                        # len(stack) = height of stack
                        if not stack:
                            self.repeatUp(stack, r, c)
                            #stack.append( self.axioms[CUBE].translate(r,0,c) )
                            continue
                        elif len(stack) >= self.MAX_HEIGHT: #or self.maxSide <= 0:
                            func_i = TERMINATE
                        f = self.rules[ stack[-1] ][func_i]
                        f(stack, r, c)
            rand = uniform(0, 1.0)

            if (rand > 0.85):
                self.maxSide -= 1
                self.minSide += 1

    def repeatUp(self, stack, r, c):
        if(r == self.minSide):
            stack.append( self.nonterminals[TRI].rotate(0,180,180).translate(r, len(stack), c) )
        elif(r == self.maxSide):
            stack.append( self.nonterminals[TRI].rotate(0,0,180).translate(r, len(stack), c) )
        elif(c == self.minSide):
            stack.append( self.nonterminals[TRI].rotate(0,90,180).translate(r, len(stack), c) )
        elif(c == self.maxSide):
            stack.append( self.nonterminals[TRI].rotate(0,-90,180).translate(r, len(stack), c) )
        else:
            stack.append( self.nonterminals[CUBE].translate(r, len(stack), c) )

    # mirrors the last thing on the stack vertically
    def mirror(self, stack, r=None, c=None):
        stack.append( stack[-1].translate(-1*r, -1*len(stack), -1*c).rotate(0,0,180).translate(r, len(stack), c) )

    def terminate(self, stack, r, c):
        self.terminated[r][c] = True
        #stack.append( self.terminals[0].translate(r, len(stack), c) )

    def empty(self, stack, r, c):
        stack.append(self.nonterminals[EMPTY].translate(r, len(stack), c))

    def body(self, stack, r, c):
        if ( r > self.minSide and r < self.maxSide and c > self.minSide and c < self.maxSide):
            stack.append(self.nonterminals[CUBE].translate(r, len(stack), c))
        else:
            stack.append(self.nonterminals[EMPTY].translate(r, len(stack), c))


    def postProcess(self):
        #place cylinders at corners of bounding box
        coords = [(0,0), (0,self.maxLength-1), (self.maxLength-1, self.maxLength-1), (self.maxLength-1, 0)]

        for point in coords:
            stack = self.grid[point[0]][point[1]]
            for i in range(0, len(stack)):
                stack[i] = self.nonterminals[CYL].translate(point[0], i, point[1])

        #places cubes in extra space for now
        for l in range(self.length):
            for w in range(self.width):
                if(not self.floorplan[w][l]):
                    stack = self.grid[w][l]
                    stack.append( self.nonterminals[CUBE].translate(w, 0, l) )

