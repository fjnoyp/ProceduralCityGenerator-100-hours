import abc
from objectManipulator import *
import random

cube_obj = OBJ(filename="models/cube/Cube_type1.obj",
               mtlname="models/cube/Cube_type1.mtl")

tex_cube_obj = OBJ(filename="models/cube/cube_textured.obj",
                   mtlname="models/cube/cube_textured.mtl")

empty_obj = OBJ(3)
delete_obj = OBJ(100)

small_cyl_obj = OBJ(filename="models/cylinders/cylinder_small.obj")
half_rad_cyl_obj = OBJ(filename="models/cylinders/cylinder_half_radius_type1.obj",
                       mtlname="models/cylinders/cylinder_half_radius_type1.mtl")
full_rad_cyl_obj = OBJ(filename="models/cylinders/cylinder_full_radius_type1.obj", 
                       mtlname="models/cylinders/cylinder_full_radius_type1.mtl")

kitkat_obj = OBJ(filename="models/kitkat/kitkat_emissive_type1.obj", mtlname="models/kitkat/kitkat_emissive_type1.mtl")

window_obj = OBJ(filename="models/advanced/window_type4.obj",
                 mtlname="models/advanced/window_type4.mtl")
vent_obj = OBJ(filename="models/advanced/vent_type1.obj",
               mtlname="models/advanced/vent_type1.mtl")


class Building(object):
    def __init__(self, length, width, max_height, seed=None):
        """Constructor"""

        random.seed(seed)
            
        # WIDTH IS IN X DIRECTION
        # LENGTH IS IN Z DIRECTION

        self.MAX_HEIGHT = max_height
        
        # THIS IS A 2D ARRAY OF STACKS
        # Represents the actual objects over a given point on the grid
        self.grid = [[ [] for l in range(length)] for w in range(width)]
        
        # Tell which boxes on which to build
        self.floorplan = [[False for l in range(length)] for w in range(width)]

        self.terminated = [[True for l in range(length)] for w in range(width)]
        
        # Whether or not a stack has terminated. This will allow us to build
        # outward without worrying about whether a stack below it might run
        # into our outward protrusion. All False squares in floorplan 
        # are considered terminated. The terminate function needs to also
        # make sure to set that x,z to be True (terminated)
        # self.terminated = ["implement me"]*10     

        # The current height of a building part over a grid
        self.heights = [[0 for l in range(length)] for w in range(width)]

        # How to start a building
        self.axioms = []

        # List of nonterminals. Thse are probably objects (liek cubes). Stories.
        # We could change this to be a dict if it'd be more helpful. like
        # nt's = { "cube" : cube_obj, "pencil" : pencil_obj, ... }
        self.nonterminals = []

        # List of terminals. Also objects.
        self.terminals = []

        # Map of nonterminals to list of functions. Each subclass has a unique
        # list of terminals and functions
        self.rules = {}
        
    @abc.abstractmethod
    def expand(self):
        print("IMPLEMENT EXPAND")
        exit()

    @abc.abstractmethod
    def terminate(self, r, c):
        print("IMPLEMENT TERMINATE")
        exit()

    @abc.abstractmethod
    def to_obj(self):
        """Convert object to obj. This should be building type-independent
        Returns an OBJ object"""

        main_obj = OBJ() # The encapsulating object

        # Loop over all stacks of objects
        for r in range(len(self.grid)):
            for c in range(len(self.grid[0])):
                #if not (r == c == 1):
                    #continue
                # Stacks are lists of OBJs
                stack = self.grid[r][c]
                #print(stack)
                for component_obj in stack:
                    main_obj.append(component_obj)
        #commented out to avoid dup writing - Kai
        #main_obj.write("test.obj")
        return main_obj
        


"""
    def growOutwards(self, stack, r, c):
        if terminated[r+1][c+1]:
            s2 = self.grid[r+1][c+1]
            # make sure the modifier methods return a new object
            s2.append( cube_obj.translate(0, len(stack), 0) )
        elif terminated[r-1][c+1]:
            # s2....
            pass
"""     


class BuildingType:

    def __init__(self, t):
        self.metaType = t
