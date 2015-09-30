from buildingType import *

class Cube(Building):

    def __init__(self, length, width, max_height, seed):
        Building.__init__(self, length, width, max_height, seed)
        
        # A cube has all floorplan things set to true
        self.floorplan = [[True for l in range(length)] for w in range(width)]
        
        # The places where stacks have terminatedf
        self.terminated = [[False for l in range(length)] for w in range(width)]
        
        # Axioms for a cube are just a cube
        self.axioms = [cube_obj.copy()]
        
        self.nonterminals = [cube_obj.copy()] # Fix copy part=fix OBJ constr

        self.terminals = [cube_obj.copy()] 
        
        self.rules = { cube_obj : [self.terminate, self.repeatUp] }
    
        #self.expand()

        self.grid[0][0].append(cube_obj.scale3(length,max_height,width).translate(0,max_height/2,0))
        

    def expand(self):
        # While not everything has been terminated
        while not all([done for sublist in self.terminated for done in sublist]):
            # Iterate over the stacks of things in grid
            for r in range( len(self.grid) ):
                for c in range( len(self.grid[0]) ):
                    
                    # Only do it if we are allowed to build here
                    if self.floorplan[r][c] and not self.terminated[r][c]:
                        
                        # The current building stack in the grid
                        stack = self.grid[r][c]

                        if self.MAX_HEIGHT == 1:
                            self.terminate(stack, r, c)
                            continue

                        # Here we hae to decide what function to take
                        func_i = None # function index
                        
                        # len(stack) = height of stack
                        # - 1 in order not to have terminals go over max height
                        if not stack:
                            stack.append( self.axioms[0].translate(r,0,c) )
                            continue
                        elif len(stack) >= self.MAX_HEIGHT - 1:
                            func_i = 0 # Terminate function
                        else:
                            # Ozther ways to choose function probabilistically
                            func_i = 1 # only expand up for cube
                            
                        #                      obj         func
                        f = self.rules[ stack[-1] ][func_i]
                        f(stack, r, c)


    def repeatUp(self, stack, r=None, c=None):
        stack.append( stack[-1].translate(0, 1, 0) )


    def terminate(self, stack, r, c):
        self.terminated[r][c] = True
        stack.append( self.terminals[0].translate(r, len(stack), c) )
