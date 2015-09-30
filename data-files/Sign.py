from buildingType import *
from sys import argv


# labels for the array indices

A = 0
B = 1
C = 2
D = 3
E = 4
F = 5
G = 6
H = 7
I = 8
J = 9
K = 10
L = 11
M = 12
N = 13
O = 14
P = 15
Q = 16
R = 17
S = 18
T = 19
U = 20
V = 21
W = 22
X = 23
Y = 24
Z = 25

class Sign(Building):

    def __init__(self, length, width, max_height):
        Building.__init__(self, length, width, max_height)


    def makeSign(self, stack, name):
        j = 0
        for i in range(len(name)-1, 0-1, -1):
            if name[i] == " ":
                file = "models/letter/letter_Base.obj"
                mtl  = "models/letter/letter_Base.mtl"
                obj  = OBJ(filename=file, mtlname=mtl)
                stack.append(obj.translate(0,j,0))
                
            else:    
                file = "models/letter/letter_" + name[i] + ".obj"
                mtl  = "models/letter/letter_" + name[i] + ".mtl"
                obj  = OBJ(filename=file, mtlname=mtl)
                stack.append(obj.translate(0,j,0))
             
            j += 1
        
# make the sign posts
            
        file  = "models/cylinders/cylinder_base.obj"
        mtl  = "models/cylinders/cylinder_base.mtl"
        obj  = OBJ(filename=file, mtlname=mtl)
        stack.append(obj.rotate(0,90,0).translate(-0.5,1.0,-0.75))
        stack.append(obj.rotate(0,90,0).translate(-0.5, len(name) - 2.0 , -0.75))




    def terminate(self, stack, r, c):
#        print("terminating " + str(r) + ", " + str(c))
        self.terminated[r][c] = True
        #stack.append( self.terminals[0].translate(r, len(stack), c) )
        
if __name__ == "__main__":
    s = Sign(length=1, width=1, max_height = 1)
    
    name = argv[1]
    s.makeSign(s.grid[0][0], name)
    objFile = name + ".obj"
    s.to_obj().write(objFile)

